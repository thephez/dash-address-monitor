"""
    Set up defaults and read dash-address-monitor.conf
"""
import sys
import os
from dash_config import DashConfig

default_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../dash-address-monitor.conf')
)
config_file = os.environ.get('DASH_ADDRESS_MONITOR_CONFIG', default_config)
cfg = DashConfig.tokenize(config_file)


def get_dash_conf():
    home = os.environ.get('HOME')

    dash_conf = os.path.join(home, ".dashcore/dash.conf")
    if sys.platform == 'darwin':
        dash_conf = os.path.join(home, "Library/Application Support/DashCore/dash.conf")

    dash_conf = cfg.get('dash_conf', dash_conf)

    return dash_conf

def get_address_file():
    return cfg.get('address_file', 'addresses.txt')

def get_db_name():
    return cfg.get('db_name', 'balances.dat')

def get_keybase_params():
    keybaseParams = {}
    keybaseParams['team'] = cfg.get('keybase_team', 'myteamname')
    keybaseParams['channel'] = cfg.get('keybase_channel', 'general')
    keybaseParams['screen'] = cfg.get('keybase_screen', 'kbscreen')
    return keybaseParams

dash_conf = get_dash_conf()
address_file = get_address_file()
db_name = get_db_name()
keybase_params = get_keybase_params()
