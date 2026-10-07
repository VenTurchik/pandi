def cmd_cd(args: list[str]) -> str:
    if not args:
        return "cd"
    return f"cd {' '.join(args)}"