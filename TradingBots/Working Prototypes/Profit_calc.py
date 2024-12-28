import json


db_file="trade_db_try_2.json"


def Show_Profit():
    with open(db_file, "r") as read_file:
        db_dict = json.load(read_file)
    print(sum(db_dict['profit_value']))


Show_Profit()