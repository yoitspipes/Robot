import getpass
import time
import selenium
from time import sleep
from selenium import webdriver
import random
#import os
#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import subprocess
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
	"download.prompt_for_download": False,
	"download.directory_upgrade": True,
	"safebrowsing.enabled": True
})
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--log-level=3")

#Change your chromedriver path on the line below!
service = Service(executable_path="C:\\Scripts\\chromedriver.exe")

b = webdriver.Chrome(options=chrome_options, service=service)

b.implicitly_wait(25)
wait  = WebDriverWait(b, 15)