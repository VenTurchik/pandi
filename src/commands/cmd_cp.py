from commands.errors import CommandError


def cmd_cp(args, shell=None):
    if shell is None or getattr(shell, "_vfs", None) is None:
        if not args:
            return "cp"
        return f"cp {' '.join(args)}"
    from vfs import get_node, resolve

    if len(args) < 2:
        raise CommandError("cp: missing file operand")
    if len(args) > 2:
        raise CommandError(f"cp: extra operand '{args[2]}'")
    src_arg, dst_arg = args[0], args[1]
    src_abs = resolve(shell._cwd, src_arg)
    dst_abs = resolve(shell._cwd, dst_arg)
    src_node = get_node(shell._vfs, src_abs)
    if src_node is None:
        raise CommandError(
            f"cp: cannot stat '{src_arg}': "
            "No such file or directory"
        )
    if src_node["__dir"]:
        raise CommandError(
            f"cp: -r not specified; omitting "
            f"directory '{src_arg}'"
        )
    dst_node = get_node(shell._vfs, dst_abs)
    if dst_node is not None and dst_node["__dir"]:
        parent = dst_node
        name = src_abs.rsplit("/", 1)[-1]
        parent["children"][name] = {
            "__dir": False,
            "data": bytes(src_node["data"]),
        }
        return ""
    if dst_node is not None and not dst_node["__dir"]:
        parent_path = dst_abs.rsplit("/", 1)[0]
        if not parent_path:
            parent_path = "/"
        parent = get_node(shell._vfs, parent_path)
        name = dst_abs.rsplit("/", 1)[-1]
        parent["children"][name] = {
            "__dir": False,
            "data": bytes(src_node["data"]),
        }
        return ""
    parent_path = dst_abs.rsplit("/", 1)[0]
    if not parent_path:
        parent_path = "/"
    name = dst_abs.rsplit("/", 1)[-1]
    parent = get_node(shell._vfs, parent_path)
    if parent is None or not parent["__dir"]:
        raise CommandError(
            f"cp: cannot create '{dst_arg}': "
            "No such file or directory"
        )
    parent["children"][name] = {
        "__dir": False,
        "data": bytes(src_node["data"]),
    }
    return ""
