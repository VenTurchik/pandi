from commands import CommandError


def run_script(shell, path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as exc:
        shell.output(f"pandi: cannot open script {path!r}: {exc}")
        return False

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        shell.output(f"{shell.prompt()}{stripped}")

        tokens = shell.parser(stripped)

        if tokens[0] == "exit":
            shell.stop()
            return True

        try:
            shell.output(shell.command_manager(tokens))
        except CommandError as exc:
            shell.output(str(exc))
            shell.output(
                f"pandi: script {path!r} stopped at line {lineno}"
            )
            return False

    return True
