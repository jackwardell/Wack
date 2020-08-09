import os
import tempfile
import venv
from pathlib import Path
import pytest
from click.testing import CliRunner


@pytest.fixture(scope='function')
def tempdir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(temp_dir)
        venv.create("venv")
        path = Path("/private" + temp_dir)
        assert os.getcwd() == path.as_posix()
        yield path
        os.chdir(current_dir)


# @pytest.fixture
# def tempdir_wack(tempdir):
#     with open("wack.py", "w+") as _:
#         pass
#     yield tempdir + "/wack.py"


@pytest.fixture
def runner():
    yield CliRunner()

# @pytest.fixture
# def dockerfile():
#     if os.getenv("IN_DOCKERFILE") != "1":
#         pytest.skip("Not in Dockerfile")
#
#     client = docker.from_env()
#     image, logs = client.images.build(path=DOCKER_FILE[0], dockerfile=DOCKER_FILE[1])
#     client.containers.run(image)
#     image.run()
#     yield
