from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from contextlib import contextmanager
from fuck.config import load_config
import datetime

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')

LOGIN_URL = "http://student.zjedu.moocollege.com/system/login?url=http%3A%2F%2Fstudent.zjedu.moocollege.com%2F"
MUTE_JS = 'document.getElementsByTagName("video")[0].muted=true;'

config = load_config()
college_name = config['college_name']


@contextmanager
def fuck_manage():
    global driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
        yield fuck()
    finally:
        driver.close()

def print_with_time(*args):
    print('[{}]'.format(datetime.datetime.now()),*args)

def exist(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def block_until_appear(xpath):
    while not exist(xpath):
        time.sleep(0.1)


def block_until_valid(xpath, validation):
    while driver.find_element_by_xpath(xpath).text != validation:
        time.sleep(0.1)


class fuck:
    def __init__(self):
        self.username = config['username']
        self.password = config['password']

    def start(self):
        self.login(self.username, self.password)
        block_until_appear('//*[@id="app"]/div/div/div/div[1]/div[1]/div[1]/ul/li[2]')
        time.sleep(2)
        print_with_time('账号 「{}」 登陆成功'.format(self.username))
        driver.get('http://student.zjedu.moocollege.com/course/study/30002920')  # 暂时只支持马原
        self.enter_video()
        block_until_appear('//div[@aria-selected="true"]')
        while 1:
            time.sleep(4)
            self.next()

    def login(self, username, password):
        driver.get(LOGIN_URL)

        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div[1]/div[2]/div/div/div[1]/ul/li[2]').click()  # 点击 学号登录

        college_input = driver.find_element_by_xpath('//*[@id="orgId"]')  # 找到院校框
        college_input.send_keys(college_name)  # 填进信息

        block_until_appear('/html/body/div[2]/div/div/div/ul/li')
        block_until_valid('/html/body/div[2]/div/div/div/ul/li', college_name)
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div/ul/li').click()  # 选择第一个
        # 如果院校名称第一个匹配不到那么说明配置有问题

        driver.find_element_by_xpath('//input[@id="userName"]').send_keys(username)
        driver.find_element_by_xpath('//input[@id="passWord"]').send_keys(password)
        driver.find_element_by_xpath('//button[@type="submit"]').click()  # 点击登录

    # def find(self, course):
    #     driver.find_element_by_xpath('//input[@placeholder="搜索课程"]').send_keys(course)
    #     driver.find_element_by_xpath('//div[@class="course-home"]//button').click()  # 点击搜索
    #     # 在class为course-home的div下第一个button就是搜索按钮
    #     # 结果应该只有一个元素 --> 配置里面要写全部的名称

    # def enter_course(self):
    #     ENTER_COURSE_XPATH = '//div[@class="course-home"]//button'
    #     block_until_appear(ENTER_COURSE_XPATH)
    #     driver.find_elements_by_xpath(ENTER_COURSE_XPATH)[-1].click()

    def enter_video(self):
        PROCESS_XPATH = '//a[text()="学习进度"]'
        ENTER_VIDEO_XPATH = '//button[span/text()="继续学习"]'

        block_until_appear(PROCESS_XPATH)
        driver.find_element_by_xpath(PROCESS_XPATH).click()

        time.sleep(2)

        block_until_appear(ENTER_VIDEO_XPATH)
        driver.find_element_by_xpath(ENTER_VIDEO_XPATH).click()

    def next(self):
        cur_type, cur_name = self.extract_type_and_name()
        if cur_type == 'TEXT':
            print_with_time('进入文字类课程 「{}」'.format(cur_name))
        else:
            print_with_time('进入视频类课程 「{}」'.format(cur_name))
        hook = {
            'TEXT': self.next_text,
            'VIDEO': self.next_video
        }
        hook[cur_type]()
        print_with_time('完成课程 {}'.format(cur_name))
        time.sleep(2)
        self.refresh()

    def next_text(self):
        driver.find_element_by_xpath('//button[span/text()="完成学习"]').click()

    def next_video(self):
        self.mute()
        NEXT_BUTTON = '//button[span/text()="继续学习"]'
        block_until_appear(NEXT_BUTTON)
        driver.find_element_by_xpath(NEXT_BUTTON).click()

    def mute(self):
        driver.execute_script(MUTE_JS)

    def extract_type_and_name(self):
        cur_div = driver.find_element_by_xpath('//div[@aria-selected="true"]')
        cur_name = cur_div.find_element_by_xpath('div//span').text
        try:
            cur_div.find_element_by_xpath('div//i[@class="anticon anticon-video-camera"]')
            return ('VIDEO', cur_name)
        except:
            cur_div.find_element_by_xpath('div//i[@class="anticon anticon-file-text"]')
            return ('TEXT', cur_name)

    def refresh(self):
        driver.refresh()


if __name__ == '__main__':
    with fuck_manage() as f:
        f.start()
