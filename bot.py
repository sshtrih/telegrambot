from parsing import DataEntrant


class CalculatorBot:

    def __init__(self):
        self.new_search = None
        self.response_status = None
        self.active_achievement = None
        self.active_subject = None
        self.search_result = None
        self.subjects = None

    def new_request(self):
        self.active_achievement = None
        self.active_subject = None
        self.search_result = None
        self.subjects = None
        self.new_search = DataEntrant()
        self.response_status = False

    def get_subject(self):
        self.subjects = self.new_search.get_subjects()

    def search(self):
        result = self.new_search.search()
        try:
            self.search_result = sorted(result, key=lambda x: x.passing_score, reverse=True)
        except:
            self.search_result = result

    def get_active_achievement(self):
        self.active_achievement = self.new_search.get_active_achievements()

    def add_place(self, place_id):
        self.new_search.add_place(place_id)

    def get_active_subject(self):
        self.active_subject = self.new_search.get_active_subjects()

    def show_search_result(self, n=0):
        flag_end = False
        mess = []
        if isinstance(self.search_result, str):
            return False
        else:
            if n > len(self.search_result) - 1:
                return mess, True
            elif n + 5 > len(self.search_result) - 1:
                directions = [i for i in self.search_result[n: len(self.search_result)]]
                flag_end = True
            else:
                directions = [i for i in self.search_result[n:n + 5]]
            for i in directions:
                n += 1
                mess.append([i.university, i.name, i.profile.strip(), i.subdivision.strip(), i.code, i.passing_score])
            return mess, flag_end

    def start(self):
        self.new_search = DataEntrant()
