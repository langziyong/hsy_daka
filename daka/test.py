import time

import requests

from daka import config

StudentsDetail_Url = "http://shuyuan.zjhzcc.edu.cn/wap/contacts.html"
RoomChoose_Url = "http://shuyuan.zjhzcc.edu.cn/wap/roomchoose.html"
Login_Url = "http://shuyuan.zjhzcc.edu.cn/wap/login"

HEADERS = {
    "HOST": "shuyuan.zjhzcc.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}


# POST 参数为 id
def get_students_detail():
    for i in range(21300, 21350):
        req = requests.post(url = StudentsDetail_Url,
                            headers = HEADERS,
                            cookies = {
                                "PHPSESSID": "mmsaaic5454rfkt42m37893dfu"
                            },
                            data = f"id={i}")
        print(req.text)


def get_students_by_id(StudentId: str):
    req = requests.post(url = StudentsDetail_Url,
                        headers = HEADERS,
                        cookies = {
                            "PHPSESSID": "m1krs7m264htq06prug9d8dc8p"
                        },
                        data = f"id={StudentId}")
    print(req.text)


def test(session: str):
    req = requests.get(url = config.GET_SESSION_URL,
                       headers = config.DAKA_HEADERS,
                       cookies = {
                           "PHPSESSID": session
                       })
    if "本系统由学院防控办、信息技术中心自行开发，信息严格保密，请放心填报，祝各位同学及家人身体健康！！" in req.text:
        print(time.strftime('%m-%d %H:%M:%S'), "PHPSESSID 有效")
    elif "对不起，你还未在学生名单，请联系负责人" in req.text:
        print(time.strftime('%m-%d %H:%M:%S'), "PHPSESSID 无效！！")
    else:
        print(time.strftime('%m-%d %H:%M:%S'), "PHPSESSID 无效！！ 意料之外的情况")


def test_submit():
    data = "tbrq=2022%2F08%2F28&txr=%E8%B5%B5%E7%94%AC&lx=Xs&gh=2241920147&bm=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E4%B8%8E%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1%E5%AD%A6%E9%99%A2&bj=%E8%AE%A1%E7%A7%9122A&sj=17606525312&jtzz=%E4%BD%8E%E9%A3%8E%E9%99%A9%E5%8C%BA%EF%BC%88%E5%A4%A7%E6%9D%AD%E5%B7%9E%E5%86%85%EF%BC%89&jtdz=&addr=%E6%B5%99%E6%B1%9F%E7%9C%81%E6%9D%AD%E5%B7%9E%E5%B8%82%E6%A1%90%E5%BA%90%E5%8E%BF&ip=29.82563%3A119.73&area=%E6%B5%99%E6%B1%9F%E7%9C%81&dkjtdz=%E8%91%A3%E5%AE%B6%E6%9D%91&yqfk=%E5%81%A5%E5%BA%B7&xmfl=%E5%90%A6&jkm=%E5%B7%B2%E7%94%B3%E9%A2%86%EF%BC%8C%E7%BB%BF%E7%A0%81&hxrq="
    req = requests.post(url = config.POST_SUBMIT_URL,
                        headers = config.DAKA_HEADERS,
                        cookies = {
                            "PHPSESSID": "2953bvljuc50js4odtg6abe5n6"
                        },
                        data = data)
    print(req.text)


if __name__ == '__main__':
    test_submit()
