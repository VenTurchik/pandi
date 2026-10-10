import sys

from cli import build_arg_parser
from shell import Pandi


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    app = Pandi(vfs_path=args.vfs_path, script_path=args.script_path)
    return app.start()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
