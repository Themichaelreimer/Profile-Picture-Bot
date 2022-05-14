import requests
import tarfile
import io
import os
from typing import Tuple
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from generate_picture import generate_todays_pic, OUT_PATH

WEBDRIVER_URL = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz"
EXPECTED_PIC_NAME = OUT_PATH

def get_creds() -> Tuple[str,str]:
    """
        Extracts username and password from a file in the project root called '.secrets'
        which contains:
        USERNAME=USERNAME_HERE
        PASSWORD=PASSWORD_HERE
        :return: Tuple(username, password)
    """
    with open('.secrets', 'r') as cred_file:
        lines = cred_file.readlines()
        file_dict = {}
        for line in lines:
            kv = line.split("=")
            key = kv[0].strip()
            value = kv[1].strip()

            file_dict[key] = value
        return file_dict.get("USERNAME", ""), file_dict.get("PASSWORD", "")

def download_webdriver():
    print("Downloading webdriver...")
    req = requests.get(WEBDRIVER_URL)
    if req.status_code == 200:
        vfile = io.BytesIO(req.content)
        tf = tarfile.open(fileobj=vfile)
        tf.extractall()
        print("Complete!")
    else:
        raise Exception(f"Download failed! Request Code {req.status_code}: {req.text}")

def upload_new_pic(username:str, password:str):
    fpath = str(os.path.join(os.getcwd(), EXPECTED_PIC_NAME))
    driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(),"geckodriver"))
    
    # login ---------------------------------------------------
    try:
        driver.get("https://github.com/login")
        
        username_field = driver.find_element_by_id('login_field')
        password_field = driver.find_element_by_id('password')
        time.sleep(10)

        username_field.clear()
        username_field.send_keys(username)
        print(f"Sending keys ('{username}')")

        password_field.clear()
        password_field.send_keys(password)
        print(f"Sending keys ('{password}')")

        password_field.send_keys(Keys.RETURN)
        print(f"Sending keys ([RETURN])")
        time.sleep(5)

        # Navigate to profile, send file ---------------------------
        driver.get("https://github.com/settings/profile")
        time.sleep(5)

        # Need to open file dialog,
        # then send the right file path
        # then hit the submit button
        driver.find_element_by_xpath('//div[@class="position-absolute color-bg-default rounded-2 color-fg-default px-2 py-1 left-0 bottom-0 ml-2 mb-2 border"]').click()
        time.sleep(2)
        upload_button = driver.find_element_by_xpath('//label[@for="avatar_upload"]')
        upload = driver.find_element_by_xpath('//input[@type="file"]')
        time.sleep(2)
        upload.send_keys(fpath)
        time.sleep(4)

        save_button = driver.find_element_by_xpath('//button[@type="submit"and@name="op"and@value="save"]')
        save_button.click()


    except Exception as e:
        print(f"Exception --- {type(e)=}: {e}")
    finally:
        driver.close()

def main():
    if not os.path.exists("geckodriver"):
        download_webdriver()
    generate_todays_pic()

    creds = get_creds()
    upload_new_pic(creds[0], creds[1])

if __name__== "__main__":
    main()
