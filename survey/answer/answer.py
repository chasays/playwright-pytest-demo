# @Time : 2021/4/18 
# @Author : xiaorik


import allure
from core.elements import *
from core.page import WebPage
from globaldata.data import G
from utils.tools import generate_any, generate_pic, random_int, random_str


class AnswerChoice(WebElement):

    def __init__(self, page: Page, selector):
        super().__init__(page, selector=selector, element=None)


class AnswerPage(WebPage):

    # Define wrapped Playwright Elements
    @allure.step('Click create-survey')
    def trap_field(self, valid=True) -> WebElement:
        if valid:
            return el(self.page, selector='text=西施')
        else:
            return el(self.page, selector='text=东施')

    @allure.step('Obtain Option_radio')
    def option_radios(self) -> WebElementsCollection:
        # 获取所有的radio
        return elc(self.page, elements=ss(self.page, "label > div.m-option__radio > input"),
                   element_container=AnswerChoice)

    def __init__(self, base_url, page: Page):
        super().__init__(page)
        if not base_url:
            base_url = G.ANSWER_URL
        print(G.ANSWER_URL)
        self.base_url = base_url
        self.s = lambda css: self.page.query_selector(css)

    # action
    @allure.step('open the add survey page')
    def open(self):
        self.page.goto(self.base_url, wait_until="networkidle")
        return self


    @allure.step('Select trap')
    def fill_input(self): # 填空题
        # 填写填空题， 内容为随机一串字符串
        items = self.option_inputs()
        for item in items.elements:
            item.fill(generate_any('text'))


    @allure.step('Select sort question')
    def select_sort(self): # 涉及到拖动
        # 选择排序题
        self.sort_field().scroll_into_view_if_needed()
        bounding = self.sort_field().element.bounding_box()
        bounding_x = bounding.get('x', 0)
        bounding_y = bounding.get('y', 0)
        if bounding_y and bounding_x:
            self.page.mouse.move(bounding_x + 2, bounding_y + 2)
            self.page.mouse.down()
            self.page.mouse.move(bounding_x, bounding_y + 200)
            self.page.mouse.up()
        # 检查是否选中, 没有就继续执行
        if not self.sorted_field().is_visible():
            self.select_sort()

    @allure.step('Upload picture')
    def upload_picture(self): # 上传文件
        # 图片上传提
        with self.page.expect_file_chooser() as fc_info:
            self.upload_field().click()
        file_chooser = fc_info.value
        generate_pic()  # 生成一张临时图片
        file_chooser.set_files(G.TMP_PIC_PATH)
        time.sleep(1)



    @allure.step('Select heatmap')
    def select_heatmap(self):  # 点击
        # 调到热力图，避免鼠标click到其他地方
        self.click_submit(check=False)
        # 热力图
        heatmap = self.heatmap_field()
        heatmap.scroll_into_view_if_needed()
        if heatmap.is_visible():
            bounding = heatmap.element.bounding_box()
            heat_x = bounding.get('x', 0)
            heat_y = bounding.get('y', 0)
            # 0.95和3，尽量保证没有选到最边上
            width = int(bounding.get('width', 0) * 0.95)
            height = int(bounding.get('height', 0) * 0.95)
            for i in range(3):  # 随机点击3处
                random_x = heat_x + random_int(width) + 3
                random_y = heat_y + random_int(height) + 3
                self.page.mouse.click(random_x, random_y)
                print(f'选中的坐标是[{random_x}, {random_y}]')
                time.sleep(1)
        if not self.heatmap_position_field().is_visible():
            self.select_heatmap()

    @allure.step('Click Next or submit buuton')
    def click_submit(self, check=True):
        # check 参与用于调到某题上
        self.next_and_submit().click()
        # 直到end-page出现
        if check:
            self.page.wait_for_selector('.answer-tab-page.end-page', state='visible')

    @allure.step('Start selecting...')
    def select_all(self):
        # 选择所有的radio类型题
        pass

    @allure.step('Obtain temporary link')
    def obtain_tmpUrl(self):
        # 在 sManager 里面实现，不知道后端怎么弄的，编辑端不支持get方法获取
        # implement in case todo
        pass
