import getpass
import platform
import sys

from commands import REGISTRY

class Pandi:
    def __init__(self) -> None:
        self._username = getpass.getuser()
        self._hostname = platform.node()
        self._is_enable = False

    def start(self) -> int:
        self._is_enable = True
        try:
            self._loop()
        except KeyboardInterrupt:
            self._output("")
        finally:
            self._output("Session terminated.")
        return 0

    def stop(self) -> None:
        self._is_enable = False

    def _command_manager(self, tokens: list[str]) -> str:
        cmd, *args = tokens
        handler = REGISTRY.get(cmd)
        if handler is None:
            return f"{cmd}: command not found"
        return handler(args)
        
    def _parser(self, raw: str) -> list[str]:
        return raw.split()

    def _input(self) -> str:
        return input(f"{self._username}@{self._hostname}:~$ ")

    def _output(self, text: str) -> None:
        print(text)

    def _loop(self) -> None:
        while self._is_enable:
            try:
                raw = self._input()
            except EOFError:
                self._output("")
                self.stop()
                return
            except KeyboardInterrupt:
                self._output("^C")
                continue

            if not raw.strip():
                continue

            tokens = self._parser(raw)

            if tokens[0] == "exit":
                self.stop()
                return

            self._output(self._command_manager(tokens))

def main() -> int:
    app = Pandi()
    return app.start()

if __name__ == "__main__":
    sys.exit(main())