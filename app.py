import os
import sys

sys.path.append("daka")

from flask import Flask, request, redirect, render_template, url_for, flash, session, g
from daka import User, Main, config, Task

app = Flask(__name__, static_url_path = "/static")
app.secret_key = "asdhjklhasjhdf"

userControl = User.User()

Main.printLog("Web server statrt")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loginout")
def loginout():
    session.pop("login")
    session.pop("user")
    flash("您已登出")
    return redirect(url_for("index"))


# 登录
@app.route("/login", methods = ["POST"])
def login():
    gh = request.form.get("gh")
    sj = request.form.get("sj")

    s, d = userControl.login(gh, sj)
    if s:
        d["status_message"] = config.STATUS_MESSAGE[d["status"]]
        session["login"]: bool = True
        session["user"]: dict = d
        return redirect(url_for("userPage"))
    else:
        flash(d)
        return redirect(url_for("index"))


# 注册
@app.route("/register/<do>", methods = ["POST"])
def register(do):
    if do == "verify":
        url = request.form.get("workwx_url")
        s, d = Main.verifyWorkWxURL(url)
        if not s:
            flash(d)
            return redirect(url_for("index"))
        else:
            session["user"] = d
            d["status_message"] = config.STATUS_MESSAGE[d["status"]]
            return render_template("register.html", user = d)

    elif do == "submit":
        u = userControl.getUser(session.get("user")["gh"])
        if u is not None:
            userControl.updateUser(session.get("user"))
            flash("检查到你已注册，自动为你你更新本次数据并跳转到用户界面。")
            session["login"] = True
            return redirect(url_for("userPage"))

        s, d = userControl.newUser(session.get("user"))
        if s:
            flash(d)
            session["login"] = True
            return redirect(url_for("userPage"))
        else:
            flash(d)
            return redirect(url_for("index"))

    else:
        flash("错误的操作")
        return redirect(url_for("index"))


@app.route("/user", methods = ["POST", "GET"])
@app.route("/user/<do>", methods = ["POST", "GET"])
def userPage(do = None):
    if session.get("login"):
        if request.method == "GET":
            if do is None:
                # 用户界面
                session.get("user")["status_message"] = config.STATUS_MESSAGE[session.get("user")["status"]]
                return render_template("user.html", user = session.get("user"))

            if do == "repull":
                # 根据会话重新拉取表单数据
                s, d = Main.pullUserDataBySession(session["user"].get("phpsessid"))
                if s:
                    s, d = userControl.updateUser(d)
                    if s:
                        session["user"] = d
                        flash("数据更新完成。")
                        return redirect(url_for("userPage"))
                    else:
                        # 不改变任何数据
                        flash("数据库错误, 无法保存, 所有数据均未改动。")
                        return redirect(url_for("userPage"))
                else:
                    # SESSION 失效
                    session["user"]["status"] = 3
                    userControl.updateUser(session["user"])
                    flash(d)
                    return redirect(url_for("userPage"))

            if do == "daka":
                # 打卡操作
                s, d = Task.DakaTask.daka(session.get("user"))
                flash(d)
                return redirect(url_for("userPage"))

        if request.method == "POST":
            pass

    else:
        flash("您还未登录")
        return redirect(url_for("index"))
