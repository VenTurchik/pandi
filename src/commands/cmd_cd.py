from commands.errors import CommandError


def cmd_cd(args, shell=None):
    if shell is None or getattr(shell, "_vfs", None) is None:
        if not args:
            return "cd"
        return f"cd {' '.join(args)}"
    from vfs import get_node, resolve

    if not args:
        shell._cwd = "/"
        return ""
    target = args[0]
    abspath = resolve(shell._cwd, target)
    node = get_node(shell._vfs, abspath)
    if node is None:
        raise CommandError(
            f"cd: {target}: No such file or directory"
        )
    if not node["__dir"]:
        raise CommandError(f"cd: {target}: Not a directory")
    shell._cwd = abspath
    return ""
