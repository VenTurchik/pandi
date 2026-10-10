import pytest

from commands.errors import CommandError
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
    with pytest.raises(CommandError) as exc:
        app._command_manager(["lol"])
    assert str(exc.value) == "lol: command not found"


def test_manager_unknown_with_args():
    app = Pandi()
    with pytest.raises(CommandError) as exc:
        app._command_manager(["lol", "bar", "baz"])
    assert str(exc.value) == "lol: command not found"
