# 直接在文件最下面下方输入账号密码即可
import json
import random

import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

StudentsDetail_Url = "http://shuyuan.zjhzcc.edu.cn/wap/contacts.html"
RoomChoose_Url = "http://shuyuan.zjhzcc.edu.cn/wap/roomchoose.html"
Login_Url = "http://shuyuan.zjhzcc.edu.cn/wap/login"

HEADERS = {
    "HOST": "shuyuan.zjhzcc.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}


# 选择房间提交函数
def choose_room(RoomId: str, Bed: str, Session: str):
    # RoomId 是房间ID ， Bed 是床位
    for i in range(10):
        print("try choose room ..", i)
        try:
            req = requests.post(url = RoomChoose_Url,
                                headers = HEADERS,
                                cookies = {
                                    "PHPSESSID": Session
                                },
                                data = f"room_id={RoomId}&bed={Bed}",
                                timeout = 5)  # 超时5秒
        except requests.exceptions.ReadTimeout as e:
            print("time out", i)
        else:
            print(req.text)
            return True


# 登录模块
def login(Xh: str, Passwd: str):
    print("正在登录...")
    boundary = '-----------------------------' + str(random.randint(int(1e28), int(1e29 - 1)))
    headers = HEADERS
    headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
    multipart_encoder = MultipartEncoder(
        fields = {
            'type': "students",
            'code_type': "xgh",
            'code_value': Xh,
            'password': Passwd

        },
        boundary = boundary
    )
    for i in range(10):
        print("try login ..", i)
        try:
            req = requests.post(url = Login_Url,
                                headers = headers,
                                data = multipart_encoder,
                                timeout = 5)  # 超时5秒
        except requests.exceptions.ReadTimeout as e:
            print("time out", i)
        else:
            res = json.loads(req.content)
            if res.get("code") == 1:
                print("登录成功 获取到 PHPSESSID=", req.cookies.get('PHPSESSID'))
                return req.cookies.get('PHPSESSID')
            else:
                raise Exception(res)


# 拉取房间信息
def pull_room(Session: str):
    for i in range(10):
        print("try pull room", i)
        try:
            req = requests.get(url = "http://shuyuan.zjhzcc.edu.cn/wap/mygroup",
                               headers = HEADERS,
                               cookies = {
                                   "PHPSESSID": Session
                               },
                               timeout = 5)  # 超时5秒
        except requests.exceptions.ReadTimeout as e:
            print("time out", i)
        else:
            # 返回 302 处理
            if len(req.history) != 0:
                if "选室友前先做个登记，让别人更了解你" in req.text:
                    print("你还没有进行寝室需求登记....")
                    return False

                else:
                    print("页面发生跳转 执行退出")
                    return False

            # 返回 200 处理
            elif req.status_code == 200:
                print("拉取床位信息...")
                print("找到你要去得宿舍以及床位 记下最前面得选项")
                soup = BeautifulSoup(req.content, features = "html.parser")
                room_list = {}
                BedId = 0
                for bed in soup.select('td[data-bed]'):
                    print(f"选项：{BedId} 房间ID: {bed.attrs.get('room_id')} 房间编码: {bed.attrs.get('xnh')} 空余得床位号: {bed.attrs.get('data-bed')}")
                    room_list[BedId] = {
                        "room_id": bed.attrs.get('room_id'),
                        "room_name": bed.attrs.get('xnh'),
                        "bed": bed.attrs.get('data-bed')
                    }
                    BedId += 1

                if len(soup.select("td[data-scode='']")) != 0:
                    print("------------------------\n警告！您已经选择房间了！！！" + soup.select("td[data-scode='']")[0].attrs.get("onclick") + "\n------------------------")

                return room_list
            else:
                print("请求失败 CODE", req.status_code)
                return False
    print("拉取房间信息失败 请重试")


# 启动函数
def main(xh, passwd, ):
    session = login(xh, passwd)
    room_list = pull_room(session)
    if not room_list:
        print("脚本退出")
        return False
    else:
        BedId = input("输入你要去得寝室以及床位选项 是选项 就是数字！！！")
        bed = room_list.get(int(BedId))
        if bed is None:
            print("选项不存在")
            return False
        choose_room(RoomId = bed.get("room_id"),
                    Bed = bed.get("bed"),
                    Session = session)
        return True


if __name__ == '__main__':
    XH = ""  # 填入学号
    PASSWORD = ""  # 填入密码

    main(XH, PASSWORD)

    # 2022/8/18 15:42 By Langziyong
