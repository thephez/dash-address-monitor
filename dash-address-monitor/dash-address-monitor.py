from coin_rpc_class import RPCHost
from pprint import pprint

#from blockcypher import get_address_details
#from blockcypher import get_address_full
from blockcypher import get_address_overview

#https://insight.dashevo.org/insight-api-dash/addr/Xoyn4Xxugx5K6HAog7vzxb6Hf3SW586Zfc/balance

RPCPORT = 19998
RPCUSER = 'user'
RPCPASS = 'pass'

addr = ['yY6AmGopsZS31wy1JLHR9P6AC6owFaXwuh']

def pollAddresses(host):
    for a in addr:
        print('Address: {}'.format(a))

        # Check balance
        #info = get_address_overview('Xoyn4Xxugx5K6HAog7vzxb6Hf3SW586Zfc', 'dash')
        #print(info['final_balance'])

        try:
            info = host.call('getaddressbalance', a)
        except Exception as e:
            print(e)
                
        # Compare with previous (if found)

        # Send notification if changed

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
