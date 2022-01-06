# @Time : 2021/4/20
# @Author : xiaorik


import allure
from core.elements import *
from core.page import WebPage
from globaldata.data import G


class ManagerPage(WebPage):
    # Define wrapped Playwright Elements
    def __init__(self, base_url, page: Page):
        super().__init__(page)
        if not base_url:
            base_url = G.SMANAGER_URL
        self.base_url = base_url
        self.s = lambda css: self.page.query_selector(css)

    @allure.step('Open Smanager home_page')
    def open(self):
        self.page.goto(self.base_url, wait_until="networkidle")
        return self

    def survey_list(self) -> WebElement:
        return el(self.page, selector='text=问卷档案')

    @allure.step('Obtain temporary link')
    def obtain_tmp_url(self, survey_id=None):
        if not survey_id:
            if G.SURVEY_ID:
                survey_id = G.SURVEY_ID
        else:
            logger.warning(f'id is {survey_id}, this value maybe be from CreatePage.create_empty()')
        ret = self.page.goto(f'{G.OBTAIN_TMPURL}{survey_id}', wait_until="networkidle")
        url = ''
        if ret.status == 200:
            ret_json = ret.json()
            try:
                url = ret_json.get('messages').get('url')
            except Exception as e:
                logger.error(e)
        G.TEMP_URL = url
        if url:
            print(f'temp_url:{url}')
        return url

    @allure.step('Get answer link')
    def get_answer_link(self, survey_id=None):
        if not survey_id:
            if G.SURVEY_ID:
                survey_id = G.SURVEY_ID
        else:
            logger.warning(f'id is {survey_id}, this value maybe be from CreatePage.create_empty()')
        ret = self.page.goto(f'{G.GET_ANSWER_URL}{survey_id}', wait_until="networkidle")
        url = ''
        if ret.status == 200:
            ret_json = ret.json()
            try:
                url = ret_json.get('messages').get('mUrl')
            except Exception as e:
                logger.error(e)
        G.ANSWER_URL = url
        return url

    @allure.step('delete survey')
    def delete_survey(self, id=G.SURVEY_ID):
        ret = self.page.goto(f'{G.DEL_ID}{id}', wait_until="networkidle")
        logger.debug(f' {id} - {ret.text()}')

    @allure.step('Review survey')
    def survey_reviewed(self, id=None):
        review_url = 'http://xxxx.domainname.com/xxxxx'
        if not id:
            if G.SURVEY_ID:
                id = G.SURVEY_ID
        ret = self.page.goto(f'{review_url}{id}', wait_until="networkidle")
        if ret.status == 200:
            ret_json = ret.json()
            try:
                msg = ret_json['msg']
                logger.info(f'reviewed survey_id:{id}, {msg}')
            except KeyError as e:
                logger.info(f'reviewed survey_id:{id}, {ret_json.get("errorMsg")}')


if __name__ == '__main__':
    pass
