# 一个数据库管理类以及若干工具函数
import os
import re
import pymysql
import requests
import config
import time

from bs4 import BeautifulSoup


def printLog(msg):
    print(f"[{time.strftime('%Y/%m/%d %H:%M:%S')}][{os.getpid()}] {msg}")


class Database:
    def __init__(self):
        self.databaseConfig = config.DATABASE_CONFIG
        self.connection = self.connect()

    def connect(self):
        connection = pymysql.connect(
            host = self.databaseConfig["HOST"],
            user = self.databaseConfig["USER"],
            password = self.databaseConfig["PASSWORD"],
            database = self.databaseConfig["DATABASE"],
            port = self.databaseConfig["PORT"],
            charset = 'utf8',
            autocommit = True
        )
        printLog("Database connected")
        return connection

    def getCursor(self):
        self.connection.ping(True)
        return self.connection.cursor()

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        printLog("Database disconnect PID:" + str(os.getpid()))


def getOauthCode(url: str):
    """
    从打卡页面链接url中提取oauth_code

    :param url: 企业微信打卡页面链接
    :return:
    """
    r = re.search(r"(?<=code/).*?(?=/|\.html)", url)
    return r.group() if r is not None else False


def getSession(oauth_code: str):
    """
    获取SESSION(PHPSESSID)
    获取成功将会返回 response.content便于下一步解析

    :param oauth_code: 企业微信授权登录令牌
    :return:
    """

    response = requests.get(url = config.GET_SESSION_URL,
                            params = {
                                "code": oauth_code
                            })

    if "公告：全体学生请如实填写，迟报、瞒报、漏报造成严重后果的，将严肃追究责任。" in response.text:
        printLog(f"获取到PHPSESSID:{response.history[0].cookies.get('PHPSESSID')}")
        return True, {
            "phpsessid": response.history[0].cookies.get("PHPSESSID"),
            "page_html": response.content  # 返回网页方便下一步解析
        }

    elif "40029" in response.text:
        printLog("OAUTH_CODE 无效或过期")
        return False, "OAUTH_CODE 无效或过期"

    else:
        printLog("获取PHPSESSID失败，未知原因" + response.text)
        return False, response.text


def getUserDataFromHTMLPage(page):
    data = {}
    soup = BeautifulSoup(page, features = "html.parser")
    status = 0
    # 0 - OK  1 - 表单不完整

    # 普通输入框
    for name in ["tbrq", "txr", "lx", "gh", "bm", "bj", "sj", "addr", "area"]:
        e = soup.select(f"input[name='{name}']")
        if len(e) == 1:
            data[name] = e[0]["value"]
        else:
            status = 1
            data[name] = f"无法获取值:{name}"

    # 选项部分
    for name in ["jtzz", "yqfk", "xmfl", "jkm"]:
        e = soup.select(f"input[name='{name}'][checked='']")
        if len(e) == 1:
            data[name] = e[0]["value"]
        else:
            status = 1
            data[name] = f"无法获取值(没有选择选项):{name}"

    # 长文本
    for name in ["jtdz", "dkjtdz", "hxrq"]:
        e = soup.select(f"textarea[name='{name}']")
        if len(e) == 1:
            data[name] = e[0].text
        else:
            if name == "dkjtdz":
                status = 1
            data[name] = f"无法获取值:{name}"

    data["ip"] = "地理经纬度统一为学校地址"

    return status, data


def verifyWorkWxURL(url: str):
    """
    验证企业微信打卡页面URL
    获取用户信息

    :param url:
    :return:
    """
    user = {}

    oauth_code = getOauthCode(url)
    # 检查URL是否合格
    if not oauth_code:
        return False, "无法在链接中找到OAUTH_CODE"

    s, d = getSession(oauth_code)
    if not s:
        return s, d

    phpsessid = d["phpsessid"]
    page_html = d["page_html"]

    # 解析页面获取用户信息
    status, data = getUserDataFromHTMLPage(page_html)

    user["phpsessid"] = phpsessid
    user["status"] = status
    user["data"] = data
    user["gh"] = data.get("gh")

    # 返回 User对象
    return True, user


def pullUserDataBySession(phpsessid: str):
    user = {}

    response = requests.get(url = config.GET_SESSION_URL,
                            cookies = {
                                "PHPSESSID": phpsessid
                            })

    if "公告：全体学生请如实填写，迟报、瞒报、漏报造成严重后果的，将严肃追究责任。" in response.text:
        page_html = response.content

    elif "40029" in response.text:
        return False, "OAUTH_CODE 无效或过期"

    else:
        return False, response.text

    status, data = getUserDataFromHTMLPage(page_html)

    user["phpsessid"] = phpsessid
    user["status"] = status
    user["data"] = data
    user["gh"] = data.get("gh")

    return True, user


# 临时测试
if __name__ == '__main__':
    a = Database()
