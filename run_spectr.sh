#!/bin/bash
cd "$(dirname "$0")"
echo "=== Starting SPECTR Tactical Machine v2.3 ==="
python3 -m src.spectr.main
