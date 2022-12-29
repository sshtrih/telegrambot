import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from parametrs import SearchParameters
from res import EXE_PATH, url


class DataEntrant:

    def __init__(self):
        self.frame_places = None
        self.places = None
        self.subjects = {'Математика': ['10', None], 'Русский язык': ['0', None], 'Обществознание': ['1', None],
                         'Иностранный язык': ['2', None], 'ИКТ': ['3', None], 'Биология': ['4', None],
                         'География': ['5', None],
                         'Химия': ['6', None], 'Физика': ['7', None], 'Литература': ['8', None], 'История': ['9', None]}
        self.flags = {'Медаль': [False], 'ГТО': [False], 'Волонтерство': [False]}

        my_service = Service(EXE_PATH)

        self.driver = webdriver.Chrome(service=my_service)
        self.driver.maximize_window()
        self.driver.get(url)

        self.selection_from_the_list = self.driver.find_elements(By.CLASS_NAME, 'w100mobile')
        self.id_sub = self.driver.find_elements(By.TAG_NAME, 'input')
        self.id_flag = self.driver.find_element(By.CLASS_NAME, 'dop').find_elements(By.TAG_NAME, 'table')

    def get_subjects(self):
        subjects = ''
        for i in self.subjects:
            subjects += f'{i}\n'
        return subjects

    def get_active_subjects(self):
        subject = [[i, self.subjects[i][1]] for i in self.subjects.keys() if self.subjects[i][1] is not None]
        return subject

    def get_active_achievements(self):
        achievements = [i for i in self.flags.keys() if self.flags[i][0] is not False]
        return achievements

    def search(self):
        self.driver.find_element(By.CLASS_NAME, 'link5margin').click()
        time.sleep(3)
        return self.__parsing()

    def __search_id_sub(self, sub):
        new_letter = filter(lambda x: x.get_property('name') == f'ege{self.subjects[sub][0]}', self.id_sub)
        new_letter.__next__().send_keys(f'\b\b\b{self.subjects[sub][1]}')

    def add_point(self, sub_name, point):
        if sub_name not in self.subjects.keys():
            return False
        else:
            self.subjects[sub_name][1] = point
            self.__search_id_sub(sub_name)
            return True

    def add_flag(self, flag_name):
        if flag_name not in self.flags.keys():
            return False
        else:
            self.flags[flag_name][0] = True
            self.__search_id_flag(flag_name)
            return True

    def __search_id_flag(self, flag_name):
        for i in self.id_flag:
            if flag_name == i.text:
                i.click()

    def __parsing(self):
        for i in range(2):
            try:
                self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[5]').click()
            except:
                break
            time.sleep(2)
        with open('data.txt', 'w', encoding='utf-8') as f:
            f.write(self.driver.find_element(By.ID, 'resultdiv').text)
        with open('data.txt', 'r', encoding='utf-8') as r:
            result = r.readlines()
            if sum(1 for line in result) > 10:
                return SearchParameters().find_parameters()
            else:
                return '\n'.join(result).replace('\n\n', '\n')

    def open_places_console(self):
        self.selection_from_the_list[3].click()
        self.frame_places = self.driver.find_element(By.CSS_SELECTOR, '#popup2 > div')
        frame_result = self.frame_places.find_element(By.ID, 'resultdiv2')
        time.sleep(1)
        self.places = frame_result.find_elements(By.TAG_NAME, 'a')

    def add_place(self, place_id):
        # with open('places_with_code.txt', 'w') as f:
        #     for i in places[1:]:
        #         result = re.search(r'(\d{4})\',\'([^\']+)', i.get_attribute('onclick'))
        #         f.write(f'{result.group(1)}:{result.group(2)}\n')
        new_list = list(filter(lambda x: x.get_attribute('onclick')[34:38] == place_id, self.places))
        new_list[0].click()
        self.frame_places.find_element(By.XPATH, '//*[@id="popupcontent2"]/div[1]/div/img').click()
