import sys
import os

from rpc.rpcConnection import RPCHost
from keybase.keybaseClient import Keybase
from datetime import datetime

from pprint import pprint
import shelve
from base58 import b58decode_check

import apis.coreRpcClient
import apis.blockcypherClient
import apis.insightClient

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), './lib')))
import config
from dash_config import DashConfig

COIN = 100000000
DBFILE = config.db_name
KEYBASE_PARAMS = config.keybase_params


def poll_addresses(rpc_connections, addresses):
    db = DBFILE

    for addr in addresses:
        network_type = None
        balance = None

        network_type = get_network_type(addr)
        print('Network: {}, Address: "{}"'.format(network_type, addr))

        try:
            balance = apis.coreRpcClient.get_balance(rpc_connections[network_type], addr)
            print('Balance: {} DASH'.format(float(balance)/COIN))
        except Exception as e:
            print('Exception getting balance: {}. Exiting'.format(e))
            continue

        # Compare with previous (if found)
        last_balance = get_balance(db, addr)
        if (balance != last_balance):
            balance_change = balance - last_balance

            # Store new Balance
            store_balance(db, addr, balance)

            # Send notification
            kb = Keybase()
            notify_msg = 'Balance change ({}):\n\t\`{}\`\n    Previous Balance: {}DASH\n    New Balance: {} DASH\n    Change of: {} DASH'.format(datetime.now(), addr, float(last_balance)/COIN, float(balance)/COIN, balance_change/COIN)
            kb.send_team_msg(KEYBASE_PARAMS['team'], KEYBASE_PARAMS['channel'], notify_msg, KEYBASE_PARAMS['screen'])
        else:
            print('No balance change for `{}`'.format(addr))


def store_balance(db, address, balance):
    d = shelve.open(db)
    d[address] = balance
    d.close()

    return


def get_balance(db, address):

    d = shelve.open(db)
    if address in d:
        balance = d[address]
    else:
        print('Address not found in database. Using 0.0')
        balance = 0.0

    d.close()

    return balance


def get_network_type(address):
    # Determine if the address belongs to Mainnet or Testnet

    if (address[0] == 'X') or (address[0] == '7'):
        return 'mainnet'
    elif (address[0] == 'y') or (address[0] == '8') or (address[0] == '9'):
        return 'testnet'
    else:
        raise ValueError('Address type unknown')


def is_valid_address(address):

    try:
        b58decode_check(address)
        return True
    except ValueError:
        return False
    return None


def get_used_networks(addresses):

    networks = set()

    # Get types of addresses used
    for addr in addresses:
        network_type = get_network_type(addr)
        networks.add(network_type)

    return networks


def load_address_file(fname):
    # Create set containing only unique, valid Addresses
    valid_addresses = set()

    with open(fname) as f:
        data = f.readlines()

        for line in data:
            addr = line.strip()
            if (is_valid_address(addr)):
                valid_addresses.add(addr)
                print(valid_addresses)
            else:
                print('Skipping invalid address: {}'.format(addr))

    print('{} valid addresses found'.format(len(valid_addresses)))
    return valid_addresses


def main():
    # Get dash.conf location and load key values
    config_text = DashConfig.slurp_config_file(config.dash_conf)

    # Get valid addresses and determine networks used (Main and/or Test)
    addresses = load_address_file(config.address_file)
    networks = get_used_networks(addresses)
    print('Addresses found on {} network(s)'.format(networks))

    # Establish connections to used network(s)
    rpc_connections = {}
    for network in networks:
        rpc_params = DashConfig.get_rpc_creds(config_text, network)
        rpc_connections[network] = RPCHost(rpc_params['user'], rpc_params['password'], rpc_params['port'])

    print(rpc_connections)

    poll_addresses(rpc_connections, addresses)

if __name__ == '__main__':
    main()
