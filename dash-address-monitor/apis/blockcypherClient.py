from blockcypher import get_address_overview

def getBalance(address):

    # Only works for mainnet addresses
    info = get_address_overview(address, 'dash')
    print('Balance: {}'.format(info['final_balance']))
    return info['final_balance']


#    from blockcypher import get_address_overview
#    print(get_address_overview('Xico5nigvR8Kk2PQZuthSb5dETUf5oAj8g', 'dash')['balance'])
