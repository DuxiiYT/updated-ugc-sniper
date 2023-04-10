# some imports
import requests as r
import os
import uuid
import time
import datetime
import colorama

# more imports
from colorama import Fore as fore
from threading import Thread
from itertools import cycle

# checking for update
print(fore.RED + "Checking for potential updates...")
gitcode = r.get("https://raw.githubusercontent.com/DuxiiYT/fixed-ugc-sniper/main/main.py").text
with open("main.py", "r") as f:
    if f.read() != gitcode:
        print(fore.RED + "Found update, updating to newest version..")
        with open("main.py", "w") as f:
            f.write(gitcode)
            print(fore.RED + "Successfully updated, close and open main.py")
            exit(0)

with open("cookie.txt", "r") as f:
    cookie = f.read()

with open("limiteds.txt", "r") as f:
    limiteds = f.read().replace(" ", "").split(",")

with open("proxies.txt", "r") as f:
    proxies = f.read().splitlines()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

urowncooldown = input(fore.YELLOW + "Cooldown for all limiteds: ")

user_id = r.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).json()["id"]
x_token = ""
def get_x_token():
    global x_token

    x_token = r.post("https://auth.roblox.com/v2/logout",
                     cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).headers["x-csrf-token"]

    while 1:
        # Gets the x_token every 4 minutes.
        x_token = r.post("https://auth.roblox.com/v2/logout",
                         cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).headers["x-csrf-token"]
        time.sleep(248)


def buy(json, itemid, productid):
    print(fore.GREEN + "BUYING LIMITED: " + productid)
    data = {
        "collectibleItemId": itemid,
        "expectedCurrency": 1,
        "expectedPrice": 0,
        "expectedPurchaserId": user_id,
        "expectedPurchaserType": "User",
        "expectedSellerId": json["creatorTargetId"],
        "expectedSellerType": "User",
        "idempotencyKey": "random uuid4 string that will be your key or smthn",
        "collectibleProductId": productid
    }

    while 1:
        data["idempotencyKey"] = str(uuid.uuid4())
        bought = r.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{itemid}/purchase-item", json=data,
            headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy})

        if bought.reason == "Too Many Requests":
            print(fore.YELLOW + "Ran into a ratelimit, switching proxy and trying again.")
            proxy = next(proxy_pool) # switch proxy
            print("Proxy: " + proxy)
            time.sleep(0.5)
            continue

        try:
            bought = bought.json()
        except:
            print(bought.reason)
            print(fore.YELLOW +"Json decoder error whilst trying to buy item.")
            continue

        if not bought["purchased"]:
            print(fore.RED + f"Failed buying the limited, trying again.. Info: {bought} - {data}")
        else:
            print(fore.GREEN + f"Successfully bought the limited! Info: {bought} - {data}")

        info = r.post("https://catalog.roblox.com/v1/catalog/items/details",
                      json={"items": [{"itemType": "Asset", "id": int(limited)}]},
                      headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy})
        try:
            left = info.json()["data"][0]["unitsAvailableForConsumption"]
        except:
            print(fore.RED + f"Failed getting stock. Full log: {info.text} - {info.reason}")
            left = 0

        if left == 0:
            print(fore.RED + "Couldn't buy the limited in time. Better luck next time.")
            return


# Get collectible and product id for all the limiteds.
Thread(target=get_x_token).start()

print("Starting Sniper")
while x_token == "":
    time.sleep(0.01)

# https://apis.roblox.com/marketplace-items/v1/items/details
# https://catalog.roblox.com/v1/catalog/items/details

if urowncooldown.isdigit():
    cooldown = int(urowncooldown)/len(limiteds)
else:
    print("not a digit, try again.")
while 1:
    start = time.perf_counter()

    for limited in limiteds:
        try:
            info = r.post("https://catalog.roblox.com/v1/catalog/items/details",
                           json={"items": [{"itemType": "Asset", "id": int(limited)}]},
                           headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).json()["data"][0]
        except KeyError:
            print(fore.YELLOW + f"Ratelimited on proxy: {proxy} - switching proxy and trying again.")
            proxy = next(proxy_pool) # switch proxy
            print("New Proxy: " + proxy)

            time.sleep(5)
            continue

        if info.get("priceStatus", "") != "Off Sale" and info.get("collectibleItemId") is not None:
            productid = r.post("https://apis.roblox.com/marketplace-items/v1/items/details",
                   json={"itemIds": [info["collectibleItemId"]]},
                   headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy})

            try:
                productid = productid.json()[0]["collectibleProductId"]
            except:
                print(fore.RED + f"Something went wrong whilst getting the product id Logs - {productid.text} - {productid.reason}")
                continue

            buy(info, info["collectibleItemId"], productid)

    taken = time.perf_counter()-start
    print(fore.GREEN + "Start: " + str(start))
    print(fore.GREEN + "Taken: " + str(taken))
    print(fore.GREEN + "Cooldown: " + str(cooldown))
    if taken < cooldown:
        time.sleep(cooldown-taken) # better wait time

    ## os.system("cls")
    print(
          f"Time: {round(time.perf_counter()-start, 3)}\n"
          )