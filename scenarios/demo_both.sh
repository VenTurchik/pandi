#!/bin/bash
# Запуск с обоими параметрами: --vfs и --script.
# Используем сценарий с комментариями, чтобы заодно проверить их обработку.
set -e
cd "$(dirname "$0")/.."
./run.sh --vfs ./vfs/example.zip --script scripts/03_comments.pandi
