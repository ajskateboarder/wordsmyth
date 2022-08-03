from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

driver = webdriver.Remote("http://localhost:4444/wd/hub", DesiredCapabilities.CHROME)

driver.set_window_size(1920, 1080)

driver.get("https://www.youtube.com/watch?v=iFPMz36std4")

driver.execute_script("window.scrollTo(1, 500);")

time.sleep(2)

driver.execute_script("window.scrollTo(1, 3000);")

comment_div = driver.find_element(By.XPATH, '//*[@id="contents"]')
comments = comment_div.find_elements(By.XPATH, '//*[@id="content-text"]')
for comment in comments:
    print(comment.text)
