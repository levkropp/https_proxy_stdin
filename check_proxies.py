import sys
import ast
import requests
import concurrent.futures
from tqdm import tqdm
import random
import time

def check_proxy(proxy):
    url = "https://google.com"
    proxies = {
        "https": "http://"+proxy  # Only use HTTPS proxy
    }
    start_time = time.time()  # Record the start time
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        response_time = time.time() - start_time  # Calculate the response time
        if response.status_code == 200:
            return proxy, True, response_time*1000  # Multiply by 1000 to convert from seconds to milliseconds
        else:
            return proxy, False, None
    except requests.exceptions.RequestException:
        return proxy, False, None

proxies = ast.literal_eval(sys.stdin.read())  # Read list from stdin
random.shuffle(proxies)

print(f"Checking {len(proxies)} proxies for HTTPS...")
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), ncols=70):
        proxy = futures[future]
        try:
            proxy, valid, response_time = future.result()
            if valid:
                print(f"\n{proxy} VALID {round(response_time)} ms")
        except Exception as exc:
            print(f"{proxy} generated an exception: {str(exc)}")
