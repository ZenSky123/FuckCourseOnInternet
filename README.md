# 自动刷浙江省高等学校在线开放课程共享平台网课

学校马原要在这个学校刷网课，So stupid。


## 使用方法

### 傻瓜版
自行安装chrome最新版

进入[release](https://github.com/ZenSky123/FuckCourseOnInternet/releases/tag/0.1)，下载 `FCO_v0.1.rar`。[微云链接](https://share.weiyun.com/5Q5gZgh)

解压文件并进入目录，啥都不要动

最简单方式：双击`start.bat` ，跟随配置。

```text
请输入您的学校名称（学校全称！例如：杭州师范大学）：[您的学校名称]
请输入您的学号：[您的学号]
请输入您的密码：[您的密码]
配置生成成功！

[自动运行程序]
```

进阶：

命令行下：

- `manage init` 进行初始化配置，输入学校名称，学号和密码
- `main` 开始刷课

## 程序员版
需要安装最新版Chrome，并自行配置chromedriver（也可以在[release](https://github.com/ZenSky123/FuckCourseOnInternet/releases/tag/0.1)中下载）
```text
git clone https://github.com/ZenSky123/FuckCourseOnInternet.git
cd FuckCourseOnInternet
pip install -r requirements.txt     安装依赖库
python manage.py init               初始化配置
python main.py                      开始！
```

## Todo
- 去掉各种愚蠢的time.sleep

## Develop Log
- 2018年5月22日
    - 完成基本功能
    - 代码中使用了很多hard code，待优化。
- 2018年5月23日
    - 增加交互界面配置生成
    - 自动检测配置进入对应学校页面
    - 使用headless模式
    - 增加友好交互输出
    - 提高chrome日志输出等级