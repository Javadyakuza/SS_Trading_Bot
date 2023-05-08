# import required module
import os
import time
import shutil
from functions import *
import sys
import logging
# import functions
# assign directory
directory = 'inboxes'

# array of received signal's
signal_array = []

# the list contains the signal id's that are used
blacklist = []

# this variables saves the words that the particular text should have them

BUY_TEXT = 'this is a buy signal'
SELL_TEXT = 'this is a sell signal'
USED_TEXT = 'depricated'
# check if the script is starting or started before
started = False

# filtering the text


def filter_and_edit(textString: str, filename: str):
    if BUY_TEXT in str(textString):
        shutil.move(f'./inboxes/{filename}', f'./used_signals/{filename}')
        return 'buy'
    if SELL_TEXT in str(textString):
        shutil.move(f'./inboxes/{filename}', f'./used_signals/{filename}')
        return 'sell'
    else:
        shutil.move(f'./inboxes/{filename}', f'./spam/{filename}')
        return 'spam'


def open_buy():
    while True:
        try:
            logging.warning("BUY_OPENING")
            orderId = BUY("open")
            return orderId
        except Exception as e:
            logging.warning(f"{e} accured while operation")

            try:
                pos_detail = get_current_position_situation()
                pos_price = get_current_position_entry_price()
                if (pos_detail == True):
                    if (pos_price == last_price):
                        return ("BUY_DYDXUSDT operation done ")
                    else:
                        res = manually_setting_last_price(pos_price)
                        logging.warning(res)
                        return ("BUY_DYDXUSDT operation done ")
                else:
                    logging.warning("BUY_DYDXUSDT operation incompelete ")
            except Exception:
                logging.warning("issue while fetching the position")


def close_buy():
    while True:
        try:
            logging.warning("BUY_CLOSING")
            pos_price = get_current_position_entry_price()
            orderId = BUY("close")
            return orderId
        except Exception as e:
            logging.warning(f"{e} accured while operation")

            try:
                pos_detail = get_current_position_situation()
                if (pos_detail == False):
                    if (pos_price == last_price):
                        return ("BUY_DYDXUSDT operation done ")
                    else:
                        res = manually_setting_last_price(pos_price)
                        logging.warning(res)
                        return ("BUY_DYDXUSDT operation done ")
                else:
                    logging.warning("BUY_DYDXUSDT operation incompelete ")
            except Exception:
                logging.warning("issue while fetching the position")


def open_sell():
    while True:
        try:
            logging.warning("SELL_OPENING")
            orderId = SELL("open")
            return orderId
        except Exception as e:
            logging.warning(f"{e} accured while operation")

            try:
                pos_detail = get_current_position_situation()
                pos_price = get_current_position_entry_price()
                if (pos_detail == True):
                    if (pos_price == last_price):
                        return ("SELL_DYDXUSDT operation done ")
                    else:
                        res = manually_setting_last_price(pos_price)
                        logging.warning(res)
                        return ("SELL_DYDXUSDT operation done ")
                else:
                    logging.warning("SELL_DYDXUSDT operation incompelete ")
            except Exception:
                logging.warning("issue while fetching the position")


def close_sell():
    while True:
        try:
            logging.warning("SELL_CLOSING")
            pos_price = get_current_position_entry_price()
            orderId = SELL("close")
            return orderId
        except Exception as e:
            logging.warning(f"{e} accured while operation")
            try:
                pos_detail = get_current_position_situation()
                if (pos_detail == False):
                    if (pos_price == last_price):
                        return ("SELL_DYDXUSDT operation done ")
                    else:
                        res = manually_setting_last_price(pos_price)
                        logging.warning(res)
                        return ("SELL_DYDXUSDT operation done ")
                else:
                    logging.warning("SELL_DYDXUSDT operation incompelete ")
            except Exception:
                logging.warning("issue while fetching the position")


def operator(orderText: str, filename: str):
    global started
    if (orderText == 'buy'):

        # doing the buy operation and moving the file to the used signals folder
        if (started == False):
            started = True
            orderId = open_buy()
            deal_saver(f"{orderId},  \n opened buy")
            return (orderId, " \n opened buy")
        else:
            orderId = close_buy()
            if (orderId != "duplicated buy signal !!"):
                print(orderId, '\n closed sell')
                deal_saver(f"{orderId}, \n closed sell")
                print(PNL_calculator()) if (PNL_calculator()) != (
                    'PNL : not changed !!') else print()
                orderId = open_buy()
                deal_saver(f"{orderId}, \n opened buy")
                return (orderId, '\n opened buy')
            else:
                return ("duplicated buy signal !!")
    if (orderText == 'sell'):

        # doing the sell operation and moving the file to the used signals folder
        if (started == False):
            started = True
            orderId = open_sell()
            deal_saver(f"{orderId},  \n opened sell")
            return (orderId, " \n opened sell")
        else:

            orderId = close_sell()
            if (orderId != "duplicated short signal !!"):
                print(orderId, '\n closed buy')
                deal_saver(f"{orderId}, \n closed buy")
                print(PNL_calculator()) if (PNL_calculator()) != (
                    'PNL : not changed !!') else print()
                orderId = open_sell()
                deal_saver(f"{orderId}, \n opened SELL")
                return (orderId, '\n opened SELL')
            else:
                return ("duplicated short signal !!")

# iterate over files in
# that directory


def extract():
    if (len(os.listdir(directory)) > 0):
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                result: str = filter_and_edit(open(f).read(), filename)
                if result != 'spam':
                    res = operator(result, filename)
                    return res
    return ("so signal received")


def run():
    counter = 1000
    while True:
        res = extract()
        print(res)
        time.sleep(15)
        counter = (counter + 1)
        sys.setrecursionlimit(counter)


run()
