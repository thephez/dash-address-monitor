from coin_rpc_class import RPCHost
from keybase import Keybase

from pprint import pprint
import time, requests

#from blockcypher import get_address_details
#from blockcypher import get_address_full
from blockcypher import get_address_overview

#https://insight.dashevo.org/insight-api-dash/addr/Xoyn4Xxugx5K6HAog7vzxb6Hf3SW586Zfc/balance

RPCPORT = 19998
RPCUSER = 'user'
RPCPASS = 'pass'
COIN = 100000000

addr = ['yY6AmGopsZS31wy1JLHR9P6AC6owFaXwuh']

def pollAddresses(): #host):
    balance = None
    prevBalance = 1000000000000.0

    for a in addr:
        print('Address: {}'.format(a))

        try:
            #info = host.call('getaddressbalance', a)
            balance = float(getBalanceInsight(a))
            #balance = getBalanceBlockcypher(a)

            print('Balance: {} DASH'.format(float(balance)/COIN))
        except Exception as e:
            print('Exception getting balance: {}'.format(e))
            return

        # Compare with previous (if found)
        if (balance != prevBalance):
            # Store new Balance
            balanceChange = balance - prevBalance

            # Send notification
            kb = Keybase()
            notifyMessage = 'Balance change:\n\t`{}`\n\t\tPrevious Balance: {}DASH\n\t\tNew Balance: {} DASH\n\t\tChange of: {} DASH'.format(a, float(prevBalance)/COIN, float(balance)/COIN, balanceChange/COIN)
            kb.sendTeamMessage('phez', 'notifications', notifyMessage)

def getBalanceInsight(address):
    apiUrlBase = "https://testnet-insight.dashevo.org/insight-api-dash/addr/"
    apiUrlSuffix = "/balance"
    url = '{}{}{}'.format(apiUrlBase, address, apiUrlSuffix)

    tries = 5
    hadConnectionFailures = False
    while True:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            tries -= 1
            if tries == 0:
                raise Exception('Failed to connect to Insight API at {} for balance check.'.format(apiUrlBase))
            hadFailedConnections = True
            print("Couldn't connect for balance check, will sleep for five seconds and then try again ({} more tries)".format(tries))
            time.sleep(5)
        else:
            if (response.status_code == 400):
                tries -= 1
                print('Insight-Api request failure: {} {}. Retrying {} more times...'.format(response.status_code, response.reason, tries))
                time.sleep(1)
                continue

            if hadConnectionFailures:
                print('Connected after retry.')

            break

    if not response.status_code in (200, 500):
        raise Exception('Insight-API connection failure: ' + str(response.status_code) + ' ' + response.reason)

    if (response.text.isdigit() != True):
        raise Exception('Insight-API: Non-numeric balance returned')

    print('Completed with {} tries remaining'.format(tries))

    #if response.status_code == requests.codes.ok:
    #    print('{} {}'.format(response.status_code, response.text)) #, contents.json()))
    #    return response.text
    #else:
    #    response.raise_for_status()
    #    #throw 'Invalid response: {}'.format(response.status_code)

    return response.text

def getBalanceBlockcypher(address):

    # Only works for mainnet addresses
    info = get_address_overview(address, 'dash')
    print('Balance: {}'.format(info['final_balance']))

def rpcTest(host):

    #block = host.call('getblock', hash)
    #coin = block['tx'][0]
    #test = host.call('listreceivedbyaddress', 0, True)
    #pprint(test)

    getinfo = host.call('getinfo')
    print('Current block height: {}'.format(getinfo['blocks']))

    #try:
    #    balance = host.call('getaddressbalance', 'yY6AmGopsZS31wy1JLHR9P6AC6owFaXwuh')
    #    pprint(balance)
    #except Exception as e:
    #    print(e)

def getRpcHost(rpcPort, rpcUser, rpcPassword):
    # Accessing the RPC local server
    serverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

    # Using the class defined in the dash_rpc_class.py
    host = RPCHost(serverURL)

    return host

def main():

    pollAddresses()

    #host = getRpcHost(RPCPORT, RPCUSER, RPCPASS)

    #if (host.isResponding()):
    #    #print(host.call('getinfo'))
    #    rpcTest(host)

    #    pollAddresses(host)
    #else:
    #    print('Host not responding')

if __name__ == '__main__':
    main()


#    from blockcypher import get_address_overview
#    print(get_address_overview('Xico5nigvR8Kk2PQZuthSb5dETUf5oAj8g', 'dash')['balance'])
