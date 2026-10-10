#!/bin/bash
# Этап 5: демонстрация cp и help поверх deep.zip.
set -e
cd "$(dirname "$0")/.."

echo "=== deep.zip + 06_extra_ok.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/06_extra_ok.pandi

echo
echo "=== deep.zip + 06_extra_err_nosrc.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/06_extra_err_nosrc.pandi || \
  echo "[scenario] expected error (no such source)"

echo
echo "=== deep.zip + 06_extra_err_isdir.pandi ==="
./run.sh --vfs vfs/deep.zip --script scripts/06_extra_err_isdir.pandi || \
  echo "[scenario] expected error (cp of directory)"
