#!/bin/bash
set -e
cd "$(dirname "$0")/.."
./run.sh --vfs vfs/few.zip --script scripts/04_vfs_ok.pandi
