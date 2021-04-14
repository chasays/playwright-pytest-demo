from survey.elements import *


class Survey(object):
    def __init__(self, page: Page):
        self.page = page

    def delete_cookies(self):
        self.page.context.clear_cookies()

    def reload(self):
        self.page.reload(wait_until="load")
