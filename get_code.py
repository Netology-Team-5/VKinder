from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import re


def get_token_vk():
    service = Service(executable_path=EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.get("https://oauth.vk.com/authorize?client_id=51432598&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=stats,offline&response_type=token&v=5.131")
    WebDriverWait(driver, 240).until(ec.url_contains('https://oauth.vk.com/blank.html#access_token='))
    link_of_token = driver.current_url
    driver.close()
    required_token = re.sub(r"(^https://oauth.vk.com/blank.html#access_token=)([\w.-]*)(&.*)", r"\g<2>", link_of_token)
    return required_token


if __name__ == '__main__':
    print(get_token_vk())
