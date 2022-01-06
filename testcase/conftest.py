# @Time : 2021/4/18 
# @Author : xiaorik

import pytest
import allure
import sys
from playwright.sync_api import Page, Browser, BrowserContext
from survey.login import LoginPage
from globaldata.data import G
from globaldata.user import login_user
from survey.smanager.smanager import ManagerPage
from typing import Generator, Dict, Any, Callable
from io import BytesIO
from pathlib import Path
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from utils.logger import logger


@pytest.fixture
def context(
        browser: Browser, browser_context_args: Dict, browser_name, video_path, request
) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)
    current_failed_tests = request.session.testsfailed
    yield context


# session and function
@pytest.fixture(scope="function")
def login_fixture(browser: Browser, request, env):
    if env:
        G.CUR_ENV = env
    state = LoginPage.cookie_is_exist()
    p: Page = browser.new_page(record_video_dir=f"{G.VIDEO_PATH}/", storage_state=state) \
        if state else browser.new_page(record_video_dir=f"{G.VIDEO_PATH}/")
    # 为了保存 cookie
    LoginPage(G.ADD_URL, p).open().login_with(login_user())
    yield p
    screenshot = p.screenshot(path=f"{G.SNAPSHOT_PATH}/{request.node.name}.png", full_page=True)
    video = p.video.path()
    # 获取答题链接
    manager = ManagerPage(G.SMANAGER_URL, p)
    manager.obtain_tmp_url()
    manager.survey_reviewed(G.SURVEY_ID)
    manager.get_answer_link()
    # 打印控制台的 error 日志
    p.on('console', lambda msg: logger.error(msg.text) if msg.type == 'error' else None)
    p.close()
    allure.attach(screenshot, name=f'{request.node.name}', attachment_type=allure.attachment_type.PNG)
    allure.attach.file(f'{video}', attachment_type=allure.attachment_type.WEBM)


@pytest.fixture(scope="function")
def get_multi_page(login_fixture):
    browser = login_fixture
    c = browser.new_context(record_video_dir="video/")
    p1 = c.new_page()
    p2 = c.new_page()
    yield p1, p2


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args, playwright):
    iphone_11 = playwright.devices['iPhone 11']
    return {
        **browser_context_args,
        **iphone_11,
        'record_video_dir': f"{G.VIDEO_PATH}/",
        'storage_state': LoginPage.cookie_is_exist()
    }


@pytest.fixture(scope="function")
def get_mobile_page(browser: Browser, request, browser_context_args, env):
    if env:
        G.CUR_ENV = env
    state = LoginPage.cookie_is_exist()
    context = browser.new_context(**browser_context_args)
    mobile: Page = context.new_page() if state else context.new_page()
    # todo implement for mobile login
    yield mobile
    # 打印控制台的 error 日志, 或者提交的数据里面有 null
    mobile.on('console', lambda msg: logger.error(msg.text) if (msg.type == 'error' or
                                                                'null' in msg.text) else None)  # todo raise
    screenshot = mobile.screenshot(path=f"{G.SNAPSHOT_PATH}/{request.node.name}.png", full_page=True)
    video = mobile.video.path()
    mobile.close()
    allure.attach(screenshot, name=f'{request.node.name}', attachment_type=allure.attachment_type.PNG)
    if Path(video).exists():
        allure.attach.file(f'{video}', attachment_type=allure.attachment_type.WEBM)



@pytest.fixture(scope="function")
def get_temp_url(login_fixture):
    page = login_fixture
    manager = ManagerPage(G.SMANAGER_URL, page)
    manager.obtain_tmp_url()
    yield


@pytest.fixture(scope='function')
def delete_sur():
    pass


# snapshot compare
# implement from pytest-playwright-snapshot
# and add img_diff output
@pytest.fixture
def assert_snapshot(pytestconfig: Any, request: Any, browser_name: str) -> Callable:
    def compare(img: bytes, name: str, *, threshold: float = 0.1) -> None:
        update_snapshot = pytestconfig.getoption("--update-snapshots")
        filepath = (
            # Path(request.node.fspath).parent.resolve()
                Path(G.DIFF_SNAP_PATH)
                / "__snapshots__"
                / browser_name
                / sys.platform
        )
        filepath.mkdir(parents=True, exist_ok=True)
        file = filepath / name
        if update_snapshot:
            file.write_bytes(img)
            return
        if not file.exists():
            pytest.fail("Snapshot not found, use --update-snapshots to update it.")
        image = Image.open(BytesIO(img))
        golden = Image.open(file)
        img_diff = Image.new("RGBA", image.size)
        diff_pixels = pixelmatch(image, golden, output=img_diff, threshold=threshold)
        img_diff.save(filepath / f'{name.split(".")[0]}_diff.png')  # 保存 diff 图片
        # assert diff_pixels == 0, "Snapshots does not match"
        assert diff_pixels <= 200, "Snapshots does not match"

    return compare


def pytest_addoption(parser: Any) -> None:
    # pass argument in pytest by command line
    parser.addoption("--env", action="store", default="test",
                     help="env where you will run, value is test, pre or product")
    parser.addoption("--update-snapshots", action="store_true", default=False, help="Update snapshots.")


# 注册env
def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.env
    if 'env' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("env", [option_value])
