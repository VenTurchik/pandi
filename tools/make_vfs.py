import os
import zipfile


def make_minimal():
    with zipfile.ZipFile("vfs/minimal.zip", "w") as zf:
        zf.writestr("hello.txt", "hello\n")


def make_few():
    with zipfile.ZipFile("vfs/few.zip", "w") as zf:
        zf.writestr("a.txt", "a\n")
        zf.writestr("b.txt", "b\n")
        zf.writestr("docs/readme.txt", "inside docs\n")
        zf.writestr("docs/nested.txt", "nested\n")


def make_deep():
    with zipfile.ZipFile("vfs/deep.zip", "w") as zf:
        zf.writestr("motd", "Welcome to pandi deep VFS!\n")
        zf.writestr("a/b/c/file.txt", "deep file\n")
        zf.writestr("a/b/c/other.txt", "other deep\n")
        zf.writestr("a/b/other.txt", "other\n")
        zf.writestr("a/top.txt", "top\n")


def make_motd():
    with zipfile.ZipFile("vfs/motd.zip", "w") as zf:
        zf.writestr("motd", "Hello from pandi!\n")
        zf.writestr("readme.txt", "with motd\n")


if __name__ == "__main__":
    os.makedirs("vfs", exist_ok=True)
    make_minimal()
    make_few()
    make_deep()
    make_motd()
    print("vfs/*.zip created")
