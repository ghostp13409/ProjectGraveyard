from statistics import quantiles
from binance import Client
from binance.enums import *
import config
import time
from binance.client import Client
from binance import client
from datetime import date
import json


client = Client(config.api_key, config.api_secret)


#Variables

coin_pair = 'BTCUSDT'
first = True
initial_pr = -1
initial_to_buy = 0.005
enable_buy_to_sell = 0.0003
sell_from_peak = 0.00003
Balance = 60.75
trading_state = SIDE_BUY
current_buy_in_pr = 0                                                                                      #Curruntly PlaceHolder for db, change it to Buying_Price of Placed_Order [Pending]
local_peak = -1
bot_balance = 0.00314573   #[In asset format, ex. (BTC in BTCUSDT)]                                        #initial_bot_ballance to allocate funds [Pending]

Trade_value = bot_balance                                                                                  #Trade_value is global var for quantity
profit = 0 #fake
buy_in_price = 0
sell_out_price = 0
buy_in_value = 0
sell_out_value = 0


# Change buy_in_value, sell_out_value, bot_balance to USD from BTC!!!



def Trade (current_pr,initial_pr,trading_state):
    print('inside the function')
#    order = client.create_test_order(                                                                       #Place Order [WorkinProgress]
 #                   symbol=coin_pair,
  #                  side=trading_state,
   #                 timeInForce=TIME_IN_FORCE_GTC,
    #                quantity=bot_balance,
     #               price=current_pr)
    with open("trade_db_try_2.json", "r") as read_file:
        db_dict = json.load(read_file)
    if (trading_state == SIDE_BUY):                                                                         
        db_dict['buy_in_price'].append(current_pr)                                                          #append Buy Details to db
        db_dict['buy_in_value'].append(Trade_value)
        buy_in_value = Trade_value
        buy_in_price = current_pr                                                                           #[Pending, add buy-in amount(in_BTC or in_USDT)]
    else:
        db_dict['sell_out_price'].append(current_pr)                                                        #append Sell Details to db
        db_dict['sell_out_value'].append(Trade_value)
        db_dict['profit_value'].append(([sell_out_value][-1] - [buy_in_value][-1]))       #Sell_Price, Profit_Value(in USD), Profit_Percentage(per Trade) [fake value]                                                  
        db_dict['profit_pct'].append(db_dict['profit_value'][-1]*100/[buy_in_value][-1])           #[fake values][change values after implimenting balance system][Pending]
        sell_out_value = Trade_value
        sell_out_price = current_pr
        profit = [sell_out_value][-1] - [buy_in_value][-1]                                                                        #impliment balance system [Pending]
    with open("trade_db_try_2.json", "w") as trade_db:
        data = json.dump(db_dict,trade_db)




while True:
    current_pr = float(client.get_symbol_ticker(symbol= coin_pair)['price'])                                #Get Price
    current_date = str(date.today())[-2:]
    if (first or current_date != prev_date or current_pr < initial_pr):                                     #Exit first iteration and set initial_Price & Date
        first=False
        initial_pr = current_pr
        prev_date = current_date
    print("current ratio : " + str(current_pr/initial_pr))                                                  #Dispaly Trading Details
    print("required ratio : " + str(1+(initial_to_buy/100)))
    print("initial price : " + str(initial_pr))
    print("current price : " + str(current_pr))
    print("current Balance : " + str(bot_balance))
    print("current profit : " + str(profit))
    print("trading value : " + str(Trade_value))
    print(trading_state)
    if (trading_state == SIDE_BUY):
        if (current_pr/initial_pr > 1+(initial_to_buy/100)):                                                #Initial_buy-in_stratagy
            Trade(current_pr,initial_pr,trading_state)                                                      #Start Trade[BUY]
            trading_state = SIDE_SELL                                                                       #Change trading state  
            current_buy_in_pr = current_pr                                                                  #set trade Buy-in Price for sell calculations
    else:
        if ((local_peak/current_buy_in_pr > 1+(enable_buy_to_sell/100))                                     #Selling Stratagy[Main][pending change]
            and (current_pr > current_buy_in_pr)
            and ((1 - current_pr/local_peak) < (sell_from_peak/100))):                                      
            Trade(current_pr,initial_pr,trading_state)                                                      #Start Trade[Sell]
            bot_balance = bot_balance + profit #fake
            Trade_value = bot_balance
            trading_state = SIDE_BUY                                                                        #Change trading state
    if (current_pr > local_peak and trading_state == SIDE_SELL):
        local_peak = current_pr
    time.sleep(1)