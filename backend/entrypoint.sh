#!/bin/bash
set -e

source $(poetry env info -p)/bin/activate

exec "$@"
