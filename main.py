from selenium import webdriver
import time
from fuck.config import load_config

driver = webdriver.Chrome()
LOGIN_URL = "http://student.zjedu.moocollege.com/system/login?url=http%3A%2F%2Fstudent.zjedu.moocollege.com%2F"
MUTE_JS = 'document.getElementsByTagName("video")[0].muted=true;'

config = load_config()
college_name = config['college_name']


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
        username = config['username']
        password = config['password']

        self.login(username, password)
        block_until_appear('//*[@id="app"]/div/div/div/div[1]/div[1]/div[1]/ul/li[2]')
        time.sleep(2)
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
        cur_type = self.judge_type()
        hook = {
            'TEXT': self.next_text,
            'VIDEO': self.next_video
        }
        hook[cur_type]()

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

    def judge_type(self):
        cur_div = driver.find_element_by_xpath('//div[@aria-selected="true"]')
        try:
            cur_div.find_element_by_xpath('div//i[@class="anticon anticon-video-camera"]')
            return 'VIDEO'
        except:
            cur_div.find_element_by_xpath('div//i[@class="anticon anticon-file-text"]')
            return 'TEXT'

    def refresh(self):
        driver.refresh()


if __name__ == '__main__':
    fuck()
