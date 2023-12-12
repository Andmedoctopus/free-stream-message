#!/bin/bash
set -e

echo $(poetry config --list)
echo $(poetry env info -p)
source $(poetry env info -p)/bin/activate

echo $(which python)
exec "$@"
