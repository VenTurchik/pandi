def cmd_ls(args: list[str]) -> str:
    if not args:
        return "ls"
    return f"ls {' '.join(args)}"