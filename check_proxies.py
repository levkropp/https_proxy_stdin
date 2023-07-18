import sys
import ast
import requests
import concurrent.futures
from tqdm import tqdm
import random
import time
import argparse

def check_proxy(proxy, url, verbose, very_verbose):
    if very_verbose:
        print(f"\nStarting check for proxy: {proxy}")

    proxies = {
        "https": "http://"+proxy  # Only use HTTPS proxy
    }
    start_time = time.time()  # Record the start time
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
    except requests.exceptions.RequestException:
        return proxy, False, None

    response_time = time.time() - start_time  # Calculate the response time
    if response.status_code == 200:
        return proxy, True, response_time*1000  # Multiply by 1000 to convert from seconds to milliseconds
    else:
        return proxy, False, None

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="url to check with proxy", default="https://example.com")
parser.add_argument("-t", "--threads", help="number of worker threads", default=16, type=int)
parser.add_argument("-v", "--verbose", help="print invalid proxies", action='store_true')
parser.add_argument("-vv", "--very_verbose", help="print start and end of each proxy check", action='store_true')
args = parser.parse_args()

proxies = ast.literal_eval(sys.stdin.read())  # Read list from stdin
random.shuffle(proxies)

valid_proxies = []  # List to store valid proxies and their response times

print(f"URL: {args.url}")
print(f"Number of threads: {args.threads}")
print(f"Checking {len(proxies)} proxies for HTTPS...")

with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    futures = {executor.submit(check_proxy, proxy, args.url, args.verbose, args.very_verbose): proxy for proxy in proxies}
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), ncols=70):
        proxy = futures[future]
        try:
            proxy, valid, response_time = future.result()
        except Exception as exc:
            print(f"{proxy} generated an exception: {str(exc)}")
            continue

        if valid:
            print(f"\n{proxy} VALID {round(response_time)} ms")
            valid_proxies.append((proxy, response_time))  # Add valid proxy and its response time to the list
        elif args.verbose:
            print(f"\n{proxy} INVALID")

        if args.very_verbose:
            print(f"Finished check for proxy: {proxy}")


# Sort the valid proxies by response time in descending order
valid_proxies.sort(key=lambda x: x[1], reverse=True)

print(f"\n{'Rank':<5}{'Proxy':<25}{'Response Time (ms)':<15}")
print("-"*45)

# Reverse the list for enumeration
valid_proxies.reverse()

for i, (proxy, response_time) in enumerate(valid_proxies, start=1):
    print(f"{i:<5}{proxy:<25}{round(response_time)}")
