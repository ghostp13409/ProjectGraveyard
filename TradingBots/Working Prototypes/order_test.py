from binance import Client
from binance.enums import *
import config
from binance.client import Client
from binance import client
from datetime import date

client = Client(config.api_key, config.api_secret, testnet=True)


order = client.create_test_order(
    symbol='BTCUSDT',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.00034,
    price='43968.13')