from commands.cmd_ls import cmd_ls
from commands.cmd_cd import cmd_cd
from commands.cmd_cp import cmd_cp
from commands.cmd_date import cmd_date
from commands.cmd_help import cmd_help
from commands.cmd_history import cmd_history
from commands.errors import CommandError

REGISTRY = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "cp": cmd_cp,
    "date": cmd_date,
    "help": cmd_help,
    "history": cmd_history,
}

__all__ = ["REGISTRY", "CommandError"]
