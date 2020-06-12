import os
import tempfile
import venv
import IPython
import docker
import pytest
from click.testing import CliRunner

DOCKER_FILE = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    "DockerfileForTesting",
)


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(temp_dir)
        venv.create("venv")
        yield temp_dir
        os.chdir(current_dir)


@pytest.fixture
def runner():
    yield CliRunner()


@pytest.fixture
def dockerfile():
    if os.getenv("IN_DOCKERFILE") != "1":
        pytest.skip("Not in Dockerfile")

    client = docker.from_env()
    image, logs = client.images.build(path=DOCKER_FILE[0], dockerfile=DOCKER_FILE[1])
    client.containers.run(image)
    image.run()
    yield
