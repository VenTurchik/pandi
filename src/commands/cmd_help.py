DESCR = {
    "cd": "change directory",
    "cp": "copy files",
    "date": "print current date and time",
    "exit": "exit shell",
    "help": "show this help",
    "history": "show command history",
    "ls": "list directory contents",
}


def cmd_help(args, shell=None):
    lines = []
    for name in sorted(DESCR.keys()):
        lines.append(f"{name:10s} - {DESCR[name]}")
    return "\n".join(lines)
