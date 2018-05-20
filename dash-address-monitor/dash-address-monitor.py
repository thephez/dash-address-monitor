from rpc.rpcConnection import RPCHost
from keybase.keybaseClient import Keybase
from datetime import datetime

from pprint import pprint
import shelve

import apis.coreRpcClient
import apis.blockcypherClient
import apis.insightClient

RPCUSER = 'user'
RPCPASS = 'pass'
COIN = 100000000

addr = ['yY6AmGopsZS31wy1JLHR9P6AC6owFaXwuh',
        ''
        'XcbfassQgqwn3oREckfjMASWg7Bsuwd3st',
        'msdlkafj'
        ]

def pollAddresses(host): #host):
    db = 'balances.dat'

    for a in addr:
        netType = None
        balance = None

        if (a == ''):
            continue

        try:
            netType = getNetType(a)
        except:
            continue

        print('Network: {}, Address: "{}"'.format(netType, a))

        try:
            if (netType == 'MAIN'):
                balance = float(apis.insightClient.getBalance(a))
                #balance = apis.blockcypherClient.getBalance(a)

            elif (netType == 'TEST'):
                balance = apis.coreRpcClient.getBalance(host, a)

            print('Balance: {} DASH'.format(float(balance)/COIN))
        except Exception as e:
            print('Exception getting balance: {}. Exiting'.format(e))
            continue

        # Compare with previous (if found)
        prevBalance = getBalance(db, a)
        if (balance != prevBalance):
            balanceChange = balance - prevBalance

            # Store new Balance
            storeBalance(db, a, balance)

            # Send notification
            kb = Keybase()
            notifyMessage = 'Balance change ({}):\n\t\`{}\`\n    Previous Balance: {}DASH\n    New Balance: {} DASH\n    Change of: {} DASH'.format(datetime.now(), a, float(prevBalance)/COIN, float(balance)/COIN, balanceChange/COIN)
            kb.sendTeamMessage('phez', 'notifications', notifyMessage, 'kbscreen')
        else:
            print('No balance change for `{}`'.format(a))

def storeBalance(db, address, balance):
    d = shelve.open(db)
    d[address] = balance
    d.close()

    return

def getBalance(db, address):

    d = shelve.open(db)
    if address in d:
        balance = d[address]
    else:
        print('Address not found in database. Using 0.0')
        balance = 0.0

    d.close()

    return balance

def getNetType(address):
    # Determine if the address belongs to Mainnet or Testnet

    if (address[0] == 'X'):
        return 'MAIN'
    elif (address[0] == 'y'):
        return 'TEST'
    else:
        raise ValueError('Address type unknown')

def main():

    #pollAddresses()

    host = RPCHost(RPCUSER, RPCPASS, RPCHost.TESTNET_RPC_PORT)

    if (host.isResponding()):
        #host.rpcTest()
        pollAddresses(host)
    else:
        print('Host not responding')

if __name__ == '__main__':
    main()
