from commands.cmd_cd import cmd_cd
from commands.cmd_ls import cmd_ls

def test_ls_no_args():
    assert cmd_ls([]) == "ls"

def test_ls_one_arg():
    assert cmd_ls(["-la"]) == "ls -la"

def test_ls_many_args():
    assert cmd_ls(["-la", "/home"]) == "ls -la /home"

def test_cd_no_args():
    assert cmd_cd([]) == "cd"

def test_cd_one_arg():
    assert cmd_cd(["/tmp"]) == "cd /tmp"

def test_cd_many_args():
    assert cmd_cd(["/tmp", "extra"]) == "cd /tmp extra"