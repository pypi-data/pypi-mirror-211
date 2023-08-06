""" module:: test.tests_program_file
    :platform: Posix
    :synopsis: Tests for module uds.common
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from pathlib import Path

import pytest

from uds.program_file import UpdateContainerOdxFile, PackedUpdateContainer


@pytest.fixture
def flash_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_odx.odx"))[0]


@pytest.fixture
def flash_pdx_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_pdx.odx"))[0]


@pytest.fixture
def pdx_file_mock() -> Path:
    yield list(Path(".").glob("**/data/test_pdx.pdx"))[0]


class TestProgrammFiles:

    def test_flash_odx_file(self, flash_odx, tmp_path):
        odx = UpdateContainerOdxFile(flash_odx)
        alfid = odx.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        blocks = odx.get_blocks()
        assert blocks
        print(blocks)
        expected_idents = odx.get_expected_idents()
        assert expected_idents
        print(expected_idents)

        own_idents = odx.get_own_idents()
        assert own_idents
        print(own_idents)

        p = tmp_path / "test_write_flash_pdx.odx"
        odx._write_file(p)

        p = tmp_path / "test_write_flash_odx.odx"
        odx._write_file(filepath=p, format_flash_pdx=True)

    def test_flash_pdx_odx_file(self, flash_pdx_odx):
        odx = UpdateContainerOdxFile(flash_pdx_odx)
        alfid = odx.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        blocks = odx.get_blocks()
        assert blocks
        print(blocks)
        expected_idents = odx.get_expected_idents()
        assert expected_idents
        print(expected_idents)

    def test_pdx_file(self, pdx_file_mock, tmp_path):
        pdx_obj = PackedUpdateContainer(pdx_file_mock)

        alfid = pdx_obj.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        #print(alfid)

        blocks = pdx_obj.get_blocks()
        assert blocks
        expected_idents = pdx_obj.get_expected_idents()
        assert expected_idents
        #print(expected_idents)

        own_idents = pdx_obj.get_own_idents()
        assert own_idents
        #print(own_idents)

        #print(pdx_obj.security_methods)

        p = tmp_path / "test_pdx.pdx"
        pdx_obj._write_file(p)

        with pytest.raises(ValueError):
            PackedUpdateContainer(Path("Some_None_Existing_Path"))
