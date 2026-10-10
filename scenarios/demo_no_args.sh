#!/bin/bash
# Запуск эмулятора без параметров CLI.
# Чтобы не висеть в интерактиве, передаём stdin: одна команда и exit.
set -e
cd "$(dirname "$0")/.."
printf 'ls\nexit\n' | ./run.sh
