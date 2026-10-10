import zipfile


class VfsError(Exception):
    pass


def _add_path(root, path, data):
    parts = [p for p in path.split("/") if p]
    cur = root
    for part in parts[:-1]:
        nxt = cur["children"].get(part)
        if nxt is None:
            nxt = {"__dir": True, "children": {}}
            cur["children"][part] = nxt
        cur = nxt
    last = parts[-1] if parts else ""
    if not last:
        return
    if data is None:
        if last not in cur["children"]:
            cur["children"][last] = {
                "__dir": True,
                "children": {},
            }
    else:
        cur["children"][last] = {
            "__dir": False,
            "data": data,
        }


def load_vfs(path):
    try:
        zf = zipfile.ZipFile(path, "r")
    except FileNotFoundError:
        raise VfsError(
            f"pandi: cannot load vfs {path!r}: no such file"
        )
    except IsADirectoryError:
        raise VfsError(
            f"pandi: cannot load vfs {path!r}: is a directory"
        )
    except zipfile.BadZipFile as exc:
        raise VfsError(
            f"pandi: cannot load vfs {path!r}: "
            f"bad zip format: {exc}"
        )
    except OSError as exc:
        raise VfsError(
            f"pandi: cannot load vfs {path!r}: {exc}"
        )

    root = {"__dir": True, "children": {}}

    try:
        for info in zf.infolist():
            name = info.filename
            if name.startswith("/") or ".." in name:
                continue
            if name.endswith("/"):
                _add_path(root, name, None)
            else:
                data = zf.read(name)
                _add_path(root, name, data)
    finally:
        zf.close()

    return root


def get_motd(vfs):
    node = vfs["children"].get("motd")
    if node is None or node["__dir"]:
        return None
    return node["data"].decode("utf-8", errors="replace")
