# http-monitor
网站监测——发生宕机邮件通知管理者

## 一个简陋的版本
> ### 功能：
- 监测网站是否能够访问
- 日志记录
- 延迟信息记录
- 发生宕机邮件通知
> ### 配置文件说明 http-monitor/conf.json
```
{
    "logName" : "log.txt",                # 日志文件名称，不是路径
    "url": "http://www.chsobin.xin",      # 网址url
    "try_cnt": 5,                         # 连接失败时，重新尝试连接的次数，如果尝试try_cnt次都无法连接成功，视为网站无法访问，发送邮件
    "try_interval": 5,                    # 每次尝试的间隔时间（单位/秒）
    "minutes": 5,                         # 监测的时间间隔（单位/分钟）
    "mailConf":{
        "smtpServer":"smtp.163.com",      # 邮箱服务器域名或地址
        "SSLPort": 465,                   # 邮箱服务器ssl协议的端口
        "fromEmail":"example@163.com",    # 发送者邮箱地址
        "fromEmailPassword" : "example",  # 发送者邮箱密码
        "toEmail" : "example@163.com"     # 接收者邮箱地址
    }
}

```

## 不足
- 没有支持多网址监测
