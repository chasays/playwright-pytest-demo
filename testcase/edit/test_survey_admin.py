# @Time : 2021/4/19 
# @Author : xiaorik
import pytest
from playwright.sync_api import Page
from survey.smanager.smanager import ManagerPage
from globaldata.data import G
from utils.logger import logger


@pytest.mark.only_browser("chromium")
def test_find_all_buttons(page: Page):
    pass


@pytest.mark.only_browser("chromium")
def test_admin(login_fixture):
    page = login_fixture
    admin = ManagerPage(G.SMANAGER_URL, page)
    admin.open()
    admin.survey_reviewed('1540306')


def test_console(login_fixture):
    url = 'https://domainname.com'
    page  = login_fixture
    admin = ManagerPage(url, page)
    admin.open()
    page.on('console', lambda msg:logger.info(msg.text))



if __name__ == '__main__':
    pytest.main(["-q", "-k", "test_console", "--headed", "--env", "pre", "--alluredir",
                 G.ALLURE_PATH])
