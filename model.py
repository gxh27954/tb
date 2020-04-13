# encoding: UTF-8
import requests
import time
import random
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
ip = ['101.96.0.', '210.28.0.','121.56.0.','221.207.0.','211.140.0.','222.219.0.','124.112.0.','153.118.0.',\
      '125.211.0.','203.191.16.','42.50.0.','58.246.0.','219.154.0.','175.148.0.','171.112.0.','111.114.0.',\
      '222.86.0.','219.226.0.','103.22.68.','218.67.0.','103.22.64.','101.236.0.'
      ]


def makeData(n):
    list = []
    for i in range(0, 200):
        list.append([1, 0])

    list[1] = [1, [1, 0], [2, 20], [3, 30], [4, 0], [5, 0]]
    list[2] = [1, [1, 30], [2, 20]]
    list[3] = [10, [1, 60], [2, 80], [3, 70], [4, 70], [5, 85], [6, 0]]
    list[4] = [1, [1, 10], [2, 30], [3, 20]]
    list[5] = [1, [1, 0], [2, 0], [3, 22], [4, 35], [5, 30]]
    list[6] = [1, [1, 0], [2, 0], [3, 23], [4, 40], [5, 27]]
    list[7] = [1, [1, 0], [2, 0], [3, 21], [4, 36], [5, 28]]
    list[8] = [1, [1, 0], [2, 0], [3, 23], [4, 37], [5, 26]]
    list[9] = [1, [1, 0], [2, 0], [3, 21], [4, 36], [5, 29]]
    list[10] = [1, [1, 0], [2, 0], [3, 21], [4, 35], [5, 29]]
    list[11] = [1, [1, 0], [2, 0], [3, 20], [4, 38], [5, 29]]
    list[12] = [1, [1, 0], [2, 0], [3, 21], [4, 38], [5, 26]]
    list[13] = [1, [1, 0], [2, 0], [3, 21], [4, 39], [5, 29]]
    list[14] = [1, [1, 0], [2, 0], [3, 22], [4, 40], [5, 30]]
    list[15] = [1, [1, 0], [2, 0], [3, 20], [4, 36], [5, 26]]
    list[16] = [1, [1, 0], [2, 0], [3, 21], [4, 38], [5, 26]]
    list[17] = [1, [1, 0], [2, 0], [3, 23], [4, 35], [5, 29]]
    list[18] = [1, [1, 0], [2, 0], [3, 22], [4, 38], [5, 27]]
    list[19] = [1, [1, 0], [2, 0], [3, 22], [4, 36], [5, 27]]
    list[20] = [1, [1, 0], [2, 0], [3, 23], [4, 40], [5, 30]]
    list[21] = [1, [1, 0], [2, 0], [3, 22], [4, 38], [5, 25]]
    list[22] = [1, [1, 0], [2, 0], [3, 22], [4, 38], [5, 30]]
    list[23] = [1, [1, 0], [2, 0], [3, 21], [4, 35], [5, 28]]
    list[24] = [1, [1, 0], [2, 0], [3, 23], [4, 39], [5, 26]]
    list[25] = [1, [1, 0], [2, 0], [3, 22], [4, 36], [5, 27]]
    list[26] = [1, [1, 0], [2, 0], [3, 23], [4, 36], [5, 29]]
    list[27] = [1, [1, 0], [2, 0], [3, 21], [4, 39], [5, 26]]
    list[28] = [1, [1, 0], [2, 0], [3, 20], [4, 35], [5, 26]]

    data = ''
    for i in range(1, n + 1):
        # print list[i]
        data = data + str(i) + '$'  #序号

        dateTemp = ''
        if list[i][0] == 10:  # 多选
            length = len(list[i])
            slice = []
            while len(slice) == 0:
                for j in range(1, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            # size = random.randint(1, length - 1)
            # print slice
            # slice = random.sample(list[i][1:], len(slice))
            random.shuffle(slice)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'
        elif list[i][0] == 11:  # 多选,最多选几项
            length = len(list[i])
            # size = random.randint(1, list[i][1])

            slice = []
            length = len(list[i])

            while len(slice) == 0 or len(slice) > list[i][1]:
                slice = []
                for j in range(2, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])

            # slice = random.sample(list[i][2:], size)
            random.shuffle(slice)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'
        elif list[i][0] == 12:  # 多选,最少选几项
            length = len(list[i])
            slice = []
            length = len(list[i])

            while len(slice) == 0 or len(slice) < list[i][1]:
                slice = []
                for j in range(2, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'

        elif list[i][0] == 13:  # 最少选几项，最多选几项
            length = len(list[i])
            slice = []
            length = len(list[i])

            while len(slice) == 0 or len(slice) < list[i][1] or len(slice) > list[i][2]:
                slice = []
                for j in range(3, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'

        elif list[i][0] == 15:  # 填空
            length = len(list[i])
            for j in range(1, length):
                length1 = len(list[i][j])
                slice = []
                for k in range(0, length1):
                    for x in range(0, list[i][j][k][1]):
                        slice.append(list[i][j][k][0])
                size = random.randint(0, len(slice) - 1)
                # slice
                dateTemp = dateTemp + str(slice[size])
                if j < length - 1:
                    dateTemp = dateTemp + '^'
        elif list[i][0] == 16:  # 矩阵填空
            for j in range(1, len(list[i])):
                dateTemp = dateTemp + str(j) + '!' + str(list[i][j][random.randint(0, len(list[i][j]) - 1)])
                if j != len(list[i]) - 1:
                    dateTemp = dateTemp + '^'
        elif list[i][0] == 1:  # 单选
            # 以下设置比例
            length = len(list[i])
            slice = []
            for j in range(1, length):
                for k in range(0, list[i][j][1]):
                    slice.append(list[i][j][0])
            # 以上设置比例
            length = len(slice)
            size = random.randint(1, length - 1)
            dateTemp = dateTemp + str(slice[size])





        elif list[i][0] == 20:  # 矩阵
            for j in range(1, len(list[i])):
                slice = []
                for k in range(len(list[i][j])):
                    for x in range(0, list[i][j][k][1]):
                        slice.append(list[i][j][k][0])
                # print slice
                dateTemp = dateTemp + str(j) + '!' + str(slice[random.randint(0, len(slice) - 1)])
                if j != len(list[i]) - 1:
                    dateTemp = dateTemp + ','
        elif list[i][0] == 25:
            slice = []
            length = len(list[i])
            while len(slice) != list[i][1]:
                slice = []
                for j in range(2, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            for j in range(len(list[i]) - list[i][1] - 2):
                slice.append(-2)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + ','
        elif list[i][0] == 30:
            # slice = random.sample(list[i][2:], list[i][1])
            slice = []
            length = len(list[i])

            while len(slice) != list[i][1]:
                slice = []
                for j in range(2, length):
                    rand = random.randint(0, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            # print slice
            random.shuffle(slice)
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'
        str1 = '构造第' + str(i) + '题成功'
        # print(str1)
        data = data + dateTemp  # 答案

        if i < n:
            data = data + '}'  # 分隔符

    print data

    return data


def wjx(number, url, Cookie, params):
    sess = requests.session()
    data = {
        # 'submitdata': "1$2",
        'submitdata': makeData(number)
        # 'submitdata':'1$1}2$3}3$17}4$7}5$4|7|9}6$1}7$3|5}8$3}9$3}10$2}11$-3}12$1|2}13$3|5|7}14$1}15$2}16$3}17$2}18$3}19$2^没有这么快}20$2}21$2|4}22$2|4}23$2}24$2}25$1}26$3}27$5'
    }
    # ipp = ip[random.randint(0, len(ip)-1)] + str(random.randint(0, 255))
    # 发送post请求
    ipp = ip[random.randint(0, len(ip) - 1)] + str(random.randint(0, 255))
    # print ipp
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        # 'X-Forwarded-For': '%d.%d.%d.%d' % (
        # random.randint(27, 27), random.randint(109, 109), random.randint(124, 127), random.randint(0, 225)),
        'X-Forwarded-For': ipp,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "close",
        "Content-Length": "519",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": Cookie,
        "Host": "www.wjx.cn",
        "Origin": "https://www.wjx.cn",
        "Referer": "https://www.wjx.cn/jq/27154188.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    res = sess.post(url, headers=headers, data=data, params=params, verify=False)
    print(res.text)


def json2String(data):
    json_data = dict(data)
    # print(json_data)
    # keys = json_data.keys()
    # values = json_data.values()
    # i=0
    str = ''
    for key, value in json_data.items():
        prefix = "{}={};".format(key, value)
        str += prefix
    return str.rstrip(';')


def getJqsign(a, k):
    b = k % 10
    c = ""
    d = 0
    for ch in a:
        e = ord(ch) ^ b
        c = c + chr(e)
    return c


def getAll(curid, needTime):
    url = 'https://www.wjx.cn/m/' + str(curid) + '.aspx'
    head = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    s = requests.get(url, headers=head, verify=False)
    cookie = s.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookie)
    c = json2String(cookies_dict)
    rndnum = re.search("rndnum=\".+\";", s.text).group(0)[8:-2]
    jqnonce = re.search("jqnonce=\".+\";", s.text).group(0)[9:-2]

    ktimes = random.randint(110, 428) + 2
    jqsign = getJqsign(jqnonce, ktimes)

    params = {
        "curid": curid,
        "starttime": needTime,
        "source": 'directphone',
        "submittype": 1,
        "ktimes": ktimes,
        "hlv": 1,
        "rn": rndnum,
        "jpm": 2,
        "t": int(time.time() * 1000),
        "jqnonce": jqnonce,
        "jqsign": jqsign
    }
    return params, c


if __name__ == '__main__':
    curId = 70354776

    time1 = 200
    time2 = 250
    url = "https://www.wjx.cn/joinnew/processjq.ashx"

    doNumber = 50  # 刷几次
    titleNumber = 28  # 多少个题目

    for i in range(doNumber):
        print i +1
        needTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime((time.time() - random.randint(time1, time2))))
        params, Cookie = getAll(curId, needTime)

        wjx(titleNumber, url, Cookie, params)
        time.sleep(random.randint(20, 40))  # 277开始





