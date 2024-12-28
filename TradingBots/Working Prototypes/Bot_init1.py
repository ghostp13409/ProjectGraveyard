#!/usr/bin/env python
# coding: utf-8

# In[43]:


import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
from datetime import date
import json
import config # for api keys

# In[33]:

client = Client(config.api_key, config.api_secret)


# In[102]:


bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')
first = True
initial_pr = -1
initial_to_buy = 0.5
enable_buy_to_sell = 1.3
sell_from_peak = 0.3
Balance = 100
trading_state = 'buy'
current_buy_in_pr = 0
local_peak = -1


# In[45]:


def createframe (msg) :
    df = pd.DataFrame( [msg] )
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol','Time','Price']
    df.Price = df.Price.astype (float)
    df.Time = pd.to_datetime (df . Time, unit='ms' )
    return df

# In[57]:



def Trade (current_pr,initial_pr,current_time,trading_state):
    print('inside the function')
    with open("trade_db.json", "r") as read_file:
        db_dict = json.load(read_file)
    if (trading_state == 'buy'):
        db_dict['buy_in_price'].append(current_pr)
        db_dict['buy_in_time'].append(str(current_time))
    else:
        db_dict['sell_out_price'].append(current_pr)
        db_dict['sell_out_time'].append(str(current_time))
        db_dict['profit_value'].append((db_dict['sell_out_price'][-1] - db_dict['buy_in_price'][-1]))
        db_dict['profit_pct'].append(db_dict['profit_value'][-1]*100/db_dict['buy_in_price'][-1])
    with open("trade_db.json", "w") as trade_db:
        data = json.dump(db_dict,trade_db)
    
    
# In[103]:


while True:
    await socket.__aenter__()
    msg = await socket.recv()
    current_df = createframe(msg)
    print(current_df)
    current_pr = current_df.loc[0,"Price"]
    current_time = current_df.loc[0,"Time"]
    current_date = str(date.today())[-2:]
    if (first or current_date != prev_date or current_pr < initial_pr):
        first=False
        initial_pr = current_pr
        prev_date = current_date
    print("current ratio : " + str(current_pr/initial_pr))
    print("required ratio : " + str(1+(initial_to_buy/100)))
    print("initial price : " + str(initial_pr))
    print("current price : " + str(current_pr))    
    if (trading_state == 'buy'):
        if (current_pr/initial_pr > 1+(initial_to_buy/100)):
            Trade(current_pr,initial_pr,current_time,trading_state) #make a row for order in db -> make an buy order
            trading_state = 'sell'
            current_buy_in_pr = current_pr            
    else:
        if ((local_peak/current_buy_in_pr > 1+(enable_buy_to_sell/100)) and (current_pr > current_buy_in_pr) and ((1 - current_pr/local_peak) < (sell_from_peak/100))):
            Trade(current_pr,initial_pr,current_time,trading_state)
            trading_state = 'buy'
    if (current_pr > local_peak and trading_state == 'sell'):
        local_peak = current_pr
            





# In[91]:


def Clear_DB():
    with open("trade_db.json", "w") as trade_db:
        db_dict = {"buy_in_price": [], "sell_out_price": [], "profit_pct": [], "profit_value": [], "buy_in_time": [], "sell_out_time": []}
        data = json.dump(db_dict,trade_db)


# In[98]:


Clear_DB()


# In[99]:


def Show_Profit():
    with open("trade_db.json", "r") as read_file:
        db_dict = json.load(read_file)
    print(sum(db_dict['profit_value']))


# In[104]:


Show_Profit()

