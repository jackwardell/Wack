import tempfile
import os
import pytest


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(current_dir)
