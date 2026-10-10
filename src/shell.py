import getpass
import platform

from commands import REGISTRY, CommandError


class Pandi:
    def __init__(self, vfs_path=None, script_path=None):
        self._username = getpass.getuser()
        self._hostname = platform.node()
        self._vfs_path = vfs_path
        self._script_path = script_path
        self._vfs = None
        self._is_enable = False

    def start(self):
        self._debug_dump_config()
        if not self._load_vfs():
            self.output("Session terminated.")
            return 1
        self._print_motd()
        self._is_enable = True
        try:
            if self._script_path is not None:
                from script import run_script

                if not run_script(self, self._script_path):
                    self.stop()
                    return 1
            if self._is_enable:
                self._loop()
        except KeyboardInterrupt:
            self.output("")
        finally:
            self.output("Session terminated.")
        return 0

    def stop(self):
        self._is_enable = False

    def _debug_dump_config(self):
        self.output("[pandi] --- startup configuration ---")
        self.output(f"[pandi] vfs_path    = {self._vfs_path!r}")
        self.output(
            f"[pandi] script_path = {self._script_path!r}"
        )
        self.output(f"[pandi] username    = {self._username!r}")
        self.output(f"[pandi] hostname    = {self._hostname!r}")
        self.output("[pandi] -------------------------------")

    def _load_vfs(self):
        if self._vfs_path is None:
            return True
        try:
            from vfs import load_vfs

            self._vfs = load_vfs(self._vfs_path)
        except Exception as exc:
            self.output(str(exc))
            return False
        return True

    def _print_motd(self):
        if self._vfs is None:
            return
        from vfs import get_motd

        motd = get_motd(self._vfs)
        if motd is not None:
            for line in motd.splitlines():
                self.output(line)

    def _command_manager(self, tokens):
        cmd, *args = tokens
        handler = REGISTRY.get(cmd)
        if handler is None:
            raise CommandError(f"{cmd}: command not found")
        return handler(args)

    def command_manager(self, tokens):
        return self._command_manager(tokens)

    def _parser(self, raw):
        return raw.split()

    def parser(self, raw):
        return self._parser(raw)

    def _prompt(self):
        return f"{self._username}@{self._hostname}:~$ "

    def prompt(self):
        return self._prompt()

    def _input(self):
        return input(self.prompt())

    def output(self, text):
        print(text)

    def _output(self, text):
        self.output(text)

    def _loop(self):
        while self._is_enable:
            try:
                raw = self._input()
            except EOFError:
                self.output("")
                self.stop()
                return
            except KeyboardInterrupt:
                self.output("^C")
                continue

            if not raw.strip():
                continue

            tokens = self.parser(raw)

            if tokens[0] == "exit":
                self.stop()
                return

            try:
                self.output(self.command_manager(tokens))
            except CommandError as exc:
                self.output(str(exc))
