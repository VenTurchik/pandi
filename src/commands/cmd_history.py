def cmd_history(args, shell=None):
    if shell is None or not getattr(shell, "_history", None):
        return ""
    lines = []
    for idx, entry in enumerate(shell._history, start=1):
        lines.append(f"{idx:4d}  {entry}")
    return "\n".join(lines)
