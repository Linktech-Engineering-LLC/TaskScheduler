#!/bin/bash
set -e

PROJECT_DIR="$HOME/projects/Python/TaskScheduler"
VENV_DIR="$HOME/.venv"

# Activate venv
source "$VENV_DIR/bin/activate"

# Move into project
cd "$PROJECT_DIR"

# Launch TimerDeck
exec python -m TaskScheduler
