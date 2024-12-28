import json

db_file="trade_db_try_2.json"

def Clear_DB():
    with open(db_file, "w") as trade_db:
        db_dict = {"buy_in_price": [], "sell_out_price": [], "buy_in_value": [], "sell_out_value": [], "profit_pct": [], "profit_value": []}
        data = json.dump(db_dict,trade_db)
        print("db Cleared")

Clear_DB()
