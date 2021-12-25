from riposte import Riposte
from colorama import Fore

import alpaca_trade_api as tradeapi
import pandas as pd
import json
import random

shepherd = Riposte(prompt="[shepherd] >> ")

creds = json.load(open('api.json',))

api = tradeapi.REST(
    creds["alpaca_apiKeyID"],
    creds["alpaca_secretKey"],
    creds["alpaca_endpoint"], api_version='v2'
)

@shepherd.command("exit")
def exit():
    quit()

@shepherd.command("new_buy_side_market_order")
def new_buy_side_market_order():
    symbol = input('\n' + "symbol of security u want to order: ")
    qty = input("quantity of security u want to order: ")
    
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    print(Fore.GREEN + "[+] new buy-side market order with client ID: " + " submitted" + Fore.RESET + '\n')


@shepherd.command("new_sell_side_limit_order")
def new_sell_side_limit_order():
    symbol = input('\n' + "symbol of security u want to order: ")
    qty = input("quantity of security u want to order: ")
    lim_price = input("what is your limit price: ")
    
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='limit',
        time_in_force='opg',
        limit_price=lim_price
    )
    print(Fore.GREEN + "[+] new sell-side limit order with client ID: " + client_id + " submitted" + Fore.RESET + '\n')


@shepherd.command("new_trailing_stop_order")
def new_trailing_stop_order():
    symbol = input('\n' + "symbol of security u want to order: ")
    qty = input("quantity of security u want to order: ")

    # buy-side market order
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='gtc'

    )
    print(Fore.GREEN + "[+] new buy-side market order submitted" + Fore.RESET + '\n')

    percent_or_price = input("would you like to use trail price or trail percent (trail_price or trail_percent): ")

    if percent_or_price == "trail_price":
        trailprice = input("enter trail price: ")
        
        # trailing stop order using trail price
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='trailing_stop',
            trail_price=trailprice,  # stop price will be hwm - trail price
            time_in_force='gtc'
        )
        print(Fore.GREEN + "[+] trailing stop order using trail price submitted" + Fore.RESET + '\n')

    if percent_or_price == "trail_percent":
        trailpercent = input("enter trail percent")

        # trail percent
        api.submit.order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='trailing_stop',
            trail_percent=trailpercent,
            time_in_force='gtc'
            
        )
        print(Fore.GREEN + "[+] trailing stop order using trail percent submitted" + Fore.RESET + '\n')

    
@shepherd.command("new_bracket_order")
def new_bracket_order():
    symbol = input('\n' + "symbol of security u want to order: ")
    qty = input("quantity of security u want to order: ")

    symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]
    symbol_price = symbol_bars[symbol]['close']

    strat = input("stop-loss + take-profit or only stop-loss (stop-loss or both): ")

    if strat == "both":
         percent = input("specify percentage for stop-loss and take-profit: ")
         
         # buy a position and add a stop-loss and a take-profit of user specified percent
         api.submit_order(
             symbol=symbol,
             qty=qty,
             side='buy',
             type='market',
             time_in_force='gtc',
             order_class='bracket',
             stop_loss={'stop_price': symbol_price * (1.0 - (percent / 100.0)),
                        'limit_price':  symbol_price * (1.0 - (percent / 100.0) - 0.01)},
            take_profit={'limit_price': symbol_price * (1.0 + (percent / 100.0))}
        )
         print(Fore.GREEN + "[+] bracket order (stop-loss + take-profit) submitted" + Fore.RESET + '\n')
    
    elif strat == "stop-loss":
        percent = input("specify stop-loss percentage: ")

        api.submit_order(
            symbol=symbol,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='oto',
            stop_loss={'stop_price': symbol_price * (1.0 - (percent / 100.0))}
        )
        print(Fore.GREEN + "[+] bracket order (stop-loss) submitted" + Fore.RESET + '\n')


@shepherd.command("get_closed_orders")
def get_order():
    show_order = input('\n' + "how many closed orders to display: ")
    orders = api.list_orders(
        status='closed',
        limit=show_order,
        nested=True  # show nested multi-leg orders
    )
    print(orders)
    print('\n')

@shepherd.command("portfolio_gain_loss")
def portfolio_gain_loss():
    account = api.get_account()

    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    if balance_change > 0:
        print('\n' + Fore.GREEN + f'today\'s portfolio balance change: ${balance_change}' + Fore.RESET + '\n')
    else:
        print('\n' + Fore.RED + f'today\'s portfolio balance change: ${balance_change}' + Fore.RESET + '\n')


@shepherd.command("tradeable_or_not")
def tradeable_or_not():
    sym = input('\n' + "enter symbol to check if tradeable on alpaca or not: ")
    asset = api.get_asset(sym)
    if asset.tradable:
        print(Fore.GREEN + sym + " is tradeable" + Fore.RESET + '\n')
    else:
        print(Fore.RED + sym + " is not tradeable" + Fore.RESET + '\n')

def banner():
    print("  ██████  ██░ ██ ▓█████  ██▓███   ██░ ██ ▓█████  ██▀███  ▓█████▄ ")
    print("▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██░  ██▒▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒▒██▀ ██▌")
    print("░ ▓██▄   ▒██▀▀██░▒███   ▓██░ ██▓▒▒██▀▀██░▒███   ▓██ ░▄█ ▒░██   █▌")
    print("  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██▄█▓▒ ▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  ░▓█▄   ▌")
    print("▒██████▒▒░▓█▒░██▓░▒████▒▒██▒ ░  ░░▓█▒░██▓░▒████▒░██▓ ▒██▒░▒████▓ ")
    print("▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░▒▓▒░ ░  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░ ▒▒▓  ▒ ")
    print("=================================================================")
    print("                 trading bot built by @m00n \n")



def main():
    banner()

    account = api.get_account()
    clock = api.get_clock()

    print(Fore.GREEN + '            ${} is available as buying power.'.format(account.buying_power) + Fore.RESET)
    print('                     the market is {}'.format(Fore.GREEN + 'open.' + Fore.RESET if clock.is_open else Fore.RED + 'closed.' + Fore.RESET))
    print('\n')

    shepherd.run()



if __name__ == "__main__":
    main()



