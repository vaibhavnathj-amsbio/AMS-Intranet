from selenium import webdriver
import time
import shutil


def getFedExData(filename, user, passcode):
    browser = webdriver.Edge('C://inetpub//wwwroot//AMS-Intranet//AMSBIOintranet//extra_files//msedgedriver.exe')
    browser.maximize_window()
    browser.get('https://www.fedex.com/en-gb/tracking/advanced.html')

    browser.find_element_by_xpath('/html/body/div[1]/header/fedex-cookie-consent/div/div/div/div/form/fieldset/div[3]/button[1]').click()

    login = browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/a')
    login.click()

    username = browser.find_element_by_xpath('//*[@id="NavLoginUserId"]')
    username.send_keys(user)

    password = browser.find_element_by_xpath('//*[@id="NavLoginPassword"]')
    password.send_keys(passcode)

    login_btn = browser.find_element_by_xpath('//*[@id="HeaderLogin"]/button')
    login_btn.click() # login button click
    time.sleep(2) # wait for page to load

    flag = True
    while flag:
        try:
            browser.find_element_by_xpath('//*[@id="startTracking"]').click() # Closes pop up box/message
            flag = False
        except:
            flag = True

    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="export"]').click() # Click export button
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="dataExportContent"]/label[1]').click() # Choose parameters
    browser.find_element_by_xpath('//*[@id="removeView"]').click()
    time.sleep(5)

    browser.close() # exit the browser

    src = "C://Users//administrator.AMSBIO//Downloads//DataExport.csv"
    dest = "C://inetpub//wwwroot//AMS-Intranet//AMSBIOintranet//helper_files//" + filename

    return print(shutil.move(src,dest))


getFedExData("UK.csv", "cinziasim","Amsbio18") # UK FedEx Data
getFedExData("USA.csv", "whmccoy","am$Bioshipp3d") # US FedEx Data
