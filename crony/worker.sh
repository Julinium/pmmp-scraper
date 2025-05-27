#!/bin/bash

echo "JOB STARTED ||||||||||||||||||||"

_now=$(date +"%Y%m%d-%H%M%S%z")
_log='/var/opt/seleno/logs/browser.log'
_lok='/var/opt/seleno/crony/.lock'

if test -e "$_lok"; then
    echo "Execution prevented by a Lock file: $_lok"
    echo "Another script is probably running or did not finish as expected."
    echo "The lock file will be removed on next boot. It can also be removed manually."
else
    touch $_lok
    /opt/seleno/.venv/bin/python /var/opt/seleno/worker.py "$@" >> "$_log"
    echo "Script finished executing. See logs and system journal for details."
    if test -e "$_lok"; then
        echo "Trying to remove Lock file after script finished."
        rm -f -- $_lok
    fi
fi

echo "|||||||||||||||||||| JOB FINISHED"
