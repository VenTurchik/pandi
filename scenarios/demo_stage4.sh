#!/bin/bash
# Этап 4: демонстрация ls/cd/date/history на разных VFS.
set -e
cd "$(dirname "$0")/.."

echo "=== deep.zip + 05_main_ok.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/05_main_ok.pandi

echo
echo "=== deep.zip + 05_main_err_nopath.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/05_main_err_nopath.pandi || \
  echo "[scenario] expected error (no such path)"

echo
echo "=== deep.zip + 05_main_err_notdir.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/05_main_err_notdir.pandi || \
  echo "[scenario] expected error (not a directory)"

echo
echo "=== minimal.zip + 05_main_ok.pandi ==="
./run.sh --vfs vfs/minimal.zip --script scripts/05_main_ok.pandi || \
  echo "[scenario] minimal has no /a — ошибка ожидаема"

echo
echo "=== few.zip + 05_main_ok.pandi ==="
./run.sh --vfs vfs/few.zip --script scripts/05_main_ok.pandi || \
  echo "[scenario] few has no /a — ошибка ожидаема"
