import requests, time

def getBalance(address):
    #apiUrlBase = "https://testnet-insight.dashevo.org/insight-api-dash/addr/" # Testnet
    apiUrlBase = "https://insight.dashevo.org/insight-api-dash/addr/" # Mainnet
    apiUrlSuffix = "/balance"
    url = '{}{}{}'.format(apiUrlBase, address, apiUrlSuffix)

    tries = 5
    hadConnectionFailures = False
    while True:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            tries -= 1
            if tries <= 0:
                raise Exception(
                    'Failed to connect to Insight API at {} for balance check.'.format(apiUrlBase))
            hadFailedConnections = True
            print("Couldn't connect for balance check, will sleep for five seconds and then try again ({} more tries)".format(tries))
            time.sleep(5)
        else:
            if (response.status_code == 400):
                tries -= 1
                print('Insight-Api request failure: {} {}. Retrying {} more times...'.format(
                    response.status_code, response.reason, tries))
                time.sleep(1)
                continue

            if hadConnectionFailures:
                print('Connected after retry.')

            break

    if not response.status_code in (200, 500):
        #response.raise_for_status()
        raise Exception('Insight-API connection failure: ' +
                        str(response.status_code) + ' ' + response.reason)

    if (response.text.isdigit() != True):
        raise Exception('Insight-API: Non-numeric balance returned')

    print('Completed with {} tries remaining'.format(tries))
    return response.text
