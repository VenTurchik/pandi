#!/bin/bash
# Запуск на несуществующем пути — проверяем обработку ошибки.
cd "$(dirname "$0")/.."
out=$(./run.sh --script /nonexistent/file.pandi 2>&1)
echo "$out"
if echo "$out" | grep -qi "cannot open script\|no such file"; then
  echo "[scenario] correctly reported missing script"
else
  echo "[scenario] WARNING: message not found" >&2
fi
