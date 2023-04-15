import requests
import time
import random
import os

start_time = time.time()

cookie = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_DA23E587CA51099F9E50D68FD09C1F25564EDE208C9ACE11EFF4B95AE6CDD9047B80A535A5B4F3547C1DD2366D0FE439C1243CE11E66BE20F50C1043D1C61821E2540EDEF19618C47C9FD1E85163ECB9AC783834CC383A63B0B509019B1B84184DE2417AC07642AB2C97419AA2DD2D962CD3C6D9188FAB6791C0451E49E873FF42EF6366B346598E3BAA64AA1020E2E299D77DF671880907D57029C859058B0BAB95146BD6C289388DB5729D436BC061DCDD3AB37DA21399E6DE794DC232CB670A1ED030CCC75D4AB72AB44F090C7FF204BC43229BE228A966AD58FFBDD947E637ACDC818535245A21CCC0E64341DE79B7F69877E9EBC3E50F24E449E296D47CE022F140A53D9DD690383CDC13012EC81C84A5FEA3C799257E165EACA1FE164B6E48E5EF148D735A32FC0E2C16E8B884AD13D53D8790AE1FE3811024ADF4DA396C7076FCFF38486001D9B99ED34E0D382DD21BD63C03541EDEA1919F46FEE3FAB0ED6E1F"  # your roblox cookie here
headers = {
    "Cookie": cookie,
    "X-CSRF-TOKEN": "",
    "Content-Type": "application/json"
}

def check_free_limiteds():
    url = "https://catalog.roblox.com/v2/search/items/details?Category=1&salesTypeFilter=2&SortType=3&Subcategory=2&Limit=10&MaxPrice=0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        free_limiteds = []

        for item in data["data"]:
            if item["price"] == 0 and item["remaining"] > 0:
                free_limiteds.append(item)

        return free_limiteds

    else:
        print(f"Ratelimited. Status code: {response.status_code}")
        return None

def get_random_proxy():
    with open("proxies.txt") as f:
        proxies = f.readlines()
    return {"http": "http://" + random.choice(proxies).strip(),
            "https": "https://" + random.choice(proxies).strip()}

def buy_free_limited():
    free_limiteds = check_free_limiteds()

    if free_limiteds:
        limited_to_buy = free_limiteds[0]
        asset_id = limited_to_buy["id"]
        url = f"https://economy.roblox.com/v1/purchases/products/{asset_id}"
        start_time = time.time()  # initialize start time before the loop

        retry_count = 0
        while retry_count < 5:
            try:
                response = requests.post(url, headers=headers, proxies=get_random_proxy())
            except requests.exceptions.RequestException as e:
                print(f"Failed to buy limited. Proxy error: {e}")
                time.sleep(1)
                retry_count += 1
                continue

            if response.status_code == 200:
                print(f"Purchased {limited_to_buy['name']}.")
                end_time = time.time()  # calculate end time inside the loop
                execution_time = end_time - start_time
                print("Execution time: ", execution_time, "seconds")
                return True
            elif response.status_code == 429:
                print("Failed to buy limited. You may have hit the API rate limit. Switching proxy and trying again.")
                time.sleep(1)
                retry_count += 1
            elif response.status_code == 403:
                print("Failed to buy limited. You may not have enough Robux to make the purchase.")
                break
            elif response.status_code == 404:
                print("Failed to buy limited. The item may no longer be available.")
                break
            elif response.status_code == 400:
                print("Failed to buy limited. Invalid request.")
                break
            elif response.status_code == 401:
                print("Failed to buy limited. Unauthorized. Check your cookie.")
                break
            elif response.status_code == 500:
                print("Failed to buy limited. Internal server error.")
                break
            else:
                print(f"Failed to buy limited. Status code: {response.status_code}")
                time.sleep(1)
                retry_count += 1

    else:
        print("No free limiteds found.")
        return False

while True:
    try:
        success = buy_free_limited()
        if success:
            break
        time.sleep(random.uniform(0.9, 0.6))
        os.system('cls' if os.name == 'nt' else 'clear') # clear console

        execution_time = time.time() - start_time
        print("Execution time:", execution_time, "seconds")

    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
    except:
        print("Error occurred while attempting to buy free limited.")
        time.sleep(random.uniform(0.7, 0.3))

print("No free limited found.")

execution_time = time.time() - start_time
print("Total execution time:", execution_time, "seconds")

print(f"\nExecution time: {execution_time:.2f} seconds")
