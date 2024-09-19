"""
This is a web scraper which is specially devoloped for extracting comapany information from LinkedIn
This uses a selenium and bs4 to create a virtual browser for log in credentials

"""

# importing required libraries
import time
from selenium import webdriver
from selenium.webdriver.common.by import By                   
import pandas as pd
from bs4 import BeautifulSoup

# A function for login to LinkedIn
def login():                                                  
    time.sleep(2)
    username = " your username "
    password = " your password "
    user = driver.find_element(By.ID, value="username")
    passw = driver.find_element(By.ID, value="password")
    button = driver.find_element(By.CLASS_NAME, value="btn__primary--large")
    user.send_keys(username)
    passw.send_keys(password)
    time.sleep(2)
    button.click()
    time.sleep(3)

#initialising the variables to store data
website = ""
industry = ""
c_size = ""
associated_mem = ""
head = ""
types = ""
founded = ""
spcl = ""
followers = ""
phone=""

# webdriver for virtualbrowser
driver = webdriver.Chrome(executable_path="C:\path\contains\chromedriver-win64\chromedriver.exe")

# A file containing company information
urls = pd.read_csv("C:\path\containing\company_url\information.csv")

# login call
driver.get("https://www.linkedin.com/login")
login()

# Iterate through the file containingcompany information
for i in range(urls.shape[0]):

    website = ""
    industry = ""
    c_size = ""
    associated_mem = 0
    head = ""
    type = ""
    founded = ""
    spcl = ""
    phone = ""

    # column contain url
    c_url = urls.iloc[i, 2].strip()
    driver.get(f"{c_url}/about")

    # time to neutral network connection problems
    time.sleep(7)
    page = driver.page_source

    # Read the file in bs4 for scraping
    page = BeautifulSoup(page, 'html.parser')
    title = (page.title.getText().strip())
  
    if title == "LinkedIn Login, Sign in | LinkedIn":
        login()
      
    try:
        followers = page.select(".inline-block .org-top-card-summary-info-list__info-item")[-2].getText().strip()
        dummy = int(followers[0])
    except:
        followers = ""

    web = page.select(".ember-view .artdeco-card .overflow-hidden dt")
    answer = page.select(".ember-view .artdeco-card .overflow-hidden dd")
  
    for k in web:
        print(k.getText().strip())
    for j in answer:
        print(j.getText().strip())
      
    l = 0
    for k in range(len(web)):
        try:
            if web[k].getText().strip() == "Website":
                website = answer[l].getText().strip().replace(",", "")
            elif web[k].getText().strip() == "Industry":
                industry = answer[l].getText().strip().replace(",", "")
            elif web[k].getText().strip() == "Company size":
                c_size = answer[l].getText().strip().replace(",", "")
                l += 1
            elif web[k].getText().strip() == "Headquarters":
                head = answer[l].getText().strip().replace(",", "")
            elif web[k].getText().strip() == "Specialties":
                spcl = answer[l].getText().strip().replace(",", "")
            elif web[k].getText().strip() == "Phone":
                phone = answer[l].getText().strip().split("  ")[0].strip().replace(",", "").replace('+',"")
            l += 1
        except:
            print("error")

    company_id = i

    # Assume the file conatains name and its url
    company_name = urls.iloc[i, 1].strip()

    # Storing the result as a csv file
    with open("file_contains_url.csv", "a+") as f:
        try:
            f.write(f"{company_id},{company_name}, {website} ,{industry},{c_size}, {phone} ,{followers},{head},{types},{spcl},\n")
        except:
            pass
        time.sleep(3)




