#!/bin/bash

SCRIPT_PATH=/home/ec2-user/quote-scrape/main.py
crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH" | crontab -

echo "Crontab entry for $SCRIPT_NAME has been removed."
echo "Current crontab:"
crontab -l