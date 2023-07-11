import sys
import ast
import requests
import concurrent.futures
from tqdm import tqdm
import random

def check_proxy(proxy):
    url = "https://google.com"
    proxies = {
        "https": "http://"+proxy  # Only use HTTPS proxy
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return proxy, True
        else:
            return proxy, False
    except requests.exceptions.RequestException:
        return proxy, False

proxies = ast.literal_eval(sys.stdin.read())  # Read list from stdin
random.shuffle(proxies)


print(f"Checking {len(proxies)} proxies for HTTPS...")
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), ncols=70):
        proxy = futures[future]
        try:
            proxy, valid = future.result()
            if valid:
                print(f"")
                print(f"{proxy} VALID")
        except Exception as exc:
            print(f"{proxy} generated an exception: {str(exc)}")
