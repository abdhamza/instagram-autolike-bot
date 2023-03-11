# for each follower on instagram, it will go to their page and like their most recent photo?
# Input should expect a username...  it will then pull a list of the accounts that user is following,
# and then go like the most recent post. Use firefox  on Mac OS.
# install packages in script
import subprocess
import sys

# Install for mac os
if sys.platform == "darwin":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])

elif sys.platform == "win32":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])

elif sys.platform == "linux":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])


# imports here
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup as bs

# Log In to Your Instagram Account
# specify the path to chromedriver.exe (download and save on your computer)
# install genko driver while running this code
# get the input from user for username and password
username_insta = input("Enter your username: ")
# username_insta = "user_name"
password_insta = input("Enter your password: ")
# password_insta = "*****"


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# open the webpage
driver.get("http://www.instagram.com")

# target username
# Usually webpages take some time to load. First HTML is initialized then css and other elements. so we need to add delay untill the elements are available to be used.
# WebDriverWait function waits untill the username element is available to be clicked
try:
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
    )
except:
    print("Error username or password not found")
    driver.quit()
# enter username and password
# username.clear() function clears username area for us to type our own personal username

username.clear()
username.send_keys(username_insta)
# password.clear() function clears password area for us to type our own unique password
password.clear()
password.send_keys(password_insta)

# target the login button and click it
# click() function is used to click
try:
    button = (
        WebDriverWait(driver, 2)
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        .click()
    )
except:
    print("submit button issue")
    driver.quit()
# We are logged in
# Handle Alerts
# you might only get a single alert, or you might get 2 of them
# please adjust the cell below accordingly

time.sleep(5)
try:
    alert = (
        WebDriverWait(driver, 15)
        .until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        )
        .click()
    )
except:
    print("No alert")
    pass
try:
    alert2 = (
        WebDriverWait(driver, 15)
        .until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Not Now")]')
            )
        )
        .click()
    )
except:
    print("No alert")
    pass

driver.get(f"https://www.instagram.com/{username_insta}/")
time.sleep(5)
try:
    following_number = (
        WebDriverWait(driver, 15)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span",
                )
            )
        )
        .text
    )
    following_number = following_number.replace(",", "")
    following_number = int(following_number)
except:
    print("No following number")
    driver.quit()
    sys.exit()
# print(following_number)

# like the first post of the all the following accounts
# find the first post of the first account
driver.get(f"https://www.instagram.com/{username_insta}/following/")
time.sleep(5)
count = 0
for i in range(1, int(following_number)):
    try:
        followings = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[*]/div[2]/div[1]/div/div/span/a/span/div",
                )
            )
        )
        # followings = driver.find_elements_by_xpath(
        #     "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[*]/div[2]/div[1]/div/div/span/a/span/div"
        # )
        driver.execute_script("arguments[0].scrollIntoView(true);", followings[count])
        if count % 3 == 0:
            time.sleep(3)
        count += 1
    except:
        # print("Error finding followings")
        continue
        # driver.quit()

following_list = []
count = 0
for following in followings:
    following_text = following.text
    if "\nVerified" in following_text:
        following_text = following_text.replace("\nVerified", "")
    following_list.append(following_text)
# print(following_list)

# for i in following_list:
#     # open the first account and like the first post
#     driver.get(f"https://www.instagram.com/{i}")
#     time.sleep(5)
#     # scroll down to load the post
#     driver.execute_script("window.scrollTo(0, 200);")
#     # find the first post of the first account
#     first_post_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a"
#     try:
#         first_post = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, first_post_xpath))
#         )
#     except:
#         print(i, "first post not found")
#         continue

#     first_post.click()
#     time.sleep(5)
#     # like the first post
#     like_xpath = "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button/div[1]/svg"
#     try:
#         like = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, like_xpath))
#         )
#     except:
#         # print(i, "like button not found")
#         continue
#     like.click()
#     time.sleep(5)

for i in following_list:
    # open the first account and like the first post
    driver.get(f"https://www.instagram.com/{i}")
    time.sleep(5)
    try:
        soup = bs(driver.page_source, "html.parser")
        # links = soup.find_all('a', class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd")
        link_new = soup.find_all("div", class_="_aabd _aa8k _aanf")
        links_ = link_new[0].find_all("a")
        link = links_[0]["href"]
        driver.get(f"https://www.instagram.com{link}")
        time.sleep(5)
        # like the first post
        like_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
        try:
            like = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, like_xpath))
            )
        except:
            # print(i, "like button not found")
            continue
        like.click()
        time.sleep(5)
    except:
        print(i, "first post not found")
        continue

driver.close()
