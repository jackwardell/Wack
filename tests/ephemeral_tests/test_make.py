import os


def test_make(dockerfile):
    assert os.getenv("IN_DOCKERFILE")
