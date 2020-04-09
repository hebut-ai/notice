import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from lxml import etree

# 微信推送
def wx(title, content=""):
    api = "https://sc.ftqq.com/##################################################.send"
    data = {"text": title, "desp": content}
    requests.post(api, data=data)


host = "smtphz.qiye.163.com"
user = "#########"
password = "#########"

# 发邮件
def send_mail(head, subject, content=""):
    msg = MIMEText(content, "plain", "utf-8")
    msg["subject"] = subject
    msg["from"] = formataddr([head, "notice@notice.com"])
    msg["to"] = ",".join(["#########@qq.com"])
    asmtp = smtplib.SMTP()
    asmtp.connect(host, port="25")
    asmtp.login(user, password)
    asmtp.sendmail(user, ["#########@qq.com"], str(msg))
    asmtp.quit()


d1 = {
    "01": "台风",
    "02": "暴雨",
    "03": "暴雪",
    "04": "寒潮",
    "05": "大风",
    "06": "沙尘暴",
    "07": "高温",
    "08": "干旱",
    "09": "雷电",
    "10": "冰雹",
    "11": "霜冻",
    "12": "大雾",
    "13": "霾",
    "14": "道路结冰",
    "91": "寒冷",
    "92": "灰霾",
    "93": "雷雨大风",
    "94": "森林火险",
    "95": "降温",
    "96": "道路冰雪",
    "97": "干热风",
    "98": "空气重污染",
    "99": "低温",
    "51": "海上大雾",
    "52": "雷暴大风",
    "53": "持续低温",
    "54": "浓浮尘",
    "55": "龙卷风",
    "56": "低温冻害",
    "57": "海上大风",
    "58": "低温雨雪冰冻",
    "59": "强对流",
    "60": "臭氧",
    "61": "大雪",
    "62": "强降雨",
    "63": "强降温",
    "64": "雪灾",
    "65": "森林（草原）火险",
    "66": "雷暴",
    "67": "严寒",
    "68": "沙尘",
    "69": "海上雷雨大风",
    "70": "海上雷电",
    "71": "海上台风",
    "72": "低温",
}

d2 = {"01": "蓝色", "02": "黄色", "03": "橙色", "04": "红色", "05": "白色"}

l0 = ["初始化"]
d0 = ["初始化"]

# 获取到的预警代码解析
def code_tianqiyujing(l):
    c1 = l[1][-9:-7]
    c2 = l[1][-7:-5]
    yujing = (
        l[0]
        + "："
        + d1[c1]
        + d2[c2]
        + "预警，原文链接：http://www.weather.com.cn/alarm/newalarmcontent.shtml?file="
        + l[1]
    )
    return yujing


# 获取解析天气预警，并返回
def get_tianqiyujing():
    global l0
    r = requests.get(
        "http://product.weather.com.cn/alarm/grepalarm_cn.php?_=1586395431312"
    )
    r.encoding = "deflate"
    r = r.text
    r = r.split(":[[")[1].split("]]}")[0]
    l = r.split("],[")
    for i in range(0, len(l)):
        l[i] = l[i][1:-1]
        l[i] = l[i].split('","')
    # 得到纯净的两层嵌套列表
    if [item for item in l if not item in l0] != []:  # 检测列表的差值
        for j in range(0, len(l)):
            if l[j][0].find("##") >= 0:  # 找到信息
                tq = code_tianqiyujing(l[j])  # 解析信息
                print(tq)
                send_mail("天气预警", tq)
            elif l[j][0] == "######":
                tq = code_tianqiyujing(l[j])
                print(tq)
                send_mail("天气预警", tq)
        l0 = l


def get_dizhen():
    global d0
    r = requests.get("http://news.ceic.ac.cn/")
    r.encoding = "gzip"
    r = r.text
    html = etree.HTML(r)

    zhenji = html.xpath("//table/tr/td[1]/text()")
    shijian = html.xpath("//table/tr/td[2]/text()")
    shendu = html.xpath("//table/tr/td[5]/text()")
    weizhi = html.xpath("//table/tr/td[6]/a/text()")
    if [item for item in shijian if not item in d0] != []:
        for i in range(len(weizhi)):
            if weizhi[i].find("##") >= 0:
                dz = (
                    weizhi[i]
                    + ",于"
                    + shijian[i]
                    + ",发生"
                    + zhenji[i]
                    + "级地震，震源深度"
                    + shendu[i]
                    + "千米。"
                )
                send_mail("地震通知", dz)
                print(dz)
        d0 = shijian


while True:
    try:
        get_tianqiyujing()
        get_dizhen()
    except:
        try:
            wx("程序挂了")
            send_mail("紧急通知", "程序挂了")
        except:
            time.sleep(30)
    time.sleep(300)
