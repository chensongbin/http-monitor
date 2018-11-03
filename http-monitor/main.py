import requests
import time
import smtplib
from email.mime.text import MIMEText
import json
import os


def init():
    # 配置文件名
    confFile = "conf.json"
    # 获取目录路径
    dirPath = os.path.abspath(os.path.dirname(__file__))
    # 配置文件绝对路径
    confPath = os.path.join(dirPath, confFile)
    # 读取配置文件
    with open(confPath, 'r', encoding='utf-8') as f:
        conf = json.load(f)
    logPath = os.path.join(dirPath, conf['logName'])
    conf['logName'] = logPath
    return conf


def sendMail(mail_host, SSLPort, mail_user, mail_pw, to, subject, text):
    # 构造邮件msg
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"] = mail_user
    msg["To"] = to

    # 登陆转发邮件的服务器
    server = smtplib.SMTP_SSL(mail_host, SSLPort)
    server.login(mail_user, mail_pw)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.close()


def test():
    try:
        resp = requests.get(url)
        elapsed = resp.elapsed
        return elapsed
    except:
        return None


if __name__ == "__main__":
    conf = init()
    logPath = conf["logName"]                          # 日志路径
    url = conf["url"]                                  # 监测网址
    minutes = conf["minutes"]                         # 监测的时间间隔（单位/分钟）
    try_cnt = conf["try_cnt"]                         # 重新连接的次数
    try_interval = conf["try_interval"]              # 重新连接的时间间隔（单位/秒）


    # 发邮件相关配置信息
    conf = conf["mailConf"]
    smtpServer = conf["smtpServer"]
    SSLPort = conf["SSLPort"]
    fromEmail = conf["fromEmail"]
    fromEmailPassword = conf["fromEmailPassword"]
    toEmail = conf["toEmail"]

    # 防止重复发邮件
    send_mail = True

    while True:
        # 连接失败次数，如果超过尝试次数，认为服务器故障
        fail_cnt = 0

        # 响应时间 单位/毫秒
        response_time = 0.0

        # 连接测试
        for i in range(try_cnt):
            temp = test()
            if temp:
                response_time = temp.total_seconds() * 1000
                break
            fail_cnt = fail_cnt + 1
            timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            log_msg = timeStr + " fail"
            with open(logPath, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
            time.sleep(try_interval)

        # 测试信息记录
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if fail_cnt == try_cnt:
            log_msg = timeStr + " Down Report"
            #print(log_msg)
            with open(logPath, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
            # 发邮件通知连接出错
            if send_mail:
                log_msg = url + "\n" + log_msg
                sendMail(smtpServer, SSLPort, fromEmail, fromEmailPassword, toEmail,
                        "Down Report", log_msg)
                send_mail = False
        else:
            log_msg = timeStr + " " + str(response_time) + " Milliseconds"
            #print(log_msg)
            with open(logPath, "a", encoding="utf-8") as f:
                f.write(log_msg + "\n")
            send_mail = True

        time.sleep(minutes*60)
