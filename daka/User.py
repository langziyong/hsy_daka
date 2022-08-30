# 用户控制类
import json
import Main


class User:  # 用户控制类

    def __init__(self):
        self.dataBase = Main.Database()

    def pullAllUser(self):
        with self.dataBase.getCursor() as scursor:
            sql = "select gh, phpsessid, data, status from Daka_User"
            scursor.execute(sql)
            data = scursor.fetchall()
        return [{
            "gh": u[0],
            "phpsessid": u[1],
            "data": json.loads(u[2]),
            "status": u[3]
        } for u in data]

    def newUser(self, user):

        with self.dataBase.getCursor() as cursor:
            sql = "insert into Daka_User (gh,  phpsessid, data, status) VALUES (%s, %s, %s, %s)"
            r = cursor.execute(sql, [
                user["gh"],
                user["phpsessid"],
                json.dumps(user["data"]),
                user["status"]
            ])
            if r == 1:
                return True, "上传成功"
            else:
                return False, "数据库错误"

    def getUser(self, gh: str) -> dict | None:
        with self.dataBase.getCursor() as cursor:
            sql = "select gh, phpsessid, data, status from Daka_User where gh = %s"
            cursor.execute(sql, gh)
            r = cursor.fetchone()
            if r is None:
                return None

            else:
                return {
                    "gh": r[0],
                    "phpsessid": r[1],
                    "data": json.loads(r[2]),
                    "status": r[3]
                }

    def login(self, gh, sj):
        user = self.getUser(gh)
        if user is None:
            return False, "用户不存在"

        else:
            if sj != user["data"]["sj"]:
                return False, "学号与手机不匹配，验证失败"

            elif sj == user["data"]["sj"]:
                return True, user

            else:
                return False, "未知错误，验证失败"

    def updateUser(self, user: dict):
        with self.dataBase.getCursor() as cursor:
            sql = "update Daka_User set phpsessid=%s, data=%s, status=%s where gh=%s"
            r = cursor.execute(sql, [
                user["phpsessid"],
                json.dumps(user["data"]),
                user["status"],
                user["gh"],
            ])

            return True, user

    def delUser(self, gh: str):
        with self.dataBase.getCursor() as cursor:
            sql = "delete from Daka_User where gh=%s"
            cursor.execute(sql, gh)
            return True


if __name__ == '__main__':
    x = User()
    # d = x.pullAllUser()
    # print(d)
    print(x.getUser(""))
    print(x.login("", ""))
