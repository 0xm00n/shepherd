from strategy import *
from schedule import repeat, every, run_pending
from colorama import Fore

import datetime 
import time
import alpaca_trade_api as tradeapi
import json

# investment universe consists of the S&P500 index. Simply, buy and hold the index during the 16th day in the month during each month of the year.
# Buy 5% of portfolio value for SPY 1 min before market closes, do take profit at +10% and sell at -5% after purchase
# reference: https://quantpedia.com/strategies/payday-anomaly/


paydayAnom = strategy()
exc_order = bracket_order("SPY", paydayAnom.portfolioValQty('SPY', 0.05), "both", 5, 10)

def checkDay():
    d = datetime.datetime.now()
    print(d)
    return d.strftime("%d")

@repeat(every(1).days)
def runStrat():
    print(Fore.YELLOW + "[!] running strategy..." + Fore.RESET)
    checkDay()
    if checkDay() == "16":
        if "14:59" in time.strftime("%R:%M")[0:5]:
            paydayAnom.addRule(exc_order)
        else:
            print(Fore.RED + "[-] not 1 min b4 market closes...")
    else:
        print(Fore.RED + "[-] not 16th day of month, no order executions...")


while True:
    print(Fore.GREEN + "[+] schedueler running..." + Fore.RESET)
    run_pending()
    time.sleep(1)


