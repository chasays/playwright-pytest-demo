# @Time : 2021/4/10
# @Author : xiaorik

import os


class GlobalData():
    # 基础url、问卷等
    SURVEY_URL = 'http://survey.domainname.com'
    ANSWER_ROOT_URL = 'http://answer.domainname.com'
    SMANAGER_URL = 'http://smanager.domainname.com'
    OBTAIN_TMPURL = 'http://smanager.domainname.com/survey/generateTempUrl?surveyId='
    DEL_ID = 'http://smanager.domainname.com/survey/deleteSurvey?surveyId='
    GET_ANSWER_URL = 'http://smanager.domainname.com/survey/getAnswerLink?surveyId='
    ADD_URL = f'{SURVEY_URL}/survey/add.htm'
    SURVEY_ID = '1502239'
    TEMP_URL = ''
    ANSWER_URL = ''
    QUESTION_TOTAL = 16
    CUR_ENV = 'test'

    # 文件路径等
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    RESULT_PATH = os.path.join(BASE_PATH, 'result')
    DATA_PATH = os.path.join(BASE_PATH, 'globaldata')
    TMP_PIC_PATH = os.path.join(DATA_PATH, 'temp_pic.png')
    LOG_PATH = os.path.join(RESULT_PATH, 'logs')
    ALLURE_PATH = os.path.join(RESULT_PATH, 'report')
    SNAPSHOT_PATH = os.path.join(RESULT_PATH, 'screenshots')
    DIFF_SNAP_PATH = os.path.join(RESULT_PATH, '__screenshots__')
    VIDEO_PATH = os.path.join(RESULT_PATH, 'video')
    STATE_JSON = os.path.join(DATA_PATH, 'state.json')
    for item in (LOG_PATH, SNAPSHOT_PATH, VIDEO_PATH):
        if not os.path.exists(item):
            os.mkdir(item)

    USERNAME = b'todo_username' # todo base64 encrypt
    PASSWORD = b'test_password='

    PCVIEWPORT = {
        'width': 1366,
        'height': 768,
    }

    MVIEWPORT = {
        'width': 375,
        'height': 812,
        'isMobile': True
    }

    HEADLESS = False
    DEV_TOOLS = False
    ignoreHTTPSErrors = True

    # example excel data
    CASCADE_TEMPLATE = os.path.join(DATA_PATH, '5.xlsx')
    IC_TEMPLATE = os.path.join(DATA_PATH, '6.xlsx')
    NPS_TEMPLATE = os.path.join(DATA_PATH, '1.csv')
    CITY_NEW_TEMPLATE = os.path.join(DATA_PATH, '2.xlsx')
    CITY_OLD_TEMPLATE = os.path.join(DATA_PATH, '3.xlsx')
    PROVINCE_TEMPLATE = os.path.join(DATA_PATH, '4.xlsx')

    # 问卷固定 url 等，比如防伪溯源



G = GlobalData()

if __name__ == '__main__':
    print(G.BASE_PATH, G.SNAPSHOT_PATH, G.LOG_PATH)
