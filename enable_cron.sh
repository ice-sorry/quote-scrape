#!/bin/bash

SCRIPT_PATH=/home/ec2-user/quote-scrape/main.py
PYTHON_PATH=$(which python3)

CRON_SCHEDULE="0 8 * * 1" 
CRON_LINE="$CRON_SCHEDULE $PYTHON_PATH $SCRIPT_PATH >> ${SCRIPT_PATH}.log 2>&1"

(crontab -l 2>/dev/null | grep -Fv "$SCRIPT_PATH"; echo "$CRON_LINE") | crontab -

echo "✅ Crontab created for $SCRIPT_PATH"
echo "Current crontab:"
crontab -l