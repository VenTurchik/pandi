from main import Pandi

def test_parser_simple():
    app = Pandi()
    assert app._parser("ls") == ["ls"]

def test_parser_with_args():
    app = Pandi()
    assert app._parser("ls -la /home") == ["ls", "-la", "/home"]

def test_parser_multiple_spaces():
    app = Pandi()
    assert app._parser("ls   -la") == ["ls", "-la"]

def test_parser_leading_trailing():
    app = Pandi()
    assert app._parser("  ls -la  ") == ["ls", "-la"]