import os

import pickle
import json

from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import functions
import freenom




option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("window-size=1280,800")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
option.add_argument("user-data-dir=selenium")
#option.add_argument('--headless')
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='chromedriver.exe',options=option)    #Windows
#driver = webdriver.Chrome(options=option)                                       #Linux
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

ip = get('https://api.ipify.org').text
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as configFile:
    config = json.load(configFile)



##########################Cookies##########################
driver.get('https://www.freenom.com/')

pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))
cookies = pickle.load(open('cookies.pkl', 'rb'))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.implicitly_wait(10)


##########################Login##########################
freenom.login(driver, config['username'], config['password'])


##########################Get list of domains##########################
functions.randomSleep()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

functions.randomSleep()

driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/ul/li[2]/a').click()
driver.implicitly_wait(10)

while True:
    try:
        driver.find_element_by_xpath('//*[@id="bulkactionform"]/table/tbody')
        break
    except:
        driver.refresh()

driver.find_element_by_xpath('/html/body/div[1]/section[4]/div/div/div[4]/div/form/select/option[text()="Unlimited"]').click()
driver.implicitly_wait(10)

functions.randomSleep()

domain_list = freenom.domainsToJson(driver.find_element_by_xpath('//*[@id="bulkactionform"]/table/tbody'))


##########################Update Records##########################
for domain in config['domains']:
    domain_records = 'https://my.freenom.com/clientarea.php?managedns=DOMAIN&domainid=ID'
    domain_records = domain_records.replace('DOMAIN', domain['domain'])
    for domainTemp in domain_list['domains']:
        if domainTemp['domain'] == domain['domain']+domain['domain']:
            domain_records = domain_records.replace('ID', domainTemp['id'])

    driver.get(domain_records)
    driver.implicitly_wait(10)

    record_list = freenom.recordsToJson(driver.find_element_by_xpath('//*[@id="recordslistform"]/table/tbody'))

    for record in domain['records']:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for recordTemp in record_list['records']:
            if recordTemp['name'] == record and recordTemp['value'] != ip:
                driver.find_element_by_xpath('//*[@id="recordslistform"]/table/tbody/tr[' + str(int(recordTemp['id'])+1) + ']/td[4]/p/input').clear()
                driver.find_element_by_xpath('//*[@id="recordslistform"]/table/tbody/tr[' + str(int(recordTemp['id'])+1) + ']/td[4]/p/input').send_keys(ip)

                functions.randomSleep()

                driver.find_element_by_xpath('//*[@id="recordslistform"]/button').click()
                driver.implicitly_wait(10)
                break


##########################Logout##########################
freenom.logout(driver)
driver.quit()
