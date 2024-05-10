from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os.path
import sys
from pathlib import Path
import glob
from configparser import ConfigParser

config = ConfigParser()
config.read("main.ini")
website = config.get('DEFAULT', 'website')
path = config.get('DEFAULT','path')
driver = webdriver.Chrome(path)
driver.get(website)

def toExcel(total,year):
    df = pd.DataFrame(data=total)
    df.to_csv("{}.csv".format(year), index = False)

def hasXpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
        return True
    except:
        return False

def main():

    # directory
    dir_path = os.path.dirname(os.path.realpath(__file__)) #get cd
    dir_data = os.path.join(dir_path,"data")
    Path(dir_data).mkdir(parents=True, exist_ok=True)
    os.chdir(dir_data)

    # total arguments
    n = len(sys.argv)

    if n > 3: 
        print("ERROR: Too many arguments")
        sys.exit()

    # check latest year found in website
    year = 2008
    xpath = '//a[@href="javascript:loadBack({});"]'.format(year)
    while hasXpath(xpath):
        date_latest = year
        year += 1
        xpath = '//a[@href="javascript:loadBack({});"]'.format(year)
    
    #date start and date end
    if n == 3: 
        date_start = sys.argv[1]
        date_end = sys.argv[2]

    if n == 2:
        date_start = sys.argv[1]
        date_end = date_latest

    if n == 1: #default
        extension = 'csv'
        result = glob.glob('*.{}'.format(extension))
        list_years = []
        for files in result:
            fname, fextension = os.path.splitext(files)
            list_years.append(fname)
        if len(list_years) == 0:
            date_start = 2008
        else:
            date_start = (max(list_years))
        date_end = date_latest


    # Errors
    try: 
        int(date_start)
    except ValueError:
        print("ERROR: Only numbers allowed")
        driver.quit()
        sys.exit()
    try: 
        int(date_end)
    except ValueError:
        print("ERROR: Only numbers allowed")
        driver.quit()
        sys.exit()
        
    if len(str(date_start)) > 4 or len(str(date_end)) > 4:
        print("ERROR: Only 4-digits allowed")
        driver.quit()
        sys.exit()

    if len(str(date_start)) < 4 or len(str(date_end)) < 4:
        print("ERROR: Only 4-digits allowed")
        driver.quit()
        sys.exit()

    if int(date_start) > int(date_end) :
        print("ERROR: Year Start is bigger than Year End")
        driver.quit()
        sys.exit()

    if int(date_start) < 2008 :
        print("ERROR: Entered Year is older than 2008")
        driver.quit()
        sys.exit()

    if int(date_end) > int(date_latest):
        print("ERROR: Latest date found is {}".format(date_latest))
        driver.quit()
        sys.exit()

    # Arguments passed
    print("\nYear Start:", date_start)
    print("Year End:", date_end)

    #start scraping
    year = int(date_start)
    xpath = '//a[@href="javascript:loadBack({});"]'.format(year)
    while year <= int(date_end):
        date = pd.date_range(start ='1-1-{}'.format(year),
           end ='12-31-{}'.format(year))
        year_button = driver.find_element("xpath",xpath)
        year_button.click()
        total = []
        n = 0
        mnth = 1
        matches = driver.find_elements(By.XPATH,"//tr[@bgcolor = '#FFFFCC']")
        rows = len(matches) #31 rows
        while mnth <= 12:
            count = 1
            price=[]
            #get all prices in month
            while count <= rows:
                l = driver.find_elements(By.XPATH,"//tr[@bgcolor = '#FFFFCC'][{}]/td".format(count))[mnth] #get each row 
                price.append(l.text)
                count += 1
                
            #remove null values
            price = list(filter(None, price))
            
            #append to dict with date 
            for prices in price:
                prices = prices.replace(',','') #remove comma
                prices = prices.replace('**','')
                try:
                    float(prices)
                    data_dict = {}
                    try:
                        data_dict['Date']=date[n]
                    except Exception:
                        pass
                    data_dict['Price']=prices
                    total.append(data_dict)                    
                except ValueError: 
                    pass
                n += 1
            mnth += 1
        toExcel(total,year)
        year += 1
        if year > date_latest:
            driver.quit()
        xpath = '//a[@href="javascript:loadBack({});"]'.format(year)

    driver.quit()

if __name__=="__main__":
    main()