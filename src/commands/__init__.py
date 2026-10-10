from commands.cmd_ls import cmd_ls
from commands.cmd_cd import cmd_cd
from commands.cmd_date import cmd_date
from commands.cmd_history import cmd_history
from commands.errors import CommandError

REGISTRY = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "date": cmd_date,
    "history": cmd_history,
}

__all__ = ["REGISTRY", "CommandError"]
