from kucoin_futures.client import Trade
from kucoin_futures.client import User

import logging
api_key = '63d3f210e24f7d0001edd9ac'
api_secret = '7ced1eb1-5d94-48bc-9547-f291a8efc936'
api_passphrase = '@Fucker.com003'
client = Trade(key='63d3f210e24f7d0001edd9ac', secret='7ced1eb1-5d94-48bc-9547-f291a8efc936',
               passphrase='@Fucker.com003', is_sandbox=False, url='')
balance = User(api_key, api_secret, api_passphrase)

while True:
    try:
        res = client.get_position_details("DYDXUSDTM")
        # client.create_market_order("DYDXUSDTM", "buy", "1", "20")
        logging.warning((res
                         ))
        break
    except Exception as e:
        logging.warning("couldn't get the positions details")
        logging.warning(e)
