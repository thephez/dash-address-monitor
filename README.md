# Dash Address monitor

## Overview

Monitor a list of Dash addresses for balance changes and send a Keybase chat notification on change.

NOTE: This is designed to work with a Keybase team.

## Configuration

### dash-address-monitor.conf

Define the Keybase `team` and `channel` notification destination. Also, define
the name of the screen (created via the Linux `screen` command) receiving the
keybase commands.

### Linux `screen`

Set up a cron to call `screenbase.sh`. This script will handle setup of the
`screen` and restart it if it fails.

### Example cron setup
```
* * * * * /home/user/dash-address-monitor/dash-address-monitor/screenbase.sh > /home/user/cron_screenbase.txt 2>&1
* * * * * /usr/bin/python3 /home/user/dash-address-monitor/dash-address-monitor/dash-address-monitor.py > /home/user/cron_keybase.txt 2>&1
```

### Example config file
```
# File to load address list from
address_file=addresses.txt

# File to store balance info
db_name=balances.dat

# Keybase config
keybase_team=myteam
keybase_channel=notifications
keybase_screen=kbscreen
```
