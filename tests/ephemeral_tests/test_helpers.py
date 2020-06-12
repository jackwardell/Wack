from wack.helpers import WackFile


def test_wack_file_init(tempdir):
    with open("wack.py", "w+") as _:
        pass

    wack_file = WackFile(".")
    assert False
