# FuzzingTools

## LFI Fuzzer

A multithreaded Local File Inclusion (LFI) fuzzing tool with a Rich progress bar.
It sends payloads from a wordlist to a target URL, checks for successful inclusion based on keywords, and saves results.

## Usage

python3 lfi_fuzzer.py -w wordlist.txt -u "http://target.com/page?file={}" -t 10 \
-H headers.txt -o all_results.txt -s success.txt -k "root:x:,Windows" -S
