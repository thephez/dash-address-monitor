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
ADDRESS_FILE = 'addresses.txt'

def pollAddresses(rpcConn, addresses):
    db = 'balances.dat'

    for addr in addresses:
        netType = None
        balance = None

        netType = getNetType(addr)
        print('Network: {}, Address: "{}"'.format(netType, addr))

        try:
            balance = apis.coreRpcClient.getBalance(rpcConn[netType], addr)
            print('Balance: {} DASH'.format(float(balance)/COIN))
        except Exception as e:
            print('Exception getting balance: {}. Exiting'.format(e))
            continue

        # Compare with previous (if found)
        prevBalance = getBalance(db, addr)
        if (balance != prevBalance):
            balanceChange = balance - prevBalance

            # Store new Balance
            storeBalance(db, addr, balance)

            # Send notification
            kb = Keybase()
            notifyMessage = 'Balance change ({}):\n\t\`{}\`\n    Previous Balance: {}DASH\n    New Balance: {} DASH\n    Change of: {} DASH'.format(datetime.now(), addr, float(prevBalance)/COIN, float(balance)/COIN, balanceChange/COIN)
            kb.sendTeamMessage('phez', 'notifications', notifyMessage, 'kbscreen')
        else:
            print('No balance change for `{}`'.format(addr))

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

def isValidAddress(address):

    # Empty address
    if (address == ''):
        return False

    # List of valid address start characters
    startChars = ['X', 'y']
    if (address[0] not in startChars):
        return False

    # Invalid Base-58 characters
    invalidChars = ['0', 'I', '0', 'l']
    if any(char in address for char in invalidChars):
        return False

    return True

def getUsedNetworks(addresses):

    networks = set()

    # Get types of addresses used
    for addr in addresses:
        netType = getNetType(addr)
        networks.add(netType)

    return networks

def loadAddressFile(fname):
    # Create set containing only unique, valid Addresses
    validAddresses = set()

    with open(fname) as f:
        data = f.readlines()

        for line in data:
            addr = line.strip()
            if (isValidAddress(addr)):
                validAddresses.add(addr)
                print(validAddresses)
            else:
                print('Skipping invalid address: {}'.format(addr))

    print('{} valid addresses found'.format(len(validAddresses)))
    return validAddresses

def main():

    # Get valid addresses and deterine networks used (Main and/or Test)
    addresses = loadAddressFile(ADDRESS_FILE)
    networks = getUsedNetworks(addresses)
    print('Addresses found on {} network(s)'.format(networks))

    # Establish connections to used network(s)
    rpcConnections = {}
    for network in networks:
        if (network == 'MAIN'):
            rpcConnections[network] = RPCHost(RPCUSER, RPCPASS, RPCHost.MAINNET_RPC_PORT)
        elif (network == 'TEST'):
            rpcConnections[network] = RPCHost(RPCUSER, RPCPASS, RPCHost.TESTNET_RPC_PORT)

    print(rpcConnections)

    pollAddresses(rpcConnections, addresses)

if __name__ == '__main__':
    main()
