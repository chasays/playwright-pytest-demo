# @Time : 2021/4/19 
# @Author : xiaorik
import pytest
import time
from globaldata.data import G
from globaldata.survey import trace_back, answer_url, answer_ic_url
from survey.smanager.smanager import ManagerPage
from survey.answer.answer import AnswerPage
from utils.logger import logger


def test_answer_page(get_mobile_page, assert_snapshot, request):
    page = get_mobile_page
    mobile = AnswerPage(answer_url(), page)
    mobile.open()
    time.sleep(2)
    all_page = page.query_selector('id=app')
    assert_snapshot(all_page.screenshot(), f'{request.node.name}.png')


@pytest.mark.run(order=2)
@pytest.mark.smoke
def test_all_answer(get_mobile_page):
    page = get_mobile_page
    mobile = AnswerPage(answer_url(), page)
    mobile.open()
    mobile.select_all()
    page.on('console', lambda msg: logger.error(msg.text) if (msg.type == 'error' or
                                                              'null' in msg.text) else None)




@pytest.mark.run(order=4)
@pytest.mark.smoke
def test_verify_invalid_traceback(get_mobile_page, assert_snapshot, request):
    if trace_back()[1]:
        page = AnswerPage(trace_back()[1], get_mobile_page)
        page.open()
        all_page = get_mobile_page.query_selector('id=app')
        assert_snapshot(all_page.screenshot(), f'{request.node.name}.png')


@pytest.mark.smoke
def test_verify_ic(get_mobile_page, assert_snapshot, request):
    page = get_mobile_page
    manager = ManagerPage(G.SMANAGER_URL, page)
    ic_url = manager.obtain_tmp_url(answer_ic_url())
    if ic_url:
        answer = AnswerPage(ic_url, page)
        answer.open()
        all_page = page.query_selector('id=app')
        assert_snapshot(all_page.screenshot(), f'{request.node.name}.png')


if __name__ == '__main__':
    pytest.main(["-q", "-k", "test_verify_ic", "--headed", "--env", "pre", "--alluredir", G.RESULT_PATH])
    # pytest.main(["-q", "-k", 'test_all_answer', "--headed", "--env", "pre", "--update-snapshots", "--alluredir",
    # G.ALLURE_PATH])
