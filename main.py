import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    , 'Accept-Language': 'en-US,en;q=0.9'
}
request = requests.get(
    url='https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.57924167041016%2C%22east%22%3A-122.28741732958984%2C%22south%22%3A37.687587849055475%2C%22north%22%3A37.86289213928624%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A704399%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D',
    headers=headers)
page = request.text
soup = BeautifulSoup(page, 'html.parser')
prices = soup.find_all(class_='list-card-price')
links = soup.find_all(href=re.compile('homedetails'), class_='list-card-img')
holder = soup.find_all(href=re.compile('/b/'), class_='list-card-img')
for item in range(len(holder)):
    holder[item]["href"] = f'https://www.zillow.com{holder[item]["href"]}'
[links.append(item) for item in holder]
addresses = soup.find_all(class_='list-card-addr')


for listing in range(len(addresses)):
    chrome_path = r"C:\Users\tajex\.atom\Web Development\HTML - Personal Site\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_path)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSe1G54lqrxHuScCMOenXQRc4mv8ztBKz0lATHzWtdolhUJuPA/viewform")
    time.sleep(2)
    where = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    how_much = driver.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    site = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    where.send_keys(f'{addresses[listing].text}')
    how_much.send_keys(f'{prices[listing].text}')
    site.send_keys(f'{links[listing]["href"]}')
    button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    button.click()
    driver.close()
