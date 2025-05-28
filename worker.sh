#!/bin/bash

echo "JOB STARTED ||||||||||||||||||||"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_now=$(date +"%Y%m%d-%H%M%S%z")
_logs_dir="$SCRIPT_DIR/logs"
_logs_file="$_logs_dir/browser.log"
_crony_dir="$SCRIPT_DIR/crony"
_lock_file="$_crony_dir/.lock"

if ! [ -d "$_crony_dir" ]; then
    mkdir -p $_crony_dir
fi

if ! test -e "$_logs_file"; then
    mkdir -p $_logs_dir && touch $_logs_file
fi

if test -e "$_lock_file"; then
    echo "Execution prevented by a Lock file: $_lock_file"
    echo "Another script is probably running or did not finish as expected."
    echo "The lock file will be removed on next boot. It can also be removed manually."
else
    touch $_lock_file
    $SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/app/worker.py "$@" >> "$_logs_file"
    echo "Script finished executing. See logs and system journal for details."
    if test -e "$_lock_file"; then
        echo "Trying to remove Lock file after script finished."
        rm -f -- $_lock_file
    fi
fi


echo "|||||||||||||||||||| JOB FINISHED"
