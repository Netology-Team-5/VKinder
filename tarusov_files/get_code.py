from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def get_token_vk():
    driver = webdriver.Firefox()
    driver.get("http://oauth.vk.com/authorize?client_id=51432598&scope=65536&redirect_uri=https://vk.com/im?media=&sel=-216114574&display=popup&response_type=token")
    WebDriverWait(driver, 240).until(ec.url_contains('https://api.vk.com/blank.html#access_token='))
    link_of_tocken = driver.current_url
    driver.close()
    required_token = link_of_tocken[43:-29]
    return required_token


if __name__ == '__main__':
        print(login_to_yandex())