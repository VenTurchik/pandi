from main import Pandi

def test_manager_ls_no_args():
    app = Pandi()
    assert app._command_manager(["ls"]) == "ls"

def test_manager_ls_with_args():
    app = Pandi()
    assert app._command_manager(["ls", "-la", "/home"]) == "ls -la /home"

def test_manager_cd():
    app = Pandi()
    assert app._command_manager(["cd", "/tmp"]) == "cd /tmp"

def test_manager_unknown_command():
    app = Pandi()
    assert app._command_manager(["lol"]) == "lol: command not found"

def test_manager_unknown_with_args():
    app = Pandi()
    result = app._command_manager(["lol", "bar", "baz"])
    assert result == "lol: command not found"