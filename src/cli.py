import argparse


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="pandi",
        description="Эмулятор оболочки UNIX-подоб. ОС.",
    )
    parser.add_argument(
        "--vfs",
        dest="vfs_path",
        default=None,
        help="Путь к VFS (этап 3). На этапе 2 "
        "только показывается в отладке.",
    )
    parser.add_argument(
        "--script",
        dest="script_path",
        default=None,
        help="Путь к стартовому скрипту. "
        "Останавливается при ошибке.",
    )
    return parser
