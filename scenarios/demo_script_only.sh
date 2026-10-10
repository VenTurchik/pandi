#!/bin/bash
# Запуск только с --script: исполняем «хороший» сценарий.
set -e
cd "$(dirname "$0")/.."
./run.sh --script scripts/01_ok.pandi
