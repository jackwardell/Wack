import os
import tempfile
import venv
from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="function")
def tempdir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(temp_dir)
        venv.create("venv")
        path = (
            Path("/private" + temp_dir)
            if "private" in os.listdir("/")
            else Path(temp_dir)
        )
        assert os.getcwd() == path.as_posix()
        yield path
        os.chdir(current_dir)


@pytest.fixture
def runner():
    yield CliRunner()
