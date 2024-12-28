import random


balance = 60.75

print (balance)
i = 0 
while i < 5:
    profit = random.uniform(0, 9.5)
    balance = balance + profit
    print(profit)
    print(balance)
    i += 1

 