#!/bin/bash
cd "$(dirname "$0")/.."
echo "not a zip" > /tmp/pandi_bad.zip
./run.sh --vfs /tmp/pandi_bad.zip --script scripts/04_vfs_ok.pandi
rc=$?
echo "[scenario] exit code: $rc"
rm -f /tmp/pandi_bad.zip
