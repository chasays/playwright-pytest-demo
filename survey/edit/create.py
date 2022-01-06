# @Time : 2021/4/18 
# @Author : xiaorik


import allure
from core.elements import *
from core.page import WebPage
from globaldata.data import G
from utils.tools import random_str, generate_pic


class CreateButtons(WebElement):

    def __init__(self, page: Page, selector):
        super().__init__(page, selector=selector, element=None)


class CreatePage(WebPage):

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        if not base_url:
            base_url = G.SURVEY_URL
        self.base_url = base_url
        self.s = lambda css: self.page.query_selector(css)

    @allure.step('Open survey_add_survey_page')
    def open(self):
        self.page.goto(G.ADD_URL, wait_until="networkidle")
        return self

    # Define wrapped Playwright Elementsconsole.log();
    @allure.step('Click create_basic_survey')
    def ques_basic_items(self) -> WebElementsCollection:  # 基础题型
        return elc(self.page, elements=ss(self.page, "#pane-questions > ul:nth-child(2) > li"),
                   element_container=CreateButtons)


    @allure.step('Upload heatmap picture')
    def upload_heatmap_picture(self):
        # 热力图图片上传
        self.heatmap_field().click()
        if self.heatmap_upload_field().is_visible():
            with self.page.expect_file_chooser() as fc_info:
                self.heatmap_upload_field().click()
            file_chooser = fc_info.value
            generate_pic()  # 生成一张临时图片
            file_chooser.set_files(G.TMP_PIC_PATH)
            time.sleep(1.5)
        else:
            self.upload_heatmap_picture()

    @allure.step('Click create empty field')
    def create_empty(self, title):
        self.create_empty_field().click()
        self.empty_text_filed().should_be_visible()
        self.empty_text_filed().click()
        self.pop_up_filed().should_be_visible()
        if title:
            self.input_name_field().val(title)
            self.create_button_field().click()
            self.tab_questions().should_be_visible()
            G.SURVEY_ID = self.page.url.split('surveyId=')[1]
        return self

    @allure.step('Add the all of basic questions')
    def add_basic_questions(self):
        items = self.ques_basic_items()
        for item in items.elements:
            item.click()
            time.sleep(0.3)

    @allure.step('Add the all of advanced questions')
    def add_advanced_questions(self):
        items = self.ques_advanced_items()
        for item in items.elements:
            item.click()
            time.sleep(0.3)

    def add_all_ques(self):
        self.add_basic_questions()
        self.add_advanced_questions()

    @allure.step('Add the single choice item')
    def add_single_option(self):
        self.add_identify_filed().click()

    @allure.step('Add the identify item')
    def add_identify(self):  # 甄别题
        self.add_identify_filed().click()

    """the editor field"""

    def cascade_txt(self):
        return el(self.page, selector='text=级联题')

    def survey_total(self):
        """检查总题是否正确"""
        return el(self.page, selector=f'text={G.QUESTION_TOTAL}.')

    
   

    @allure.step('Add the cascade item with uploading')
    def upload_item_cascade(self):
        # click preview and show cascade_upload
        self.cascade_preview_field().click()
        with self.page.expect_file_chooser() as fc_info:
            self.cascade_upload_field().click()
        file_chooser = fc_info.value
        file_chooser.set_files(G.CASCADE_TEMPLATE)
        time.sleep(1)



    """survey setting"""
    @allure.step('Set aim total number')
    def set_aim_total(self):
        self.aim_total_field()
        self.aim_total_field().val(random_str())
        timeout = 0
        while self.plan_number_msg_field().is_visible():
            self.aim_total_field().val(random_str())
            timeout += 1
            time.sleep(1)
            if timeout == 10:
                break

    """collect setting"""

    @allure.step('Set field to checked')
    def click_checked_field(self, field):
        timeout = 0
        while field.is_visible():
            field.click()
            timeout += 1
            if timeout == 10 or field.is_checked():
                break

    @allure.step('Set field to be chosen')
    def click_chosen_field(self, field, field2):
        """
        选择某一区域，直到选中之后field2可见
        """
        timeout = 0
        while field.is_visible():
            field.click()
            timeout += 1
            if timeout == 10 or field2.is_visible():
                break

    @allure.step('Click submit_button')
    def click_submit(self):
        with self.page.expect_navigation():
            self.page.click('button:has-text("提交")')
        # return el(self.page, selector='text=提交')
