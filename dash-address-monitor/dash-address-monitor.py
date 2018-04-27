from coin_rpc_class import RPCHost
from keybase import Keybase

from pprint import pprint
import requests

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

    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        print('{} {}'.format(response.status_code, response.text)) #, contents.json()))
        return response.text
    else:
        response.raise_for_status()
        #throw 'Invalid response: {}'.format(response.status_code)

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
