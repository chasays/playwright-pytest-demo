# @Time : 2021/4/19 
# @Author : xiaorik
import pytest
import time
from survey.edit.create import CreatePage
from globaldata.data import G
from utils.tools import generate_random_str


@pytest.mark.smoke
def test_create_survey_empty_without_title(login_fixture, assert_snapshot, request):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty('')
    create.create_button_field().click()
    assert create.errormsg_field().is_visible()
    # 对比布局等
    assert_snapshot(page.screenshot(), f'{request.node.name}.png')


@pytest.mark.sanity
def test_create_survey_empty_with_title(login_fixture):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty(f'TEST_{generate_random_str()}_EMPTY')
    assert create.tab_questions().is_visible()


def test_create_survey_with_all_questions(login_fixture, assert_snapshot, request):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty(f'TEST_{generate_random_str()}_ALL')
    create.add_basic_questions()
    create.add_advanced_questions()
    create.add_item_cascade()
    create.cascade_txt().is_visible()
    create.survey_total().is_visible()
    # 对比布局、元素等 todo it took too long time, only skip
    # assert_snapshot(page.screenshot(), f'{request.node.name}.png')
    create.click_next_button()
    create.set_aim_total()
    create.click_next_button()
    create.free_collect_field().is_visible()
    create.free_collect_field().click()
    create.click_checked_field(create.anonymous_login_field())
    create.click_submit()
    assert 'editSurvey/surveyLink?surveyId=' in create.page.url


def test_case_next_and_submit(login_fixture):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty(f'TEST_{generate_random_str()}_ALL')
    create.add_single_option()
    create.click_next_button()
    create.click_next_button()
    create.set_aim_total()
    create.click_next_button()
    assert 'collect?surveyId=' in create.page.url
    create.free_collect_field().is_visible()
    create.free_collect_field().click()  # todo check with smanager
    create.click_checked_field(create.anonymous_login_field())
    create.click_submit()
    assert 'editSurvey/surveyLink?surveyId=' in create.page.url


@pytest.mark.run(order=1)
@pytest.mark.smoke
def test_all_next_and_submit(login_fixture, assert_snapshot, request):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty(f'TEST_{generate_random_str()}_ALL')
    # 添加所有题型
    create.add_basic_questions()
    create.add_advanced_questions()

    create.set_kpi_question()

    # 对题型增加选项，热力图和级联题
    create.upload_item_cascade()
    # create.add_item_cascade() #  级联题单个item增加
    create.upload_heatmap_picture()

    # 添加完成，下一步
    create.cascade_txt().is_visible()
    create.survey_total().is_visible()
    time.sleep(1)
    # 对比布局、元素等
    # assert_snapshot(page.screenshot(), f'{request.node.name}.png')
    create.click_next_button()
    assert 'logicSetting?surveyId=' in create.page.url

    create.click_next_button()
    assert 'surveySetting?surveyId=' in create.page.url
    create.set_aim_total()
    create.click_next_button()
    assert 'collect?surveyId=' in create.page.url
    create.free_collect_field().is_visible()
    # create.free_collect_field().click()  # todo check with smanager
    create.charge_collect_field().click()
    create.click_chosen_field(create.free_collect_field(), create.anonymous_login_field())
    create.click_checked_field(create.anonymous_login_field())
    create.click_submit()
    assert 'editSurvey' in create.page.url


def test_case_invalid(login_fixture):
    page = login_fixture
    create = CreatePage(G.ADD_URL, page)
    create.open().create_empty(f'TEST_{generate_random_str()}_ALL')
    time.sleep(1)
    # create.add_basic_questions()
    create.add_advanced_questions()
    create.set_kpi_question()
    # create.upload_item_cascade()
    create.click_next_button()


if __name__ == '__main__':
    pytest.main(["-q", "-k", "test_case_invalid", "--headed", "--env", "pre", "--alluredir",
                 G.ALLURE_PATH])
    # pytest.main(["-q", "-k", "test_case_invalid", "--headed", "--env", "pre", "--update-snapshots"])
