#!/bin/bash


PYTHON_SCRIPT="src/main.py"

start_script() {
    echo "Starting Python script..."
    nohup sudo python "$PYTHON_SCRIPT"
    echo $! > "$TARGET_DIR/script.pid"
}

if [ -f "$TARGET_DIR/script.pid" ]; then
    PID=$(cat "$TARGET_DIR/script.pid")
    if ! ps -p $PID > /dev/null; then
        echo "Python script is not running. Restarting..."
        start_script
    else
        echo "Python script is already running."
    fi
else
    start_script
fi