"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Generator

import pytest

if TYPE_CHECKING:
    # Local type stub for mypy that works with both pytest < 7 and pytest >=7
    # https://docs.pytest.org/en/7.1.x/_modules/_pytest/legacypath.html#TempdirFactory
    import py

    class TempdirFactory:
        def mktemp(self, path: str) -> py.path.local:
            ...


from inmanta.agent import config as inmanta_config
from paramiko import sftp_client
from pytest_inmanta.plugin import Project

from pytest_inmanta_yang.const import VENDOR_CISCO
from pytest_inmanta_yang.netconf_device_helper import (
    NetconfDeviceHelper,
    NetconfOperation,
)
from pytest_inmanta_yang.yang_test import YangTest

LOGGER = logging.getLogger(__name__)

logging.getLogger("ncclient").setLevel(logging.ERROR)
logging.getLogger("ncdiff.model").setLevel(logging.CRITICAL)
logging.getLogger("paramiko").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def netconf_device_initial_config_path_file() -> str:
    """
    Empty fixture to be overridden.

    It should return the path to the file containing startup config for the device.

        .. code_block:: python

            import os
            import pytest
            from pytest_inmanta_yang import NetconfDeviceHelper

            @pytest.fixture(scope="session")
            def netconf_device_initial_config_path_file() -> str:
                hostname = os.getenv(NetconfDeviceHelper.ENV_VARIABLE_HOSTNAME)
                return os.path.join(os.path.dirname(__name__), f"resources/{hostname}.xml")

    """
    raise NotImplementedError("You should overwrite this fixture")


@pytest.fixture(scope="session")
def session_temp_dir(
    tmpdir_factory: "TempdirFactory", request: pytest.FixtureRequest
) -> Generator[str, None, None]:
    fixed_cache_dir = request.config.getoption("--cache-dir")
    if not fixed_cache_dir:
        LOGGER.info(
            "Using temporary cache folder, this will require reloading of all yang files. Use --cache-dir to prevent this"
        )
        session_temp_dir = tmpdir_factory.mktemp("session")
        yield str(session_temp_dir)
        session_temp_dir.remove(ignore_errors=True)
    else:
        # fixed cache
        LOGGER.info("Using fixed cache folder")
        abspath = os.path.abspath(fixed_cache_dir)
        os.makedirs(fixed_cache_dir, exist_ok=True)
        yield str(abspath)


@pytest.fixture
def use_session_temp_dir(session_temp_dir: str) -> Generator[str, None, None]:
    inmanta_config.state_dir.set(str(session_temp_dir))
    yield inmanta_config.state_dir.get()


def cisco_cleanup(netconf_device: NetconfDeviceHelper, initial_path: str) -> None:
    """
    Cleanup for Cisco IOS-XR device.
    It is done by uploading and overriding startup config file using SSH
    """
    LOGGER.info(
        f"Cleaning up Cisco device: `{netconf_device.hostname}` - startup config file will be uploaded using SSH"
    )
    LOGGER.debug(f"read config and upload to : `{netconf_device.hostname}`")
    with netconf_device.get_ssh_connect() as ssh:
        # copy the file first
        client = sftp_client.SFTPClient.from_transport(ssh.channel.transport.session)
        assert client is not None
        client.put(initial_path, "disk0:/baseconfig.cfg")
        ssh.send_command("copy disk0:/baseconfig.cfg running-config replace")

    LOGGER.info(f"Cleanup done for Cisco device: `{netconf_device.hostname}`")


def netconf_cleanup(netconf_device: NetconfDeviceHelper, initial_path: str) -> None:
    """
    Cleanup for device using netconf.
    It is done by editing the device config with the config located in initial_path.
    """
    LOGGER.info(
        f"Cleaning up {netconf_device.hostname} (vendor: {netconf_device.vendor})"
    )
    initial_config = Path(initial_path).read_text()

    LOGGER.debug(f"Deploying initial config on device: \n{initial_config}")
    netconf_device.edit_config(
        initial_config, default_operation=NetconfOperation.REPLACE
    )

    LOGGER.info("Cleanup done")


@pytest.fixture(scope="session")
def netconf_device_global(
    netconf_device_initial_config_path_file: str,
) -> Generator[NetconfDeviceHelper, None, None]:
    """
    Building the netconf device helper and cleaning up the router after the tests.
    """
    device = NetconfDeviceHelper.using_env_variables()
    yield device

    LOGGER.info("Running end of session cleanup")
    if device.vendor == VENDOR_CISCO:
        cisco_cleanup(device, netconf_device_initial_config_path_file)
    else:
        netconf_cleanup(device, netconf_device_initial_config_path_file)


@pytest.fixture(scope="function")
def netconf_device(
    netconf_device_global: NetconfDeviceHelper,
    netconf_device_initial_config_path_file: str,
) -> Generator[NetconfDeviceHelper, None, None]:
    """
    Cleanup the router before the test

    This fixture is picked up automatically when using the yang fixture from pytest_inmanta_yang.
    Other modules using pytest_inmanta_yang will have to overwrite it with their own cleanup.
    """
    LOGGER.info("Running pre-test cleanup")
    if netconf_device_global.vendor == VENDOR_CISCO:
        cisco_cleanup(netconf_device_global, netconf_device_initial_config_path_file)
    else:
        netconf_cleanup(netconf_device_global, netconf_device_initial_config_path_file)

    yield netconf_device_global


@pytest.fixture
def yang(
    request: pytest.FixtureRequest,
    project: Project,
    netconf_device: NetconfDeviceHelper,
    use_session_temp_dir: str,
) -> Generator[YangTest, None, None]:
    mgr = YangTest(project, netconf_device)
    yield mgr

    if not request.node.rep_call.passed:
        mgr.report_state()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> Generator[None, None, None]:
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()  # type: ignore

    # set a report attribute for each phase of a call, when can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
