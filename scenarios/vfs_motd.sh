#!/bin/bash
set -e
cd "$(dirname "$0")/.."
printf 'exit\n' | ./run.sh --vfs vfs/motd.zip
