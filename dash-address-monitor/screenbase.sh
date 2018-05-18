#!/bin/bash
# Thanks to moocowmoo (https://github.com/moocowmoo) for creating this script
# Add this script to your cron to make sure the screen is preset

# Set this to match the Screen name defined in the python project
SCREEN_NAMESPACE=kbscreen

# Don't modify
KEYBASE_BIN=$(which keybase)
SCREEN_BIN=$(which screen)
CR=$(echo -e "\015")
SCREEN_STATE=-1

echo "Last run: $(date)"

function screenspace(){
    $SCREEN_BIN -q -ls $SCREEN_NAMESPACE ;
    SCREEN_STATE=$(( $? - 10 ));
    if [[ SCREEN_STATE -eq 1 ]]; then
        # echo "screen running"
        return 0 # good condition, return logical true
    elif [[ SCREEN_STATE -lt 1 ]]; then
        # echo "screen down, spinning up fresh"
        $SCREEN_BIN -d -m -S $SCREEN_NAMESPACE -s /bin/bash
        $SCREEN_BIN -S $SCREEN_NAMESPACE -p 0 -X stuff "export XDG_RUNTIME_DIR=/run/user/$UID$CR"
        mkdir -p $HOME/bin $HOME/tmp
        return 0 # good condition, return logical true
    else
        # won't get here until we do, patch accordingly
        echo "multiple screens running - confoozed, halp!"
        return 1 # fail condition, return logical false
    fi ;

}

screenspace