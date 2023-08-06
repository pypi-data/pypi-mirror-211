from selenium import webdriver as wd 
from selenium.webdriver.common.keys import Keys as ky
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os
import datetime



def scrap_map(url_1,fs,Crome_driver):
    
  
  

    #driver = wd.Chrome('chromedriver.exe')
    driver = wd.Chrome(Crome_driver)

    #scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1
    cz = 0


    lis1 = []
    lis2 = []
    lis3 = []
    lis4 = []


    number = 1
    SCROLL_PAUSE_TIME = 5

    driver.get(url_1)
    
    while True:
        try:
            number = number+1
            #find data
            ur=driver.find_elements(by=By.XPATH,value="//a[@class ='hfpxzc']")
            nam = ur[cz].get_attribute('aria-label')
            #print(nam)
            lis1.append(nam)
            #sleep(3)
            sleep(1)
            con=driver.find_element(by=By.XPATH,value="//a[@aria-label = '" + nam + "']")
            con.click()
            #sleep(5)
            sleep(2)
            #find extra inforamtion
            c1 = driver.find_element(by=By.XPATH,value="//button[@data-tooltip = 'Copy address']")
            adree = c1.get_attribute('aria-label')
            lis4.append(adree)
            c2 = driver.find_element(by=By.XPATH,value="//a[@data-tooltip = 'Open website']")
            web = c2.get_attribute('href')
            lis3.append(web)
            #end
            con1 = driver.find_element(by=By.XPATH,value="//button[@data-tooltip = 'Copy phone number']")
            con2 = con1.get_attribute('aria-label')
            lis2.append(con2)
            #sleep(3)
            sleep(1)
            con3 = driver.find_element(by=By.XPATH,value="//button[@aria-label = 'Close']")
            con3.click()
            sleep(1)
        except IndexError:
            break
            
        except:
            continue
        finally:
            if len(lis3) != len(lis1):
                lis3.append("")
            if len(lis2) != len(lis1):
                lis2.append("")
            if len(lis4) != len(lis1):
                lis4.append("")
            # Scroll down to bottom
            ele = driver.find_element(by=By.XPATH,value="//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]")
            driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
            ele = driver.find_element(by=By.XPATH,value="//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]")
            new_height = driver.execute_script("return arguments[0].scrollHeight", ele)
            last_height = new_height
            cz = cz+1
  
    
    
    fist = fs + ".csv"
    df = pd.DataFrame({'Name':lis1,'Contact no':lis2,'Address':lis4,'web':lis3})
    df.to_csv(fist,index=False)

    
  
    driver.quit()



'''Google_url = "https://www.google.com/maps/search/dentist+new+york/@40.7403671,-74.0224996,13z/data=!3m1!4b1?entry=ttu"
Data_csv = "C://Users//EDITOR//Desktop//Infinity datasoft/data"
Crome_driver = "chromedriver.exe"

scrap_map(Google_url,Data_csv,Crome_driver)'''



    
