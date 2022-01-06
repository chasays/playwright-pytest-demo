# @Time : 2021/4/18 
# @Author : xiaorik

from globaldata.data import G
from core.elements import *
from core.page import WebPage
import allure


class MainPage(WebPage):

    def account_button(self, username) -> WebElement: return el(self.page, selector='a[href="#@%s"]' % username)

    def login_button(self) -> WebElement: return el(self.page, selector='a[href="#login"]')

    def register_button(self) -> WebElement: return el(self.page, element=s(self.page, 'text="Sign up"'))

    def main_buttons(self) -> WebElementsCollection:
        return elc(self.page, elements=ss(self.page, "div > div.header__context > ul > li"),
                   element_container=MainButtons)

    # layout-header > div > div.header__context > ul > li:nth-child(1)

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        if not base_url:
            base_url = G.SURVEY_URL
        self.base_url = base_url

    # Open Survey Main Page
    @allure.step('Open main page')
    def open(self):
        self.page.goto(f"{self.base_url}", wait_until="networkidle")
        return self

    @allure.step("Press login button")
    def login(self):
        self.login_button().click()
        from survey.login import LoginPage
        return LoginPage(self.base_url, self.page)


class MainButtons(WebElement):

    def __init__(self, page: Page, selector):
        super().__init__(page, selector=selector, element=None)

    # 登录
    def home_button(self): return el(self.page, element=self.element.query_selector("text=登录"))

    def create_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(1) > a"))

    def example_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(2) > a"))

    def example_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(3) > a"))

    def scenario_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(4) > a"))

    def intro_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(5) > a"))

    def help_button(self): return el(self.page, element=self.element.query_selector("li:nth-child(6) > a"))

    # 我的问卷
    def login_button(self): return el(self.page, element=self.element.query_selector("li.pull-left.my-count.login > a"))

    def name(self): return el(self.page, element=self.element.query_selector("a"))
