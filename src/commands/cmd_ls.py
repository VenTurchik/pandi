from commands.errors import CommandError


def cmd_ls(args, shell=None):
    if shell is None or getattr(shell, "_vfs", None) is None:
        if not args:
            return "ls"
        return f"ls {' '.join(args)}"
    from vfs import get_node, resolve

    target = None
    for a in args:
        if not a.startswith("-"):
            target = a
            break
    if target is None:
        abspath = shell._cwd
        disp = target
    else:
        abspath = resolve(shell._cwd, target)
        disp = target
    node = get_node(shell._vfs, abspath)
    if node is None:
        name = disp if disp is not None else abspath
        raise CommandError(
            f"ls: cannot access '{name}': "
            "No such file or directory"
        )
    if not node["__dir"]:
        return abspath.rsplit("/", 1)[-1]
    items = sorted(node["children"].keys())
    return "\n".join(items)
