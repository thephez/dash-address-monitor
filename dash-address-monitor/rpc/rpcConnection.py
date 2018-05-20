import time, requests, json

# ----------------------------------------------------
# From https://gist.github.com/Deadlyelder/6baad86e832acf0df23a70914c014d7a#file-bitcoin_rpc_class-py

class RPCHost(object):

    MAINNET_RPC_PORT = 9998
    TESTNET_RPC_PORT = 19998

    def __init__(self, rpcUser, rpcPassword, rpcPort=9998):
        self._session = requests.Session()
        self._url = 'http://{}:{}@localhost:{}'.format(rpcUser, rpcPassword, rpcPort)
        self._headers = {'content-type': 'application/json'}

    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print("Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']

# ----------------------------------------------------

    def isResponding(self):
        try:
            self.call('getinfo')
            return True
        except Exception as e:
            print(e)
            return False

    def rpcTest(self):

        getinfo = self.call('getinfo')
        print('Current block height: {}'.format(getinfo['blocks']))

        #try:
        #    balance = host.call('getaddressbalance', 'yY6AmGopsZS31wy1JLHR9P6AC6owFaXwuh')
        #    pprint(balance)
        #except Exception as e:
        #    print(e)
