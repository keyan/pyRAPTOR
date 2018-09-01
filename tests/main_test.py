from pyraptor.main import main


def test_main():
    result = main('M06N', '103')

    assert result is not None
