from pyraptor.main import main


def test_main():
    result = main('12TH', '24TH')

    assert result is not None
    print(result)
