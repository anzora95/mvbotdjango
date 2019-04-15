from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as soup
from time import sleep
from typing import List, Set

"""
Parametros necesarios:
user de cuenta scraper
pass de cuenta scraper
user de cuenta a ser escrapeada
Parametro si sera followers o followings
"""

"""funcion para friendlist"""
def friendScrapi(sc_us, sc_pas,sc_account,target):

    #def login(driver):

    username = sc_us  # <username here>
    password = sc_pas  # <password here>
    list_css = "div[role='dialog'] a.notranslate"

    #def driver
    options=Options()
    options.add_argument('-headless')
    driver=webdriver.Firefox(options=options)
    #driver=webdriver.Firefox()

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")
    #driver.minimize_window()
    driver.implicitly_wait(10)
    #sleep(5)

    # Login
    driver.find_element_by_css_selector("input[name='username']").send_keys(username)
    #sleep(2)
    driver.find_element_by_css_selector("input[name='password']").send_keys(password)
    #sleep(2)
    driver.find_element_by_css_selector("button[type='submit']").click()
    sleep(4)
    #chase target
    driver.get("https://www.instagram.com/%s/" %(sc_account))
    sleep(4)
    #Select followers or followings links on profile target page
    if target==False:
        fol=driver.find_element_by_css_selector("a[href*='following'] span")
    else:
        fol=driver.find_element_by_css_selector("a[href*='follower'] span")
    fol.click()
    sleep(4)
    
    #Select div class of the followings/followers
    fal=driver.find_element_by_class_name("isgrP")
    sleep(2)
    
    #first scroll into a popup div
    driver.execute_script("arguments[0].scrollTop=arguments[1];",fal,500)
    sleep(2)
    
    last_height=driver.execute_script("return arguments[0].scrollHeight;", fal)
    print(last_height)
    while True:
        count=0
        #second scroll on the popup
        driver.execute_script("arguments[0].scrollTop=arguments[1];",fal,1000)
        sleep(2)
        new_height=driver.execute_script("return arguments[0].scrollHeight;",fal)

        if new_height == last_height:  
            print("this is the last_height")
            print(last_height)
            print("This is new_height")
            print(new_height)
            break
        else:
            last_height=new_height
            driver.execute_script("arguments[0].scrollTop=arguments[1];",fal,500)
            print(last_height)
            count=count+1
   
    #
    _followers= driver.find_elements_by_css_selector(list_css)
    followers = [i.text for i in _followers]
    driver.close()
    return(followers)
    




"""
Parametros para la funcion de autenticacion de logeo
usuario
pass
"""
def validat(user,contra):
    username = user  # <username here>
    password = contra  # <password here>
    login_url="https://www.instagram.com/accounts/login/"
    saver=0
        

        #def driver
    driver=webdriver.PhantomJS()

        # Load page
    driver.get("https://www.instagram.com/accounts/login/")
    sleep(4)

        # Login
    driver.find_element_by_css_selector("input[name='username']").send_keys(username)
    driver.find_element_by_css_selector("input[name='password']").send_keys(password)
    driver.find_element_by_css_selector("button[type='submit']").click()
    sleep(2)
    if driver.current_url==login_url:
        print("error credenciales invalidas")
        driver.close()
        saver=1
        
    else:
        print("credenciales validas")
        driver.close()
        saver=2
    return saver