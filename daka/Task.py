import time

import schedule
import config
import requests
from Main import printLog
from User import User
from urllib.parse import quote


class HeartBeat:
    def __init__(self, uc: User):
        self.userControl = uc
        self.execute_time = 10
        self.success_result = []
        self.fail_result = []
        self.users = []
        printLog(f"Heartbeat Serve run ! at {self.execute_time}")

    def wakeSession(self, phpsession: str):
        """
        执行一次带PHPSESSID的请求, 唤醒会话

        :param phpsession:
        :return:
        """
        req = requests.get(url = config.GET_SESSION_URL,
                           headers = config.DAKA_HEADERS,
                           cookies = {
                               "PHPSESSID": phpsession
                           })
        if "公告：全体学生请如实填写，迟报、瞒报、漏报造成严重后果的，将严肃追究责任。" in req.text:
            self.success_result.append((phpsession, 0))

        elif "对不起，你还未在学生名单，请联系负责人" in req.text:
            self.fail_result.append((phpsession, 3))

        else:
            self.fail_result.append((phpsession, 9))

    def main(self):
        """
        执行函数

        :return:
        """
        self.fail_result.clear()
        self.success_result.clear()
        self.users.clear()

        self.users = self.userControl.pullAllUser()
        for user in self.users:
            self.wakeSession(user["phpsessid"])

        printLog(f"End excute wake! result: ok:{len(self.success_result)}  fail:{len(self.fail_result)} all:{len(self.users)}")
        self.fail_result.clear()
        self.success_result.clear()
        self.users.clear()

    def createTask(self):
        """
        创建定时任务

        :return:
        """
        schedule.every(self.execute_time).minutes.do(self.main)


class DakaTask:
    def __init__(self, uc: User):
        self.userControl = uc

    @staticmethod
    def daka(user):
        user_data = user["data"].copy()
        for i in user_data:
            user_data[i] = quote(user_data[i], "utf-8")

        data = f"tbrq={quote(time.strftime('%Y/%m/%d'), 'utf-8')}" \
               f"&txr={user_data['txr']}" \
               f"&lx={user_data['lx']}" \
               f"&gh={user_data['gh']}" \
               f"&bm={user_data['bm']}" \
               f"&bj={user_data['bj']}" \
               f"&sj={user_data['sj']}" \
               f"&jtzz={user_data['jtzz']}" \
               f"&jtdz={user_data['jtdz']}" \
               f"&addr={user_data['addr']}" \
               "&ip=29.82563%3A119.73" \
               f"&area={user_data['area']}" \
               f"&dkjtdz={user_data['dkjtdz']}" \
               f"&yqfk={user_data['yqfk']}" \
               f"&xmfl={user_data['xmfl']}" \
               f"&jkm={user_data['jkm']}" \
               f"&hxrq={user_data['hxrq']}"
        req = requests.post(url = config.POST_SUBMIT_URL,
                            headers = config.DAKA_HEADERS,
                            cookies = {
                                "PHPSESSID": user["phpsessid"]
                            },
                            data = data)
        if "数据填报成功" in req.text:
            return True, "Today Submit Success!"

        elif "数据已填报" in req.text:
            return True, "Repeat Submit!"

        else:
            return False, "Submit Fail"

    def main(self):
        users = self.userControl.pullAllUser()
        for u in users:
            s, d = self.daka(u)
            printLog(f"{u['gh']} {d}")

    def createTask(self):
        schedule.every().day.at("06:00").do(self.main)


if __name__ == '__main__':
    userControl = User()
    # task1 = HeartBeat(userControl)
    # task1.createTask()

    task2 = DakaTask(userControl)
    task2.createTask()

    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(5)
