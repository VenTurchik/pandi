import pytest

from main import build_arg_parser, Pandi


def test_arg_parser_defaults():
    parser = build_arg_parser()
    ns = parser.parse_args([])
    assert ns.vfs_path is None
    assert ns.script_path is None


def test_arg_parser_vfs_only():
    parser = build_arg_parser()
    ns = parser.parse_args(["--vfs", "/tmp/a.zip"])
    assert ns.vfs_path == "/tmp/a.zip"
    assert ns.script_path is None


def test_arg_parser_script_only():
    parser = build_arg_parser()
    ns = parser.parse_args(["--script", "scripts/01_ok.pandi"])
    assert ns.script_path == "scripts/01_ok.pandi"
    assert ns.vfs_path is None


def test_arg_parser_both():
    parser = build_arg_parser()
    ns = parser.parse_args(
        ["--vfs", "/a/b.zip", "--script", "scripts/demo.txt"]
    )
    assert ns.vfs_path == "/a/b.zip"
    assert ns.script_path == "scripts/demo.txt"


def test_arg_parser_unknown_raises():
    parser = build_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--unknown", "x"])


def test_debug_dump(capsys):
    app = Pandi(vfs_path="/a/b.zip", script_path="scripts/01_ok.pandi")
    app._debug_dump_config()
    out = capsys.readouterr().out
    assert "vfs_path" in out
    assert "/a/b.zip" in out
    assert "script_path" in out
    assert "01_ok.pandi" in out
