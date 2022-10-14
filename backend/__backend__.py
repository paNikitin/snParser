import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
from captcha_solver import CaptchaSolver

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1024,768")
options.add_argument("--headless")

with open('driver_path.txt', 'r', encoding='utf-8') as file:
    path = file.readline()
    print(path)
    file.close()
driver = webdriver.Chrome(
    executable_path=path,
    options=options
)

driver = webdriver.Chrome(
    executable_path=path,
    options=options
)
url = "https://vk.com/"


def elementInteraction(input):
    ActionChains(driver) \
        .move_to_element_with_offset(input, 8, 0) \
        .click() \
        .perform()


def sendKeys(element, input):
    element.clear()
    element.send_keys(input)


def getToMainPage(login, password, key):
    driver.implicitly_wait(10)
    driver.get(url=url)
    time.sleep(2)
    driver.save_screenshot("1.png")
    email_input = driver.find_element(By.XPATH,
                                      '//*[@id="index_email"]')
    elementInteraction(email_input)
    sendKeys(email_input, login)
    time.sleep(1)
    login_button = driver.find_element(By.XPATH,
                                       '//*[@id="index_login"]/div/form/button[1]')
    elementInteraction(login_button)
    time.sleep(2)
    if check_exists_by_xpath('//*[@id="root"]/div/div/div/div[2]/div/div/form/img'):
        captchaSolve(key)
        time.sleep(1)
    password_input = driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/div/div/div[2]/div/div/form/div[1]/div[3]/div[1]/div/input')
    elementInteraction(password_input)
    sendKeys(password_input, password)
    time.sleep(1)
    login_button = driver.find_element(By.XPATH,
                                       '//*[@id="root"]/div/div/div/div/div[2]/div/div/form/div[2]/button')
    elementInteraction(login_button)
    time.sleep(2)
    driver.save_screenshot("2.png")


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def scrapeElements(page):
    doc = BeautifulSoup(page, 'html.parser')
    details = doc.find_all('div', {'class': 'ProfileModalMiniInfoCell'})
    output = ""
    for param in details:
        output += param.text
        output += " | "
    return output


def singleHumanHandler(human_id):
    driver.get(url=f'https://vk.com/id{human_id}')
    driver.implicitly_wait(5)
    time.sleep(2)
    output = ""
    if check_exists_by_xpath('//*[@id="owner_page_name"]'):
        output = driver.find_element(By.XPATH, '//*[@id="owner_page_name"]').text
        output += " | "
        if check_exists_by_xpath(
                '//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[3]/div[2]'):
            details = driver.find_element(By.XPATH,
                                          '//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[3]/div[2]')
            elementInteraction(details)
            time.sleep(3)
            output += scrapeElements(driver.page_source)
            output = "|" + str(human_id) + "| " + output
        elif check_exists_by_xpath('//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div'):
            details = driver.find_element(By.XPATH,
                                          '//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div')
            elementInteraction(details)
            time.sleep(3)
            output += scrapeElements(driver.page_source)
            output = str(human_id) + "| " + output
        else:
            if check_exists_by_xpath(
                    '//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[3]/div[2]'):
                details = driver.find_element(By.XPATH,
                                              '//*[@id="profile_redesigned"]/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[3]/div[2]')
                elementInteraction(details)
                time.sleep(3)
                output += scrapeElements(driver.page_source)
                output = "|" + str(human_id) + "| " + output
            else:
                output = "....| " + str(human_id) + " | " + output + "Профиль заблокирован."
    else:
        output = "???" + str(human_id) + "|" + "Профиль не существует."
    return output


def readIds(path):
    ids = []
    with open(path, 'r', encoding='utf-8') as file:
        [ids.append(line) for line in file.readlines()]
        file.close()
    output = np.asarray(ids)
    return output


def writeOutput(array):
    with open('output.txt', 'w', encoding='utf-8') as file:
        for single_human in array:
            file.writelines(single_human + "\n")
    file.close()


def captchaSolve(key):
    img = driver.find_element(By.XPATH,
                              '//*[@id="root"]/div/div/div/div[2]/div/div/form/img')
    src = img.get_attribute('src')
    urllib.request.urlretrieve(src, 'captcha.png')
    time.sleep(1)
    driver.save_screenshot("3.png")
    solver = CaptchaSolver('rucaptcha', api_key=key)
    raw_data = open('captcha.png', 'rb').read()
    answer = solver.solve_captcha(raw_data)
    captcha_input = driver.find_element(By.XPATH,
                                        '//*[@id="root"]/div/div/div/div[2]/div/div/form/div[1]/div/div/input')
    sendKeys(captcha_input, str(answer))
    captcha_submit = driver.find_element(By.XPATH,
                                         '//*[@id="root"]/div/div/div/div[2]/div/div/form/div[2]/button')

    elementInteraction(captcha_submit)







