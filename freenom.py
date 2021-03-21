import json
import functions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def domainsToJson(element):
    a = functions.remSpaces(element.get_attribute('innerHTML'))

    a = a.replace('/"target="_blank">', '')
    a = a.replace('<tr><tdclass="second"><ahref="http://', '{"domain":"')
    a = a.replace('<istyle="font-size:12px;color:#CCC;"class="fafa-external-link"></i></a></td><tdclass="third">', '","registration":"')
    a = a.replace('</td><tdclass="fourth">', '","expiry":"')
    a = a.replace('</td><tdclass="fifth"><spanclass="labelborderRadiusActive">', '","status":"')
    a = a.replace('</span></td><tdclass="sixth">', '","type":"')
    a = a.replace('</td><tdclass="seventh"><divclass="btn-group"><aclass="smallBtnwhiteBtnpullRight"href="clientarea.php?action=domaindetails&amp;id=', '","id":"')
    a = a.replace('">ManageDomain<iclass="fafa-cog"></i></a></div></td><tdclass="notForMobileeighth">&nbsp;</td></tr>', '"},')

    a = '{"domains":[' + a[:-1] + ']}'
    return json.loads(a)

def recordsToJson(element):
    a = functions.remSpaces(element.get_attribute('innerHTML'))

    a = a.replace('<tr><tdvalign="top"class="name_column"><inputtype="hidden"name="records[', '{"id":"')
    a = a.replace('][line]"value=""><inputtype="hidden"name="records[', '","id":"')
    a = a.replace('][type]"value="', '","type":"')
    a = a.replace('"><inputtype="text"name="records[', '","id":"')
    a = a.replace('][name]"value="', '","name":"')
    a = a.replace('"size="25"></td><tdvalign="top"class="type_column"><strong>', '","type":"')
    a = a.replace('</strong></td><tdvalign="top"class="ttl_column","id":"', '","id":"')
    a = a.replace('][ttl]"value="', '","ttl":"')
    a = a.replace('"style="width:60px"></td><tdvalign="top"class="value_column"><pstyle="margin-bottom:0px!important;overflow:auto;","id":"', '","id":"')
    a = a.replace('][value]"value="', '","value":"')
    a = a.replace('"size="30"></p></td><tdvalign="top"class="delete_column"><buttontype="button"class="smallBtncautionColorpullRight"style="font-weight:600;"onclick="if(confirm(', '')
    a = a.replace("'Doyoureallywanttoremovethisentry?'))location.href='/clientarea.php?managedns=", '","domain":"')
    a = a.replace('&amp;page=&amp;records=', '","type":"')
    a = a.replace('&amp;dnsaction=delete&amp;name=', '","name":"')
    a = a.replace('&amp;value=', '","value":"')
    a = a.replace('&amp;line=&amp;ttl=', '","ttl":"')
    a = a.replace('&amp;priority=&amp;weight=&amp;port=&amp;domainid=', '","domain_id":"')
    a = a.replace("';returnfalse;", '')
    a = a.replace('">Delete</button></td></tr>', '"},')

    a = '{"records":[' + a[:-1] + ']}'
    return json.loads(a)

def domainRenewalToJson(element):
    a = functions.remSpaces(element.get_attribute('innerHTML'))

    a = a.replace('<tr><td>', '{"name":"')
    a = a.replace('</span></td><td><spanclass="textred">MinimumAdvanceRenewalis14DaysforFreeDomains</span></td><td><aclass="smallBtngreyBtnpullRight"href="domains.php?a=renewdomain&amp;domain=', '","domain_id":"')
    a = a.replace('</td><td><spanclass="textred">', '","remaining":"')
    a = a.replace('</td><td><spanclass="textgreen">', '","remaining":"')
    a = a.replace('</td><td>', '","status":"')
    a = a.replace('Days', '')
    a = a.replace('">RenewThisDomain</a></td></tr>', '"},')

    a = '{"domains":[' + a[:-1] + ']}'

    return json.loads(a)




def logout(driver):
    driver.execute_script('window.scrollTo(0, 0);')
    try:
        driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/ul/li[6]/span[2]').click()
    except:
        return
    functions.randomSleep()
    driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/ul/li[6]/ul/li[8]/a').click()
    driver.implicitly_wait(10)

def login(driver, username, password):
    logout(driver)

    driver.get('https://my.freenom.com/clientarea.php')
    driver.implicitly_wait(10)

    inputUName = driver.find_element_by_name('username')
    inputUName.send_keys(username)

    functions.randomSleep()

    inputPassword = driver.find_element_by_name('password')
    inputPassword.send_keys(password)

    functions.randomSleep()

    driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/div[2]/form[1]/div[1]/input').click()
    driver.implicitly_wait(10)
