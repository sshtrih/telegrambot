import urllib.request
import os.path

from time import sleep

from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from res import EXE_PATH


class DirectionOfStudy:

    def __init__(self, name, profile, code, subdivision, university, passing_score):
        self.img = None
        self.name = name
        self.profile = profile
        self.code = code
        self.subdivision = subdivision
        self.university = university
        self.passing_score = passing_score

    def search_link(self):
        pass

    def search_picture(self):
        if not os.path.exists(f'image/{self.university}.png'):
            try:
                my_service = Service(EXE_PATH)
                key = " ".join([self.university, 'photo of the building'])
                url = f'https://www.google.ru/search?q={key}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'
                driver = webdriver.Chrome(service=my_service)
                driver.maximize_window()
                driver.get(url)
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]').click()
                sleep(10)
                elem = driver.find_element(By.CSS_SELECTOR, '#Sva75c')
                result = elem.find_element(By.XPATH,
                                           '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div['
                                           '2]/div/a/img')
                urllib.request.urlretrieve(result.get_attribute('src'), f'image/{self.university}.png')
            except:
                print(self.university)

