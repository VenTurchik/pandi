from commands.cmd_ls import cmd_ls
from commands.cmd_cd import cmd_cd

REGISTRY = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}