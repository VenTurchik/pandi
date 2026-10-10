import os
import tempfile

import pytest

from main import Pandi, main
from script import run_script


def make_script(content: str) -> str:
    """Создать временный .pandi-файл."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".pandi",
        delete=False,
        encoding="utf-8",
    )
    tmp.write(content)
    tmp.flush()
    tmp.close()
    return tmp.name


def test_run_script_ok(capsys):
    path = make_script("ls\nls -la\n")
    try:
        app = Pandi()
        ok = run_script(app, path)
        out = capsys.readouterr().out
        assert ok is True
        assert "ls" in out
        assert "ls -la" in out
    finally:
        os.unlink(path)


def test_run_script_stops_on_error(capsys):
    path = make_script("ls\nlolkek foo\nls -la\n")
    try:
        app = Pandi()
        ok = run_script(app, path)
        out = capsys.readouterr().out
        assert ok is False
        assert "lolkek: command not found" in out
        assert "stopped at line 2" in out
        echo_lines = [
            ln for ln in out.splitlines() if "ls -la" in ln
        ]
        assert echo_lines == []
    finally:
        os.unlink(path)


def test_run_script_comments_and_blanks(capsys):
    content = "# коммент\n\nls\n   # ещё коммент\nls -la\n"
    path = make_script(content)
    try:
        app = Pandi()
        ok = run_script(app, path)
        out = capsys.readouterr().out
        assert ok is True
        assert "ls" in out
        assert "коммент" not in out
        assert "ещё коммент" not in out
    finally:
        os.unlink(path)


def test_run_script_empty(capsys):
    path = make_script("")
    try:
        app = Pandi()
        ok = run_script(app, path)
        assert ok is True
    finally:
        os.unlink(path)


def test_run_script_exit_stops(capsys):
    path = make_script("ls\nexit\nls -la\n")
    try:
        app = Pandi()
        app._is_enable = True
        ok = run_script(app, path)
        out = capsys.readouterr().out
        assert ok is True
        assert app._is_enable is False
        assert "ls -la" not in out
    finally:
        os.unlink(path)


def test_run_script_not_found(capsys):
    app = Pandi()
    ok = run_script(app, "/nonexistent/path/script.pandi")
    out = capsys.readouterr().out
    assert ok is False
    assert "cannot open script" in out


def test_main_with_script(monkeypatch, capsys, tmp_path):
    script = tmp_path / "ok.pandi"
    script.write_text("ls\nexit\n", encoding="utf-8")
    rc = main(["--vfs", "/tmp/a.zip", "--script", str(script)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "vfs_path" in out
    assert "/tmp/a.zip" in out
    assert "ok.pandi" in out


def test_main_script_error(monkeypatch, capsys, tmp_path):
    script = tmp_path / "bad.pandi"
    script.write_text("lolkek\n", encoding="utf-8")
    rc = main(["--script", str(script)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "command not found" in out


def test_main_script_not_found(capsys):
    rc = main(["--script", "/no/such/file.pandi"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "cannot open script" in out
