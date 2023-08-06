from selenium import webdriver 
import os
 
# Get the path of chromedriver which you have install
 
def startLoginBot(username, password, url, cdpath):
    path = cdpath
     
    # giving the path of chromedriver to selenium webdriver
    driver = webdriver.Chrome(path)
     
    # opening the website  in chrome.
    driver.get(url)
     
    # find the id or name or class of
    # username by inspecting on username input
    driver.find_element_by_name(
        "id/class/name of username").send_keys(username)
     
    # find the password by inspecting on password input
    driver.find_element_by_name(
        "id/class/name of password").send_keys(password)
     
    # click on submit
    driver.find_element_by_css_selector(
        "id/class/name/css selector of login button").click()