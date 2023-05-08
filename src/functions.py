'''
importing the required libraries

'''
import logging
from kucoin_futures.client import User
from kucoin_futures.client import Trade
from kucoin_futures.client import Market
from config import KUCOIN_API_KEY
from config import KUCOIN_API_SECRET
from config import KUCOIN_API_PASSPHRASE
"""
setting the API creditional's

"""

api_key = None
api_secret = None
api_passphrase = None
client = None
# //////////

# ///////////
balance = None
# ///////////

# //////////
price = None
# /////////

# //////////
last_balance = None
last_price = None

# //////////
last_deal_side = None

# //////////
last_deal = None


def initialing():
    # ///////////
    global last_balance
    global last_price
    global api_key
    global api_secret
    global api_passphrase
    global client
    global balance
    global price

    api_key = KUCOIN_API_KEY
    api_secret = KUCOIN_API_SECRET
    api_passphrase = KUCOIN_API_PASSPHRASE
    client = Trade(key=api_key, secret=api_secret,
                   passphrase=api_passphrase, is_sandbox=False, url='')
    # //////////

    # ///////////
    balance = User(api_key, api_secret, api_passphrase)
    # ///////////

    # //////////
    price = Market()
    # /////////

    # //////////
    tmp_balance = balance.get_account_overview('USDT')
    last_balance = tmp_balance["availableBalance"]
    temp_price1 = price.get_ticker("DYDXUSDTM")
    last_price = temp_price1['price']
    # /////////


while True:
    try:
        initialing()
        logging.warning("initialzed successfully")
        break
    except Exception:
        logging.warning("couldn't initial")


def live_price(symbol: str):
    return price.get_ticker(f'{symbol}USDTM')['price']


def get_current_position_currentQty():

    return str(abs(int(client.get_position_details("DYDXUSDTM")['currentQty'])))


def get_current_position_entry_price():

    return client.get_position_details("DYDXUSDTM")['currentCost']


def get_current_position_situation():

    return client.get_position_details("DYDXUSDTM")['isOpen']


def manually_setting_last_price(price):
    global last_price
    last_price = price
    return (f"last trading price has been updated{last_price}")

# if side was close it means calculate the amount for closing the position if it was open means calculate for opening and side = PNL measn give me the newest balance


def available_balance(side):
    if (side != 'close'):
        while True:
            try:
                tmp_balance = balance.get_account_overview('USDT')[
                    "availableBalance"]
                print(f"balance is fetched again and is {tmp_balance}")
                if (last_deal_side == True):
                    # live balance
                    if ((tmp_balance + .5) >= last_balance):
                        print("according to profit balance is updated")
                        return tmp_balance
                    else:
                        print(
                            f"according to profit , balance is not updated LB({last_balance})LIVEB({tmp_balance}), waiting to update...")
                if (last_deal_side == False):
                    # live balance
                    if ((tmp_balance - 0.5) <= last_balance):
                        print("according to lost balance is updated")
                        return tmp_balance
                    else:
                        print(
                            f"according to lost , balance is not updated LB({last_balance})LIVEB({tmp_balance}), waiting to update...")
                else:
                    print("raw balance ")
                    return tmp_balance
            except Exception as e:

                logging.warning(
                    f"the {e} accured while updating the balance , waiting to update ...")
    else:
        return last_balance


def amount_calculator(price, side: str):
    unedited_balance = available_balance(side)
    print("the balance is >>", unedited_balance)
    print("(live & last )price of DYDX >> ", price, "||", last_price)
    deal_saver(f"the balance is >>, {unedited_balance}")
    deal_saver(f"live price of DYDX >> , {price}")
    edited_balance = unedited_balance / 2
    # because the leverage is 5x
    trading_amount = ((edited_balance / float(price))*5)
    print("half of balance to trade in DYDX >>", str(round(trading_amount)))
    deal_saver(
        f"half of balance to trade in DYDX >>,{str(round(trading_amount))}")
    return str(int(round(trading_amount)))+'0'


def deal_saver(data):
    LOG_FILE_PATH = './deals_log/deals_log.txt'
    logFile = open(LOG_FILE_PATH, 'a')
    logFile.write(str(data))
    logFile.close()


def PNL_saver(log):
    LOG_FILE_PATH = './deals_log/deals_log.txt'
    logFile = open(LOG_FILE_PATH, 'a')
    logFile.write(str(log))
    logFile.close()


def PNL_calculator():
    global last_balance
    global last_deal_side
    price1 = float(last_balance)
    price2 = float(available_balance("pnl"))
    if (price1 > price2):  # means losses of funds
        PNL = 100 - (price2*100/price1)
        PNL_saver((f'PNL : lost >> {PNL}%'))
        last_deal_side = False  # means the last deal has been lost
        last_balance = available_balance("pnl")  # updating the balance
        return (f'PNL : lost >> {PNL}%')
    if (price2 > price1):  # means profit of funds
        PNL = 100 - (price1*100/price2)
        PNL_saver((f'PNL : profit >> {PNL}%'))
        last_deal_side = True  # means the last deal has been  profite
        last_balance = available_balance("pnl")  # updating the balance
        return (f'PNL : profit >> {PNL}%')
    else:
        last_balance = available_balance("pnl")  # updating the balance
        return ('PNL : not changed !!')


def price_for_trade(side):
    temp_price1 = price.get_ticker("DYDXUSDTM")
    temp_price = temp_price1['price']
    if (side == 'buy'):
        temp_price = float(temp_price) + 0.005
        return str(round(temp_price, 3))
    if (side == 'sell'):
        temp_price = float(temp_price) - 0.005
        return str(round(temp_price, 3))
    if (side == "manual_sell"):
        temp_price = float(last_price) - 0.005
        return str(round(temp_price, 3))
    if (side == "manual_buy"):
        temp_price = float(last_price) + 0.005
        return str(round(temp_price, 3))


def BUY(condition):
    global last_deal
    if (last_deal != "buy"):
        global last_price
        temp_price = 0
        amount = 0
        if (condition == "open"):
            temp_price = price_for_trade('buy')
            amount = amount_calculator(temp_price, "open")
        if (condition == "close"):
            temp_price = price_for_trade('manual_buy')
            amount = get_current_position_currentQty()

        order_id = client.create_limit_order(
            'DYDXUSDTM', 'buy', '5', str(amount), str(price_for_trade('buy')))
        print("BUY_DYDXUSDT , ID : ", order_id['orderId'])
        res = manually_setting_last_price(temp_price)
        print(res)
        if (condition == 'open'):
            last_deal = "buy"
        return order_id
    else:
        return ("duplicated buy signal !!")


def SELL(condition):
    global last_deal
    if (last_deal != "short"):
        global last_price
        temp_price = 0
        amount = 0
        if (condition == "open"):
            temp_price = price_for_trade('sell')
            amount = amount_calculator(temp_price, "open")
        if (condition == "close"):
            temp_price = price_for_trade('manual_sell')
            amount = get_current_position_currentQty()

        order_id = client.create_limit_order(
            'DYDXUSDTM', 'sell', '5', str(amount), str(price_for_trade('sell')))
        print("SELL_DYDXUSDT , ID : ", order_id['orderId'])

        res = manually_setting_last_price(temp_price)
        print(res)
        if (condition == 'open'):
            last_deal = "short"
        return order_id
    else:
        return ("duplicated short signal !!")
