import requests
import time
import random
import os

start_time = time.time()

cookie = ""  # your roblox cookie here
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
