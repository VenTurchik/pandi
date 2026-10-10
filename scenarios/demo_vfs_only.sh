#!/bin/bash
# Запуск только с --vfs: проверяем, что путь к VFS отображается
# в отладочном выводе. Через stdin сразу завершаем сессию.
set -e
cd "$(dirname "$0")/.."
printf 'exit\n' | ./run.sh --vfs ./vfs/example.zip
