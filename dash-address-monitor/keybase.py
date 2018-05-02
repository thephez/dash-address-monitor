import json
import subprocess


class Keybase(object):

    # Keybase Chat API
    # ----------------
    #NAME:
    #   keybase chat api - JSON api
    #
    #USAGE:
    #   keybase chat api [command options]
    #
    #DESCRIPTION:
    #   "keybase chat api" provides a JSON API to the Keybase chat service.
    #
    # OPTIONS:
    #    -p, --pretty		Output pretty (indented) JSON.
    #    -m 			Specify JSON as string instead of stdin
    #    -i, --infile 	Specify JSON input file (stdin default)
    #    -o, --outfile 	Specify output file (stdout default)

    def __init__(self):
        self.CHATCMD = 'keybase chat api'

    def sendTeamMessage(self, teamName, teamChannel, message):
        msg = None

        apiMsg = {}
        apiMsg['method'] = 'send'
        apiMsg['params'] = {}
        apiMsg['params']['options'] = {}
        apiMsg['params']['options']['channel'] = {}
        apiMsg['params']['options']['channel']['name'] = teamName
        apiMsg['params']['options']['channel']['members_type'] = 'team'
        apiMsg['params']['options']['channel']['topic_name'] = teamChannel
        apiMsg['params']['options']['message'] = {}
        apiMsg['params']['options']['message']['body'] = message
        #print(apiMsg)

        jsonData = json.dumps(apiMsg)
        subprocess.call('keybase status', shell=True)
        # Run command
        osCommand = "{} -m '{}'".format(self.CHATCMD, jsonData)

        try:
            exitcode = subprocess.call(osCommand, shell=True)

            if exitcode == 0:
                msg = 'Command completed successfully (return code = {}) - "{}"'.format(osCommand, exitcode)
            else:
                msg = 'Command failed (return code = {}) - "{}".'.format(exitcode, osCommand)
        except Exception as e:
            print(e)
            raise

        print(msg)
        return
