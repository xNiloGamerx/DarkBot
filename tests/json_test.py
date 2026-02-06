import json

with open(r"C:\Users\nikb0\Documents\01_Programming\01_Projects\DarkBot\src\cogs\counting\shop\counting_shop_items.json", "r", encoding="utf-8") as file:
    shop_items = json.load(file)

for i in range(len(shop_items["items"])):
    shop_item = shop_items["items"][i]
    print(i % 4 < 2)

print(shop_items)
