"""Init Config
Usage:
    manage.py init

Options:
    init        Initialize your config.
"""

from docopt import docopt
from fuck.config import init_config

def init():
    college_name=input('请输入您的学校名称（学校全称！例如：杭州师范大学）：')
    username=input('请输入您的学号：')
    password=input('请输入您的密码：')
    init_config({
        'college_name':college_name,
        'username':username,
        'password':password
    })
    print('配置生成成功！')


if __name__ == '__main__':
    arguments=docopt(__doc__,version="temp config 0.01")
    if arguments['init']:
        init()