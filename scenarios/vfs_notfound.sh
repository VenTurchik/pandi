#!/bin/bash
cd "$(dirname "$0")/.."
./run.sh --vfs /no/such/file.zip --script scripts/04_vfs_ok.pandi
rc=$?
echo "[scenario] exit code: $rc"
