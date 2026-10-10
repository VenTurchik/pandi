import zipfile

import pytest

from vfs import VfsError, get_motd, load_vfs
from main import main


def make_zip(path, files):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files:
            if isinstance(data, str):
                data = data.encode()
            zf.writestr(name, data)


def test_load_minimal(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("hello.txt", "hello\n")])
    vfs = load_vfs(str(z))
    assert "hello.txt" in vfs["children"]
    assert not vfs["children"]["hello.txt"]["__dir"]


def test_load_few(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [
        ("a.txt", "a\n"),
        ("b.txt", "b\n"),
        ("docs/readme.txt", "hi\n"),
    ])
    vfs = load_vfs(str(z))
    assert "a.txt" in vfs["children"]
    assert "docs" in vfs["children"]
    assert "readme.txt" in vfs["children"]["docs"]["children"]


def test_load_deep(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("a/b/c/file.txt", "deep\n")])
    vfs = load_vfs(str(z))
    assert "a" in vfs["children"]
    a = vfs["children"]["a"]
    assert "b" in a["children"]
    b = a["children"]["b"]
    assert "c" in b["children"]
    assert "file.txt" in b["children"]["c"]["children"]


def test_motd_present(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("motd", "hi motd\n"), ("x.txt", "x")])
    vfs = load_vfs(str(z))
    assert get_motd(vfs) == "hi motd\n"


def test_motd_missing(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("hello.txt", "hi")])
    vfs = load_vfs(str(z))
    assert get_motd(vfs) is None


def test_motd_is_dir(tmp_path):
    z = tmp_path / "a.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("motd/", "")
    vfs = load_vfs(str(z))
    assert get_motd(vfs) is None


def test_not_found():
    with pytest.raises(VfsError) as exc:
        load_vfs("/no/such/file.zip")
    assert "no such file" in str(exc.value)


def test_bad_format(tmp_path):
    p = tmp_path / "bad.zip"
    p.write_text("not a zip")
    with pytest.raises(VfsError) as exc:
        load_vfs(str(p))
    assert "bad zip format" in str(exc.value)


def test_motd_printed(tmp_path, capsys):
    z = tmp_path / "v.zip"
    make_zip(z, [("motd", "Hello MOTD\n"), ("a.txt", "a")])
    s = tmp_path / "s.pandi"
    s.write_text("ls\nexit\n")
    rc = main(["--vfs", str(z), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Hello MOTD" in out


def test_vfs_error_rc1(tmp_path, capsys):
    s = tmp_path / "s.pandi"
    s.write_text("ls\n")
    rc = main(["--vfs", "/no/such.zip", "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "cannot load vfs" in out


def test_bad_vfs_rc1(tmp_path, capsys):
    p = tmp_path / "bad.zip"
    p.write_text("bad")
    s = tmp_path / "s.pandi"
    s.write_text("ls\n")
    rc = main(["--vfs", str(p), "--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "bad zip format" in str(out)


def test_no_vfs_no_motd(tmp_path, capsys):
    s = tmp_path / "s.pandi"
    s.write_text("ls\nexit\n")
    rc = main(["--script", str(s)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Hello MOTD" not in out


def test_no_extract(tmp_path):
    z = tmp_path / "a.zip"
    make_zip(z, [("a/b/c.txt", "hi")])
    vfs = load_vfs(str(z))
    assert not (tmp_path / "a").exists()
    assert vfs["children"]["a"]["children"]["b"][
        "children"
    ]["c.txt"]["data"] == b"hi"
