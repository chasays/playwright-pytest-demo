# @Time : 2021/4/18 
# @Author : xiaorik

import json
import os
import allure
from core.elements import *
from survey.main_page import MainPage
from core.page import WebPage
from globaldata.data import G
from globaldata.user import User


class LoginPage(WebPage):

    # Define wrapped Playwright Elements
    def login_field(self) -> WebElement:
        return el(self.page, selector='text=账户登录')
        # return el(self.page, selector='button.el-button.login-text.el-button--text.el-button--small > span')

    def login_box_field(self) -> WebElement:
        return el(self.page, selector='ldiv > div.login-box')

    def loginname_field(self) -> WebElement:
        return el(self.page, selector='#loginname')

    def nloginpwd_field(self) -> WebElement:
        return el(self.page, selector='#nloginpwd')

    def loginsubmit_field(self) -> WebElement:
        return el(self.page, selector='#loginsubmit')

    def logined_field(self) -> WebElement:
        return el(self.page, selector='text=我的问卷')
        # return el(self.page, selector='div.header__user-info > div > span > span')

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        if not base_url:
            base_url = G.SURVEY_URL
        self.base_url = base_url
        self.s = lambda css: self.page.query_selector(css)

    @staticmethod
    def cookie_is_exist():
        storage_state = ''
        if os.path.exists(G.STATE_JSON) and os.path.getsize(G.STATE_JSON):
            with open(G.STATE_JSON) as f:
                storage_state = json.loads(f.read())
        return storage_state

    def save_cookie(self):
        for i in range(5):
            time.sleep(1)
            # has_login = page.query_selector('li.pull-left.my-count > a')
            has_login = self.logined_field()
            if has_login and has_login.is_visible():  # save cookies
                storage = self.page.context.storage_state()
                with open(G.STATE_JSON, "w") as f:
                    f.write(json.dumps(storage))
                break

    # Open Login Page
    @allure.step("Open login home page")
    def open(self):
        self.page.goto(self.base_url, wait_until="networkidle")
        return self

    @allure.step('Ready to login')
    def ready_login(self):
        if self.login_field():
            # self.login_field().click() # http->https
            self.page.goto('domainname.com', wait_until="networkidle")
            for i in range(6):
                self.page.click('text=账户登录')
                if self.login_box_field().is_visible():
                    break
                time.sleep(1)

    @allure.step('Check whether login or not')
    def has_login(self):
        # text=账户登录,还可以看到说明cookie失效了，需要重新登录
        if self.login_field().is_visible():
            return False
        else:
            return True

    @allure.step('Login user with usr: "{username}", pwd: "******"')  # hidden passwd
    def login(self, username, password):
        """
            1. 判断cookie文件是否为空，建议第一次里面的数据： globaldata/state.json
            2. 登录之后缓存会存到这个json文件
            3. 第二次之后的登录就可以检测 logined_field 这个区域的值
        """
        if not self.has_login():
            self.ready_login()
            self.loginname_field().val(username).press_tab()
            self.nloginpwd_field().val(password).press_enter()
            self.loginsubmit_field()
            self.save_cookie()
        return MainPage(self.base_url, self.page)

    @allure.step('Login with user: "{1}"')
    def login_with(self, user: User):
        return self.login(user.username, user.password)
