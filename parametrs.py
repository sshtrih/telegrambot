import re

from direction import DirectionOfStudy


class SearchParameters:

    def __init__(self):
        with open('data.txt', 'r', encoding="utf8") as r:
            self.f = []
            self.f = re.split(r'\n{4,}', r.read())
            self.direction_of_study = []

    def find_parameters(self):
        for i in range(len(self.f)):
            try:
                university = re.match(r'[\w.\- ()«»]*', self.f[i]).group(0)
                profile = re.search(r'Профиль:([\w\- ;."()«»]*)', self.f[i]).group(1)
                code = re.search(r'\d{2}\.\d{2}\.\d{2}', self.f[i]).group(0)
                subdivision = re.search(r'Подразделение:([\w "\-;.()«»]*)', self.f[i]).group(1)
                name = re.match(r'[\w.\- ()«»]*\n([\w.\-; ()«»]*)', self.f[i]).group(1)
                passing_score = re.search(r'\n\d{2,3}\n', self.f[i]).group(0)
                direction = DirectionOfStudy(name, profile, code, subdivision, university, passing_score)
                direction.search_picture()
                self.direction_of_study.append(direction)
            except AttributeError:
                print('Ошибка: ' + self.f[i])

        return self.direction_of_study
