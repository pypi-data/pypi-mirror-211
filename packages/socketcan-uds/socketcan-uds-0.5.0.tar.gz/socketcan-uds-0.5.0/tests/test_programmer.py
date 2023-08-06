""" module:: tests.test_programmer
    :platform: Posix
    :synopsis: Tests for module uds.programmer
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import pickle
import time
from pathlib import Path

import pytest

from tests.mocks import MockSocket, SilentMockSocket
from uds.client import *
from uds.common import ResponseCode
from uds.program_file import ExampleProgrammingFile
from uds.programmer import ExampleUdsProgrammer, EXAMPLE_PROGRAMMING_FILE_DICT, OdxFileProgrammerBase
from uds.programmer import ProgrammerState

LOGGER = logging.getLogger()


@pytest.fixture
def mock_socket() -> MockSocket:
    yield MockSocket()


@pytest.fixture
def mock_client(mock_socket) -> UdsClient:
    # noinspection PyTypeChecker
    client = UdsClient(socket=mock_socket)
    yield client


@pytest.fixture
def mock_programmer(mock_client) -> ExampleUdsProgrammer:
    programmer = ExampleUdsProgrammer(client=mock_client)
    yield programmer


@pytest.fixture
def mock_programming_file_path(tmpdir) -> Path:
    pkl_path = Path(tmpdir, "test.pkl")
    with pkl_path.open("wb") as f:
        pickle.dump(EXAMPLE_PROGRAMMING_FILE_DICT, f)
    yield pkl_path


@pytest.fixture
def mock_programming_file(mock_programming_file_path) -> ExampleProgrammingFile:
    yield ExampleProgrammingFile(filepath=mock_programming_file_path)


class TestProgrammingFile:

    def test_class_init(self, mock_programming_file):
        filepath = mock_programming_file._filepath
        pf = ExampleProgrammingFile(filepath=filepath)
        blocks = pf.get_blocks()
        assert blocks


class TestExampleUdsProgrammer:

    def test_class_init(self):
        with pytest.raises(ValueError):
            ExampleUdsProgrammer(client=mock_client,
                                 programming_filepath=Path("some filepath"))

    def test_class_properties(self, mock_programmer):
        mock_programmer.register_hook(print)
        mock_programmer.state = ProgrammerState.ProgrammingError
        assert mock_programmer.state == ProgrammerState.ProgrammingError

        with pytest.raises(AssertionError):
            mock_programmer.state = 42

        mock_programmer.current_programming_block = ("block_100", 100, 100)
        assert mock_programmer.current_programming_block == ("block_100", 100, 100)

        mock_programmer.current_block_progress = (99, 100)
        assert mock_programmer.current_block_progress == (99, 100)

        # just for coverage no test yet
        mock_programmer.get_uds_server_block_versions()
        mock_programmer.get_uds_server_identification()

    def test_load_programming_file(self, mock_programmer, tmpdir, mock_programming_file_path):
        mock_programmer.load_programming_file(filepath=mock_programming_file_path)
        assert mock_programmer._programming_file is not None
        with pytest.raises(ValueError):
            mock_programmer.load_programming_file(filepath=Path("some_path"))
        tempfile = Path(tmpdir).joinpath("test.txt")
        with open(tempfile, "w") as f:
            f.write("test")
        with pytest.raises(ValueError):
            mock_programmer.load_programming_file(filepath=tempfile)

    def test_check_if_connected(self, mock_programmer):
        mock_programmer.try_to_connect()

        mock_programmer._client._s = SilentMockSocket()
        mock_programmer.try_to_connect()

    def test_uds_timeout_during_pre_programming(self, mock_programmer):
        mock_programmer.state_to_function_dict.update(
            {ProgrammerState.NotConnected: lambda: ProgrammerState.ProgrammingFinished})
        mock_programmer._state = ProgrammerState.PreProgramming
        mock_programmer._client._s = SilentMockSocket()
        mock_programmer.handle_state_machine()

    def test_switch_to_programming_mode(self, mock_programmer):
        assert mock_programmer.switch_to_programming_mode() == ProgrammerState.UnlockDeviceForProgramming
        mock_programmer._client._s = SilentMockSocket()
        assert mock_programmer.switch_to_programming_mode() == ProgrammerState.ProgrammingError

    def test_unlock_device(self, mock_programmer):
        assert mock_programmer.unlock_device() == ProgrammerState.BlockProgramming
        mock_programmer._client._s = SilentMockSocket()
        assert mock_programmer.unlock_device() == ProgrammerState.ProgrammingError

    def test_pre_block_download(self, mock_programmer):
        mock_programmer.pre_block_download(addr=0x1234, erase_block=False)

    def test_block_programming(self, mock_programmer, mock_programming_file_path):
        mock_programmer.load_programming_file(filepath=mock_programming_file_path)
        assert mock_programmer.block_programming() == ProgrammerState.PostProgramming
        mock_programmer._client._s = SilentMockSocket()
        assert mock_programmer.block_programming() == ProgrammerState.ProgrammingError

    def test_download_block(self, mock_programmer):
        mock_programmer.download_block(addr=0x11223344,
                                       data=bytes.fromhex("11 22 33 44 55 66 77 88"),
                                       size=8)
        mock_programmer.download_block(addr=0x1234,
                                       data=bytes.fromhex("11 22 33 44 55 66 77 88"),
                                       size=8)

    def test_post_block_download(self, mock_programmer):
        mock_programmer.post_block_download(addr=0x1234,
                                            checksum=bytes(range(15)),
                                            signature=bytes(range(15)))

    def test_post_programming(self, mock_programmer):
        mock_programmer.post_programming()

    def test_state_machine(self, mock_programmer, mock_programming_file):
        mock_programmer._programming_file = mock_programming_file
        mock_programmer.start_programming()
        time.sleep(3)
        assert mock_programmer.current_block_progress == (8, 8)
        assert mock_programmer.state == ProgrammerState.ProgrammingFinished

    def test_state_machine_unhandled_state(self, mock_programmer, mock_programming_file):
        mock_programmer._programming_file = mock_programming_file
        mock_programmer.state_to_function_dict.update({ProgrammerState.Init: lambda: ProgrammerState.TestOnly})
        mock_programmer.start_programming()
        time.sleep(1)
        assert mock_programmer.state == ProgrammerState.ProgrammingError

    def test_switch_to_block_wait(self, mock_programmer, mock_socket):
        mock_programmer.state = ProgrammerState.UnlockDeviceForProgramming
        mock_socket.send_uds_error(ResponseCode.RequiredTimeDelayNotExpired)
        mock_programmer.state = mock_programmer.switch_to_programming_mode()
        assert mock_programmer.state == ProgrammerState.AccessUnblockWait
        mock_programmer.state = mock_programmer.access_unblock_wait()
        assert mock_programmer.state == ProgrammerState.UnlockDeviceForProgramming


@pytest.fixture()
def mock_odx_file_programmer_base() -> OdxFileProgrammerBase:
    yield OdxFileProgrammerBase(client=mock_client)


@pytest.fixture
def pdx_file_mock() -> Path:
    yield list(Path(".").glob("**/data/test_pdx.pdx"))[0]


class TestOdxFileProgrammerBase:
    def test_load_programming_file_errors(self, mock_odx_file_programmer_base, mock_programming_file_path):
        with pytest.raises(ValueError):
            mock_odx_file_programmer_base.load_programming_file(Path("some filepath"))
        with pytest.raises(ValueError):
            mock_odx_file_programmer_base.load_programming_file(mock_programming_file_path)

    def test_load_programming_file(self, mock_odx_file_programmer_base, pdx_file_mock):
        mock_odx_file_programmer_base.load_programming_file(pdx_file_mock)

    def test_state_functions(self, mock_odx_file_programmer_base):
        """
        A simple call of all functions just to achieve coverage.
        :return: Nothing.
        """
        mock_odx_file_programmer_base.unlock_device()
        mock_odx_file_programmer_base.pre_programming()
        mock_odx_file_programmer_base.access_unblock_wait()
        mock_odx_file_programmer_base.access_unblock_wait()
        mock_odx_file_programmer_base.pre_block_download(addr=0x1234, erase_block=False)
        mock_odx_file_programmer_base.post_block_download(addr=0x1234, checksum=b"1234", signature=b"5678")
        mock_odx_file_programmer_base.post_programming()
