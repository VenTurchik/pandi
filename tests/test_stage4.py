import zipfile

import pytest

from commands.errors import CommandError
from main import Pandi, main
from vfs import get_node, resolve


def make_zip(path, files):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files:
            if isinstance(data, str):
                data = data.encode()
            zf.writestr(name, data)


def make_app(vfs_path):
    return Pandi(vfs_path=vfs_path)


def test_resolve_absolute():
    assert resolve("/", "/a/b") == "/a/b"


def test_resolve_relative():
    assert resolve("/a", "b/c") == "/a/b/c"


def test_resolve_dotdot():
    assert resolve("/a/b", "../c") == "/a/c"
    assert resolve("/a/b", "../../") == "/"
    assert resolve("/", "..") == "/"


def test_resolve_dot_slash():
    assert resolve("/a/b", "./c") == "/a/b/c"
    assert resolve("/a", ".") == "/a"


def test_get_node_root(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("a/b.txt", "hi")])
    from vfs import load_vfs

    vfs = load_vfs(str(z))
    assert get_node(vfs, "/") is vfs


def test_get_node_found(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("a/b/c.txt", "hi")])
    from vfs import load_vfs

    vfs = load_vfs(str(z))
    node = get_node(vfs, "/a/b")
    assert node is not None
    assert node["__dir"]


def test_get_node_missing(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("a.txt", "hi")])
    from vfs import load_vfs

    vfs = load_vfs(str(z))
    assert get_node(vfs, "/nope") is None


def test_ls_root(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "a"), ("b.txt", "b")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    out = app._command_manager(["ls"])
    assert "a.txt" in out
    assert "b.txt" in out


def test_ls_subdir(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b.txt", "hi"), ("a/c.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    out = app._command_manager(["ls", "/a"])
    assert "b.txt" in out
    assert "c.txt" in out


def test_ls_file(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b/c.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    out = app._command_manager(["ls", "/a/b/c.txt"])
    assert out == "c.txt"


def test_ls_no_such_file(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["ls", "/nope"])
    assert "No such file" in str(exc.value)


def test_ls_with_flag(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    out = app._command_manager(["ls", "-la"])
    assert "a.txt" in out


def test_cd_ok(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b/c.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._command_manager(["cd", "/a/b"])
    assert app._cwd == "/a/b"
    app._command_manager(["cd", ".."])
    assert app._cwd == "/a"
    app._command_manager(["cd", "/"])
    assert app._cwd == "/"


def test_cd_no_args(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a/b.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._cwd = "/a"
    app._command_manager(["cd"])
    assert app._cwd == "/"


def test_cd_not_found(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cd", "/nope"])
    assert "No such file" in str(exc.value)


def test_cd_not_dir(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    app = make_app(str(z))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    with pytest.raises(CommandError) as exc:
        app._command_manager(["cd", "/a.txt"])
    assert "Not a directory" in str(exc.value)


def test_date(tmp_path):
    app = make_app(None)
    out = app._command_manager(["date"])
    assert len(out) > 0
    assert "202" in out


def test_history_via_script(tmp_path):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    s = tmp_path / "s.pandi"
    s.write_text("ls\ndate\nhistory\nexit\n")
    app = Pandi(vfs_path=str(z), script_path=str(s))
    from vfs import load_vfs

    app._vfs = load_vfs(str(z))
    app._is_enable = True
    from script import run_script
    import io
    import sys

    cap = io.StringIO()
    old = sys.stdout
    sys.stdout = cap
    try:
        run_script(app, str(s))
    finally:
        sys.stdout = old
    out = cap.getvalue()
    assert "1" in out
    assert "history" in out


def test_main_stage4_ok(tmp_path, capsys):
    z = tmp_path / "v.zip"
    make_zip(z, [
        ("a/b/c/file.txt", "hi"),
        ("a/top.txt", "hi"),
    ])
    s = tmp_path / "s.pandi"
    s.write_text("ls\ncd /a\nls\nexit\n")
    rc = main(["--vfs", str(z), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "a" in out


def test_main_stage4_error(tmp_path, capsys):
    z = tmp_path / "v.zip"
    make_zip(z, [("a.txt", "hi")])
    s = tmp_path / "s.pandi"
    s.write_text("cd /nope\n")
    rc = main(["--vfs", str(z), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "No such file" in out
