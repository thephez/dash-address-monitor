# Connect to a the provided Core RPC connection and request address balance

def getBalance(rpcConnection, address):
    balance = rpcConnection.call('getaddressbalance', address)['balance']
    return balance
