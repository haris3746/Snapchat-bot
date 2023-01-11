from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import warnings
import time
import undetected_chromedriver as uc
import re
from pymongo import MongoClient
import chromedriver_autoinstaller


warnings.filterwarnings("ignore")

options = uc.ChromeOptions()
options.add_argument('--headless')
path_chrome = chromedriver_autoinstaller.install()

driver = uc.Chrome(executable_path=path_chrome, options=options)
driver.maximize_window()

cluster = MongoClient(
    "mongodb+srv://user1:yes321@cluster0.m6tusxx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["snapchat"]
collection = db["initial"]

initial_data = list(collection.find())
n = len(initial_data)
# print(initial_data)
url = initial_data[n - 1]['url']
count = [1] * len(url)
set0 = [0] * len(url)
sub0 = [0] * len(url)
temp0 = [0] * len(url)
count1 = [0] * len(url)
sub = [0] * len(url)
initial_vidcount = [0] * len(url)
diff_vidcount = [0] * len(url)
initial_sub = [0] * len(url)
diff_sub = [0] * len(url)
last_vid = [""] * len(url)
thumbnail = [""] * len(url)
c_name = [""] * len(url)

out_count = 0

try:

    for i in range(0, len(url)):
        temp0[i] = initial_data[n - 1]['ini_vcount'][i]
        sub0[i] = initial_data[n - 1]['ini_sub'][i]
        count[i] = 1
        print(url[i])
        driver.get(url[i])
        time.sleep(4)
        try:
            print("Channel Name : ", driver.find_element(By.XPATH,
                                                         "/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[1]/a/h1/div/span").text)
            c_name[i] = driver.find_element(By.XPATH,
                                            "/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[1]/a/h1/div/span").text
            print(driver.find_element(By.XPATH,
                                      "/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[3]/div").text)
            t = driver.find_element(By.XPATH,
                                    "/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div/div/div[3]/div").text

        except:
            continue

        res = re.sub(r'[^a-zA-Z]', '', t)
        # print(res)
        num = re.findall(r'\d+(?:\.\d+)?', t)
        # print(res[0])
        # print(num[0])
        if res[0] == 'm':
            sub[i] = 1000000 * (float(num[0]))

        else:
            if res[0] == 'k':
                sub[i] = 1000 * (float(num[0]))
            else:
                sub[i] = float(num[0])

        try:
            for m in range(1, 1000, 5):
                driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located(
                        (By.XPATH,
                         '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                             m) + ']/div[2]/h4/span'))))
                # print(driver.find_element(By.XPATH,
                #             '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                #                i) + ']/div[2]/h4/span').text)
                time.sleep(3)
                count[i] = count[i] + 5

        except:
            # print(count)
            count1[i] = count[i] - 4

            for l in range(count1[i], count1[i] + 5):
                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                                            l) + ']/div[2]/h4/span')
                    count1[i] = count1[i] + 1
                except:
                    break

                # print(count1)

        count1[i] = count1[i] - 1
        print("Latest Video Title : ", driver.find_element(By.XPATH,
                                                           '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                                                               count1[i]) + ']/div[2]/h4/span').text)
        last_vid[i] = driver.find_element(By.XPATH,
                                          '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                                              count1[i]) + ']/div[2]/h4/span').text
        thumbnail[i] = driver.find_element(By.XPATH,
                                           '/html/body/div/div[1]/main/div[2]/div/div[2]/div/div[3]/div[3]/div[' + str(
                                               count1[i]) + ']/div[1]/img').get_attribute('src')

        time.sleep(2)
        # driver.quit()
        initial_vidcount[i] = count1[i]
        initial_sub[i] = sub[i]
        print("Initial Video count = ", count1[i])
        print("Initial subscribers = ", sub[i])

        diff_vidcount[i] = count1[i] - temp0[i]
        diff_sub[i] = sub[i] - sub0[i]
        print("Video Count Difference is : ", count1[i] - temp0[i])
        print("Subscribers Difference = ", sub[i] - sub0[i])














except:
    logging.exception('msg')

driver.quit()

ini_post = {"url": url, "channel": c_name, "ini_sub": initial_sub, "ini_vcount": initial_vidcount}
print(ini_post)
cluster = MongoClient(
    "mongodb+srv://user1:yes321@cluster0.m6tusxx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["snapchat"]
collection = db["initial"]
collection.insert_one(ini_post)
post = {"channel": c_name, "url": url, "last_video": last_vid, "diff_sub": diff_sub, "diff_vcount": diff_vidcount, "thumbnail": thumbnail}
print(post)
cluster = MongoClient(
    "mongodb+srv://user1:yes321@cluster0.m6tusxx.mongodb.net/?retryWrites=true&w=majority")
db = cluster["snapchat"]
collection = db["output1"]
collection.insert_one(post)
