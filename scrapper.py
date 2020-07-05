import pandas as pd
from selenium import webdriver
import time
import re
import requests
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
#from tld import get_tld, get_fld
import numpy as np
from urllib.parse import urlparse, parse_qs
import tldextract

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("Chrome/83.0.4103.97")

input1 = pd.read_csv(r'input.csv')
input1 = pd.DataFrame(input1)
k = len(input1.index)
data = pd.DataFrame(columns = ['First_Name','Last_Name','Site','Email_ID'])
delays = range(2,6)
n = int(input("enter n :"))
#k = 5
for j in range(k):
    First_name = input1.iloc[j,0]
    Last_name = input1.iloc[j,1]
    Mail_format =( "( @gmail.com OR  @yahoo.com OR @hotmail.com)")
    z = input1.iloc[j,2]
    #m = get_tld(z, as_object = True)
    #Site = m.fld
    Site = tldextract.extract(str(z)).domain

    df = []
    df.append(str(First_name.strip() + " " + Last_name.strip() + " " + Mail_format.strip() + " " + "AND" + " " +  "www." + Site))
    df.append(str(First_name.strip() + " " + Last_name.strip() + " " + Mail_format.strip() + " " + "AND" + " " +  "gmail.com"))
    df.append(str(First_name.strip() + " " + Last_name.strip() + " " + Mail_format.strip() + " " + "AND" + " " +  "yahoo.com"))
    df.append(str(First_name.strip() + " " + Last_name.strip() + " " + Mail_format.strip() + " " + "AND" + " " +  "hotmail.com"))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + "." + Last_name.strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + Last_name.strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + "_" + Last_name.strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name[0].strip() + "." + Last_name.strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + "." + Last_name[0].strip() + '@' + Site))
    df.append(str(Site.strip() + " " + First_name.strip() + " " + Last_name.strip() + " " +  First_name.strip() + Last_name[0].strip() + '@' + Site))
    df.append(str(Site.strip() + " " + Site + "/" + "contact-us" + " " + "( @gmail.com OR  @yahoo.com OR @hotmail.com)"))
    df.append(str(Site.strip() + " " + Site + "/" + "contact"))
    df.append(str(Site.strip() + " " + Site + "/" + "contact-me"))
    #n = 4
    
    emails = set()
    browser = webdriver.Chrome(chrome_options = options, executable_path= r".\driver\chromedriver.exe")
    
    for i in range(n):
        time.sleep(5)
        browser.get("https://www.google.com")
        delay = np.random.choice(delays)
        
        time.sleep(delay)
        
        
        v = browser.find_element_by_xpath("/html/body/div/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input")
        for x in df[i]:
            v.send_keys(x)
            time.sleep(1)
        delay = np.random.choice(delays)
        
        time.sleep(delay)
        try:
            browser.find_element_by_xpath("/html/body/div/div[3]/form/div[2]/div[1]/div[3]/center/input[1]").click()
            delay = np.random.choice(delays)
        
            time.sleep(delay)
            
        except(ElementClickInterceptedException,ElementNotInteractableException):
            browser.find_element_by_xpath("/html/body/div/div[3]/form/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]").click()
            delay = np.random.choice(delays)
            time.sleep(delay)

        url = browser.current_url
        o = urlparse(url)
        query = parse_qs(o.query)
        url = o._replace(query=None).geturl()
        if 'token' in query:
            query['token'] = 'NEW_TOKEN'
        try:
            response = requests.get(url, params=query)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            print("Hi")
        delay = np.random.choice(delays)
        time.sleep(delay) 

        
        new_emails = set(re.findall(r"[a-z0-9\.\-_]+@[a-z0-9\.\-_]+\.com", response.text, re.I))
        my_list = list(new_emails)
        x = len(my_list)
        
    
        for l in range(x):
            data = data.append({'First_Name':First_name,'Last_Name':Last_name,'Site': Site, 'Email_ID':my_list[l]},  ignore_index=True )
            print(data)
        
    browser.close()
    c = "Progress" + str(j).strip() + "/" + str(k)
    print(c)
    delay = np.random.choice(delays)
    time.sleep(delay)
    


data.to_csv('Email_Output6.csv', index=False)


