from main import str2bool

def test_str2bool():
    assert str2bool("trUe") == True
    assert str2bool("1") == True
    assert str2bool("asd") == False
    assert str2bool("2") == False
    assert str2bool("0") == False