# shepherd
<b> a simple quant trading bot with seperate CLI interface/ backend REST API </b>
<br>
this was code I wrote for a uni CS class project, so obv not production grade and mainly for learning about alpaca's API...


<br>

![](https://user-images.githubusercontent.com/71098497/134826072-b99b649f-72e3-457f-b4b9-b4a107247616.png)


<br>

## Features
 - clean CLI shell interface
 - utilizes alpaca API
 - concise commands for executing various orders and strategies
    - buy-side market orders
    - sell-side limit orders
    - trailing stop orders (supports both trail price and trail percentage)
    - bracket orders (stop-loss + take-profit or only stop-loss)
    
 - miscellaneous helpful commands 
    - portfolio gain/loss
    - market open/close indicator
    - portfolio buying power indicator
    - closed orders display
    - asset check to see if it's tradeable through alpaca API

 - REST API
    - GET and POST requests to /api/v1/order endpoint
    - /api/v1/portfolioInfo endpoint to fetch portfolio info continously
    - REST API consumer example file included
    - custom ID system for orders
    - MongoDB order storage integration
    - custom strategy class for easy strategy creation
      - custom alpaca order function wrappers
      - write strategies w/ minimal lines of code
      - sample Payday Anomaly strategy using custom class
 
 <br>

<br>

 ## Docs
<br>

```
exit - exit shepherd shell
```
```
"new_buy_side_market_order - execute new buy side market order
```
```
new_sell_side_limit_order - execute new sell side limit order
```
```
new_trailing_stop_order - execute new trailing stop order.
                          can use either trail price or trail percentage.
```
```
new_bracket_order - execute new bracket order with either stop-loss alone or
                    both take-profit and stop-loss
```
```
get_closed_orders - get closed orders 
```
```
portfolio_gain_loss - display connected porfolio's current gain/loss
```
```
tradeable_or_not - check to see if symbol is tradeable w/ alpaca
```

<br>

- For REST API, you will need to fill in mongodb URI in app.py, handlers.py, and utils.py
- Additionally, fill in API keys for alpaca in both REST API and CLI components JSON files

<br>
<br>
 
 ## To-Do

- Implement real-time IEX web socket market data fetching (quotes, bars, etc.) in REST API
