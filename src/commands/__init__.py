from commands.cmd_ls import cmd_ls
from commands.cmd_cd import cmd_cd
from commands.errors import CommandError

REGISTRY = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}

__all__ = ["REGISTRY", "CommandError"]
