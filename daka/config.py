# 自动化打卡部分
# 登录获取会话地址
GET_SESSION_URL = "http://qy.zjhzcc.edu.cn/ami/ihs.php/Index/icon_yqtb/id/27/_sign/5E29795015AFD5127A14DFA86A579F7140B159F3/wtype/student/_time/_time.html"

# 表单提交地址
POST_SUBMIT_URL = "http://qy.zjhzcc.edu.cn/ami/ihs.php/Index/icon_yqtb/id/27/_sign/5E29795015AFD5127A14DFA86A579F7140B159F3/wtype/student/_time/_time.html"

# 打卡头
DAKA_HEADERS = {
    "Host": "qy.zjhzcc.edu.cn",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 wxwork/4.0.12 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark"
}


# DATABASE
DATABASE_CONFIG = {
    "HOST": "124.221.102.241",
    "USER": "root",
    "PASSWORD": "lzy0812..",
    "DATABASE": "hangshangyuan",
    "PORT": 3306
}


# status
STATUS = {
    0: "OK",
    1: "表单不完整",
    2: "OAUTH_CODE无效",
    3: "尝试唤醒会话失败, PHPSESSID失效",
    9: "尝试唤醒会话失败, 未知情况"
}

STATUS_MESSAGE = {
    0: "表单完整有效",
    1: "表单不完整, 请尝试重新拉取表单",
    2: "OAUTH_CODE无效",
    3: "PHPSESSID失效",
    9: "会话失败, 未知情况"
}