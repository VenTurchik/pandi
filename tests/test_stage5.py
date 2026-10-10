import zipfile

import pytest

from commands.errors import CommandError
from main import Pandi, main


def make_zip(path, files):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files:
            if isinstance(data, str):
                data = data.encode()
            zf.writestr(name, data)


def make_app(vfs_path):
    return Pandi(vfs_path=vfs_path)


def test_help_lists_all():
    app = make_app(None)
    out = app._command_manager(["help"])
    for name in ["ls", "cd", "cp", "date",
                 "help", "history", "exit"]:
        assert name in out


def test_cp_missing_operand(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cp", "a.txt"])
    assert "missing" in str(exc.value)


def test_cp_extra_operand(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cp", "a", "b", "c"])
    assert "extra" in str(exc.value)


def test_cp_no_such_source(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cp", "/nope", "/x"])
    assert "No such file" in str(exc.value)


def test_cp_source_is_dir(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cp", "/a", "/x"])
    assert "omitting directory" in str(exc.value)


def test_cp_new_file(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hello")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._command_manager(["cp", "/a.txt", "/b.txt"])
    out = app._command_manager(["ls"])
    assert "b.txt" in out
    from vfs import get_node

    node = get_node(app._vfs, "/b.txt")
    assert node["data"] == b"hello"


def test_cp_into_dir(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi"), ("d/b.txt", "x")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._command_manager(["cp", "/a.txt", "/d"])
    out = app._command_manager(["ls", "/d"])
    assert "a.txt" in out


def test_cp_overwrite(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "aaa"), ("b.txt", "bbb")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._command_manager(["cp", "/a.txt", "/b.txt"])
    from vfs import get_node

    node = get_node(app._vfs, "/b.txt")
    assert node["data"] == b"aaa"


def test_cp_no_parent(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cp", "/a.txt", "/nope/x"])
    assert "No such file" in str(exc.value)


def test_cp_relative(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b.txt", "hi"), ("a/c.txt", "x")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._cwd = "/a"
    app._command_manager(["cp", "b.txt", "copy.txt"])
    out = app._command_manager(["ls"])
    assert "copy.txt" in out


def test_cp_copies_bytes(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._command_manager(["cp", "/a.txt", "/b.txt"])
    from vfs import get_node

    src = get_node(app._vfs, "/a.txt")
    dst = get_node(app._vfs, "/b.txt")
    assert src is not dst
    assert src["data"] == dst["data"]


def test_cp_stub_without_vfs():
    app = make_app(None)
    assert app._command_manager(["cp", "a", "b"]) == "cp a b"


def test_main_cp_ok(tmp_path, capsys):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/top.txt", "hi")])
    s = tmp_path / "s.pandi"
    s.write_text("cp /a/top.txt /copy.txt\nls\nexit\n")
    rc = main(["--vfs", str(z), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "copy.txt" in out


def test_main_cp_error(tmp_path, capsys):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    s = tmp_path / "s.pandi"
    s.write_text("cp /nope /x\n")
    rc = main(["--vfs", str(z), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "No such file" in out
