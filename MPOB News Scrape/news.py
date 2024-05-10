from turtle import delay
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from configparser import ConfigParser
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


config = ConfigParser()
config.read("main.ini")
website = config.get('DEFAULT', 'website')
path = config.get('DEFAULT','path')
s=Service(config.get('DEFAULT','path'))
driver = webdriver.Chrome(path)
driver.get(website)

def toExcel(total,year):
    df = pd.DataFrame(data=total)
    df.to_csv("{}.csv".format(year), index = False)

def main():
    iframe = driver.find_elements(By.TAG_NAME,'iframe')[0]
    driver.switch_to.frame(iframe)
    xs = driver.find_elements(By.XPATH,'//tr[@valign="top"]')
    xs.pop(0)
    total = []
    for x in xs:
        original_window = driver.current_window_handle
        data_dict = {}
        my_element_path = './/td[@width="6%"]'
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        date = WebDriverWait(driver, 5,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, my_element_path)))
        date = x.find_element(By.XPATH,'.//td[@width="6%"]')
        if re.findall(r"\d*\/08\/\d*", date.text):
            data_dict['Date'] = date.text
            xpath = './/td[@width="92%"]'
            title_button = x.find_element("xpath",xpath)
            title_button.click() # go to article
            window_after = driver.window_handles[-1]
            driver.switch_to.window(window_after) #switch to new 
            article = driver.find_element(By.XPATH,'//div[@class="style10"]')
            data_dict['Article'] = article.text
            total.append(data_dict)
            print(total)
            driver.close()
            #Switch back to the old tab or window
            driver.switch_to.window(original_window)
            

    print(total)
    xpath = "//a[@href = 'news_title2.php?page=2']"
    button = driver.find_element("xpath",xpath)
    button.click()
    
    driver.quit()


if __name__=="__main__":
    main()