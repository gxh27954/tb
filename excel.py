# encoding: UTF-8
import requests
import time
import random
import sys
import re
import json
import string
import datetime
import os
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')
ip = []
cap = []
stash_list = []
wjx_type = "wj"
map_ip = {}
rndnum_temp = ""
cookie_temp = ""
curId2 = 0
Verify = 0
db_ip = "rm-bp1t8laryds7p02l6xo.mysql.rds.aliyuncs.com"
db_port = 3306
db_user = "root"
db_pass = "isd@cloud123"
db_name = "test"

ipURL = "http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=60&cid=-1&orderId=O23110411582875849221&time=1727931763&sign=6e6936c920b57e1cff10fa770b28d604&noDuplicate=1&dataType=1&lineSeparator=0"
# ipURL = "http://api.xiequ.cn/VAD/GetIp.aspx?act=get&num=1&time=30&plat=1&re=0&type=2&so=1&ow=1&spl=1&addr=&db=1"
# ipURL = "http://api.xiequ.cn/VAD/GetIp.aspx?act=getturn57&uid=50309&vkey=0827140B061F7A1B5C1F1CD3E94F5BBC&num=1&time=6&plat=1&re=0&type=7&so=1&group=51&ow=1&spl=1&addr=天津&db=1"
# ipURL = "http://tiqu.pyhttp.taolop.com/getip?count=1&neek=18260&type=1&yys=0&port=1&sb=&mr=1&sep=6"
for i in range(0, 200):
    cap.append([0])


def getIplist(appointIps=None):
    shanchenURL = "https://h.shanchendaili.com/api.html?action=get_ip&key=HUb344bcd90409023049NBol&time=1&count=1&protocol=http&type=text&textSep=2&only=1"
    if appointIps == None:
        return []
    ips = []
    try:
        file = open('/Users/xuanhao.guo/Downloads/ip_province.txt')
        while 1:
            line = file.readline()
            if not line:
                break
            for ip in appointIps:
                if line.find(ip) != -1:
                    ips.append(shanchenURL + "&province=" + line.split("\t")[1].replace("\n", ""))
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        file.close()
    try:
        file = open('/Users/xuanhao.guo/Downloads/ip_city.txt')
        while 1:
            line = file.readline()
            if not line:
                break
            for ip in appointIps:
                if line.find(ip) != -1:
                    ips.append(shanchenURL + "&city=" + line.split("\t")[1].replace("\n", ""))
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        file.close()
    print '获取到' + str(len(ips)) + '个段的ip，大约有ip数 : ' + str(250 * len(ips))
    return ips


ccc = []


def ips():
    global ip
    ip = getIplist(["湖南", "湖北", "深圳"])  # ["省"]是全部地区随机的意思
    # ip = getIplist(ccc) # 如果用了get_city_2()或者get_city_3()，用这句就可以ip和选项对应了
    print(ip)


appointIP = False

count = 0


def makeData(n):
    list = []
    cronbach = []
    cronbachR = []
    cronbachNum = []
    choose = []
    hasjump = []
    check = []
    limit = []

    for i in range(0, 200):
        list.append([1, 0])
        cronbach.append([0])
        cronbachR.append([0])
        cronbachNum.append(0)
        check.append([0])
        limit.append([0])
        choose.append([])
        hasjump.append(0)

    cronbachTemps = [[]]

    # 20-矩阵题保证因子
    # cronbachTemps = [[x,y,z]]
    # cronbach[x] = [1, [1, 2], [2, 5], [3, 10], [4, 16], [5, 5]]
    # if random.randint(1, 100) <= 60:
    #    cronbachTemps = [[]]
    #    cronbach[x] = [1, [1, 2], [2, 5], [3, 10], [4, 16], [5, 5]]
    #    cronbach[y] = [1, [1, 2], [2, 5], [3, 16], [4, 16], [5, 5]]
    #    cronbach[z] = [1, [1, 2], [2, 10], [3, 16], [4, 16], [5, 5]]

    report_set = []
    for cronbachTemp in cronbachTemps:
        for i in range(1, len(cronbachTemp)):
            if type(cronbachTemp[i]) == type(10):
                cronbach[cronbachTemp[i]] = [2, cronbachTemp[0]]
            if type(cronbachTemp[i]) == type('10-20'):
                c = cronbachTemp[i].split('-')
                a = int(c[0])
                b = int(c[1])
                for j in range(a, b + 1):
                    cronbach[j] = [2, cronbachTemp[0]]

    # print cronbach[0:50]
    # cronbach[x] = [1, [1, 2], [2, 5], [3, 10], [4, 16], [5, 5]]
    # check[10] = [1, [6], [4]]  #表示第10题的6一定选4
    # check[10] = [1, [5,6], [3,4]]  #表示第10题的5一定选3，6一定选4
    # limit[10] = [1, [1, 10], [2, 13]]   #表示第10题的1选10个，2选13个，固定数量时可用，用了这个就最好不要做逻辑了

    list[1] = [1, [1, 10], [2, 10]]
    list[2] = [1, [1, 21], [2, 35], [3, 26], [4, 16]]
    list[3] = [1, [1, 5], [2, 30], [3, 9]]

    list[4] = [1, [1, 21], [2, 18], [3, 0], [4, 13], [5, 14], [6, 2]]
    list[5] = [1, [1, 5], [2, 19], [3, 23], [4, 30], [5, 18]]
    list[6] = [1, [1, 5], [2, 18], [3, 32], [4, 24], [5, 25], [6, 19], [7, 2]]
    list[7] = [1, [1, 28], [2, 41], [3, 25], [4, 12], [5, 3]]
    list[8] = [20, \
    [[1, 20], [2, 22], [3, 39], [4, 23], [5, 47]], \
    [[1, 46], [2, 24], [3, 10], [4, 10], [5, 40]], \
    [[1, 44], [2, 37], [3, 27], [4, 38], [5, 37]], \
    [[1, 33], [2, 39], [3, 34], [4, 12], [5, 17]], \
    [[1, 16], [2, 29], [3, 26], [4, 10], [5, 12]], \
    ]
    list[9] = [20, \
    [[1, 47], [2, 12], [3, 14], [4, 31], [5, 13]], \
    [[1, 39], [2, 44], [3, 12], [4, 41], [5, 28]], \
    [[1, 28], [2, 39], [3, 13], [4, 26], [5, 37]], \
    [[1, 28], [2, 30], [3, 40], [4, 20], [5, 50]], \
    ]
    list[10] = [20, \
    [[1, 27], [2, 13], [3, 40], [4, 33], [5, 10]], \
    [[1, 35], [2, 39], [3, 44], [4, 38], [5, 36]], \
    [[1, 46], [2, 36], [3, 28], [4, 21], [5, 50]], \
    [[1, 40], [2, 12], [3, 18], [4, 37], [5, 42]], \
    ]
    list[11] = [20, \
    [[1, 43], [2, 44], [3, 22], [4, 41], [5, 34]], \
    [[1, 42], [2, 36], [3, 40], [4, 48], [5, 18]], \
    [[1, 38], [2, 43], [3, 37], [4, 20], [5, 46]], \
    [[1, 44], [2, 36], [3, 25], [4, 19], [5, 40]], \
    ]
    list[12] = [20, \
    [[1, 45], [2, 32], [3, 23], [4, 38], [5, 34]], \
    [[1, 46], [2, 21], [3, 46], [4, 38], [5, 47]], \
    [[1, 47], [2, 24], [3, 50], [4, 26], [5, 22]], \
    [[1, 41], [2, 37], [3, 25], [4, 16], [5, 44]], \
    ]
    list[13] = [20, \
    [[1, 34], [2, 22], [3, 15], [4, 20], [5, 50]], \
    [[1, 19], [2, 16], [3, 45], [4, 15], [5, 23]], \
    [[1, 36], [2, 23], [3, 10], [4, 36], [5, 30]], \
    [[1, 49], [2, 13], [3, 11], [4, 14], [5, 36]], \
    [[1, 35], [2, 48], [3, 49], [4, 29], [5, 19]], \
    ]
    list[14] = [20, \
    [[1, 15], [2, 16], [3, 36], [4, 45], [5, 13]], \
    [[1, 37], [2, 35], [3, 37], [4, 25], [5, 39]], \
    [[1, 16], [2, 15], [3, 17], [4, 48], [5, 15]], \
    [[1, 36], [2, 41], [3, 38], [4, 43], [5, 15]], \
    [[1, 35], [2, 35], [3, 12], [4, 13], [5, 47]], \
    [[1, 40], [2, 24], [3, 17], [4, 13], [5, 24]], \
    [[1, 43], [2, 27], [3, 17], [4, 24], [5, 24]], \
    [[1, 27], [2, 40], [3, 29], [4, 23], [5, 34]], \
    ]
    list[15] = [20, \
    [[1, 18], [2, 35], [3, 19], [4, 34], [5, 15]], \
    [[1, 44], [2, 49], [3, 12], [4, 38], [5, 11]], \
    [[1, 25], [2, 42], [3, 24], [4, 28], [5, 24]], \
    [[1, 32], [2, 10], [3, 40], [4, 30], [5, 48]], \
    ]



    # k = random.randint(1, 100)
    # if k <= 20:
    #     list[x] = []
    # elif k <= 40:
    #     list[x] = []

    for i in range(1, 100):
        list[i] = [1, [1, 10]]






    if count == 0:
        sum_list = []
        for i in range(1, n + 1):
            if limit[i][0] == 1:
                sum = 0
                for j in range(1, len(list[i])):
                    sum = sum + list[i][j][1]
                sum_list.append(sum)
                print("i=%s, sum=%s" % (i, sum))
        for i in range(1, len(sum_list)):
            if sum_list[i] != sum_list[i - 1]:
                print("有不一致的题目，请检查")
                return

        for i in range(1, n + 1):
            cap[i] = limit[i]


    data = ''
    excel_data = ''
    excel_cow = 1
    for i in range(1, n + 1):
        # print list[i]
        data = data + str(i) + '$'  # 序号

        excel_data = excel_data + '"' + str(i) + '$"'

        dateTemp = ''

        if list[i][0] == 10:  # 多选
            length = len(list[i])
            slice = []
            while len(slice) == 0:
                for j in range(1, length):
                    rand = random.randint(1, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            # slice存了多选题选了哪些选项，在这里做逻辑
            # if i == 5 and 2 in slice:
            #     list[x] = []

            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                choose[i].append(slice[j])
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
                    rand = random.randint(1, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])

            random.shuffle(slice)
            # slice存了多选题选了哪些选项，在这里做逻辑
            # if i == 5 and 2 in slice:
            #     list[x] = []
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                choose[i].append(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'
        elif list[i][0] == 12:  # 多选,最少选几项
            length = len(list[i])
            slice = []
            length = len(list[i])

            while len(slice) == 0 or len(slice) < list[i][1]:
                slice = []
                for j in range(2, length):
                    rand = random.randint(1, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            # slice存了多选题选了哪些选项，在这里做逻辑
            # if i == 5 and 2 in slice:
            #     list[x] = []
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                choose[i].append(slice[j])
                if j < len(slice) - 1:
                    dateTemp = dateTemp + '|'

        elif list[i][0] == 13:  # 最少选几项，最多选几项
            length = len(list[i])
            slice = []
            length = len(list[i])

            while len(slice) == 0 or len(slice) < list[i][1] or len(slice) > list[i][2]:
                slice = []
                for j in range(3, length):
                    rand = random.randint(1, 100)
                    if rand <= list[i][j][1]:
                        slice.append(list[i][j][0])
            random.shuffle(slice)
            # slice存了多选题选了哪些选项，在这里做逻辑
            # if i == 5 and 2 in slice:
            #     list[x] = []
            for j in range(0, len(slice)):
                dateTemp = dateTemp + str(slice[j])
                choose[i].append(slice[j])
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
                choose[i].append(slice[j])
                if j < length - 1:
                    dateTemp = dateTemp + '^'
        elif list[i][0] == 16:  # 矩阵填空
            for j in range(1, len(list[i])):
                dateTemp = dateTemp + str(j) + '!' + str(list[i][j][random.randint(0, len(list[i][j]) - 1)])
                if j != len(list[i]) - 1:
                    dateTemp = dateTemp + '^'
        elif list[i][0] == 1:  # 单选
            excel_data = excel_data + "&" + number_to_base26(excel_cow) + "2"
            excel_cow = excel_cow + 1
            if cronbach[i][0] == 2:
                size = cronbachNum[cronbach[i][1]]
                if size < 1:
                    print("检查cronbach！")
                    break
                a = random.randint(0, 100)
                if a < 30:
                    b = max(1, size - 1)
                elif a < 70:
                    b = size
                else:
                    b = min(size + 1, len(list[cronbach[i][1]]) - 1)

                if cronbachR[i][0] == 1:
                    if i in []:
                        dateTemp = dateTemp + str((cronbachR[i][1] - b + 1) * 20 - random.randint(0, 19))
                    else:
                        dateTemp = dateTemp + str(cronbachR[i][1] - b + 1)
                    choose[i].append(b)
                else:
                    if i in []:
                        dateTemp = dateTemp + str(b * 20 - random.randint(0, 19))
                    else:
                        dateTemp = dateTemp + str(b)
                    choose[i].append(b)
                cronbachNum[i] = b
            else:
                # 以下设置比例
                length = len(list[i])
                slice = []
                for j in range(1, length):
                    for k in range(0, list[i][j][1]):
                        slice.append(list[i][j][0])
                # 以上设置比例
                length = len(slice)
                if cap[i][0] == 0:
                    size = random.randint(0, length - 1)
                    if i in []:
                        dateTemp = dateTemp + str(slice[size] * 20 - random.randint(0, 19))
                    else:
                        dateTemp = dateTemp + str(slice[size])
                    choose[i].append(slice[size])
                    cronbachNum[i] = slice[size]










                else:
                    while True:
                        size = random.randint(0, length - 1)
                        pos = 0
                        for tr in range(1, len(list[i])):
                            if list[i][tr][0] == slice[size]:
                                pos = tr
                                break
                        global cap
                        if cap[i][pos][1] > 0:
                            dateTemp = dateTemp + str(slice[size])
                            cronbachNum[i] = slice[size]
                            choose[i].append(slice[size])
                            cap[i][pos][1] = cap[i][pos][1] - 1
                            break
        elif list[i][0] == 20:  # 矩阵
            if cronbach[i][0] == 1:
                length = len(cronbach[i])
                slice = []
                for j in range(1, length):
                    for k in range(0, cronbach[i][j][1]):
                        slice.append(cronbach[i][j][0])
                # 以上设置比例
                length = len(slice)
                size = slice[random.randint(1, length - 1)]
                cronbachNum[i] = size
                # size是量表的队头，可以在这里做逻辑
                # if i == 10 and size == 2:
                #     list[x] = []

                if size < 1:
                    print("检查cronbach！")
                    break

                for j in range(1, len(list[i])):
                    excel_data = excel_data + '&"' + str(j) + '!"&' + number_to_base26(excel_cow) + "2&"
                    excel_cow = excel_cow + 1
                    a = random.randint(0, 100)
                    if a < 30:
                        b = max(1, size - 1)
                    elif a < 70:
                        b = size
                    else:
                        b = min(size + 1, len(cronbach[i]) - 1)
                    if b < 1:
                        print("检查cronbach！")
                        break

                    if check[i][0] == 1 and j in check[i][1]:
                        index = check[i][1].index(j)
                        b = check[i][2][index]
                    if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                        if i in []:
                            dateTemp = dateTemp + str(j) + '!' + str(
                                (cronbachR[i][1] - b + 1) * 20 - random.randint(0, 19))
                        else:
                            dateTemp = dateTemp + str(j) + '!' + str(cronbachR[i][1] - b + 1)
                        choose[i].append(b)
                    else:
                        if i in []:
                            dateTemp = dateTemp + str(j) + '!' + str(b * 20 - random.randint(0, 19))
                        else:
                            dateTemp = dateTemp + str(j) + '!' + str(b)

                        choose[i].append(b)
                    if j != len(list[i]) - 1:
                        if i in []:
                            dateTemp = dateTemp + '^'
                            excel_data = excel_data + '&"^"'
                        else:
                            dateTemp = dateTemp + ','
                            excel_data = excel_data + '&","'
            elif cronbach[i][0] == 2:
                size = cronbachNum[cronbach[i][1]]
                size = random.choice([size, max(1, size - 1), min(len(cronbach[cronbach[i][1]]) - 1, size + 1)])
                if size < 1:
                    print("检查cronbach！")
                    break
                for j in range(1, len(list[i])):
                    excel_data = excel_data + '&"' + str(j) + '!"&' + number_to_base26(excel_cow) + "2&"
                    excel_cow = excel_cow + 1
                    a = random.randint(0, 100)
                    if a < 30:
                        b = max(1, size - 1)
                    elif a < 70:
                        b = size
                    else:
                        b = min(size + 1, len(cronbach[cronbach[i][1]]) - 1)
                    if b < 1:
                        print("检查cronbach！")
                        break
                    if check[i][0] == 1 and j in check[i][1]:
                        index = check[i][1].index(j)
                        b = check[i][2][index]
                    if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                        if i in []:
                            dateTemp = dateTemp + str(j) + '!' + str(
                                (cronbachR[i][1] - b + 1) * 20 - random.randint(0, 19))
                        else:
                            dateTemp = dateTemp + str(j) + '!' + str(cronbachR[i][1] - b + 1)
                        choose[i].append(b)
                    else:
                        if i in []:
                            dateTemp = dateTemp + str(j) + '!' + str(b * 20 - random.randint(0, 19))
                        else:
                            dateTemp = dateTemp + str(j) + '!' + str(b)

                        choose[i].append(b)
                    if j != len(list[i]) - 1:
                        if i in []:
                            dateTemp = dateTemp + '^'
                            excel_data = excel_data + '&"^"'
                        else:
                            dateTemp = dateTemp + ','
                            excel_data = excel_data + '&","'
            else:
                for j in range(1, len(list[i])):
                    excel_data = excel_data + '&"' + str(j) + '!"&' + number_to_base26(excel_cow) + "2"
                    excel_cow = excel_cow + 1
                    slice = []
                    for k in range(len(list[i][j])):
                        for x in range(0, list[i][j][k][1]):
                            slice.append(list[i][j][k][0])
                    # print slice
                    b = slice[random.randint(0, len(slice) - 1)]
                    if check[i][0] == 1 and j in check[i][1]:
                        index = check[i][1].index(j)
                        b = check[i][2][index]
                    if i in []:
                        dateTemp = dateTemp + str(j) + '!' + str(b * 20 - random.randint(0, 19))
                    else:
                        dateTemp = dateTemp + str(j) + '!' + str(b)
                    choose[i].append(b)
                    if j != len(list[i]) - 1:
                        if i in []:
                            dateTemp = dateTemp + '^'
                            excel_data = excel_data + '&"^"'
                        else:
                            dateTemp = dateTemp + ','
                            excel_data = excel_data + '&","'
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
                choose[i].append(slice[j])
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
        print(str1)
        data = data + dateTemp  # 答案

        if i < n:
            data = data + '}'  # 分隔符
            excel_data = excel_data + '&"}"&'

    # data = ans[count]
    # data = muti(data, 24, 8)
    excel_data = '=' + excel_data
    print excel_data
    global stash_list
    stash_list = []
    report_list = []
    for report in report_set:
        if type(report) == type(0):
            report_list.append(report)
        elif type(report) == type(''):
            c = report.split('-')
            a = int(c[0])
            b = int(c[1])
            for j in range(a, b + 1):
                report_list.append(j)
        else:
            print("report error!")
            return

    for i in range(1, n + 1):
        if i in report_list:
            for x in choose[i]:
                stash_list.append(x)
    return data


def muti(data, number, n):
    strx = '}' + str(number) + '$'
    a = data.find(str(strx))
    stry = data[a + len(str(number)) + 2:a + len(str(number)) + 2 + n]
    i = 1
    ans = ''
    for s in stry:
        if s == '1':
            ans = ans + str(i) + '|'
        i = i + 1
    ans = ans[:-1]
    data = data[:a + len(str(number)) + 2] + ans + data[a + len(str(number)) + 2 + n:]
    return data


def AinB(A, B):
    if B < 0:
        B = -B
        for a in A:
            if a in B:
                return False
        return False
    for a in A:
        if a in B:
            return True
    return False


def AinBALL(A, B):
    for b in B:
        if b not in A:
            return False
    return True


def wjx(number, url, Cookie, params, data, ip_proxy):
    sess = requests.session()
    if data == '':
        try:
            data = {
                'submitdata': makeData(number)
                # 'submitdata':'1$1}2$3}3$17}4$7}5$4|7|9}6$1}7$3|5}8$3}9$3}10$2}11$-3}12$1|2}13$3|5|7}14$1}15$2}16$3}17$2}18$3}19$2^没有这么快}20$2}21$2|4}22$2|4}23$2}24$2}25$1}26$3}27$5'
            }
        except Exception, e:
            if "shortid" in params:
                params["curid"] = params["shortid"]
            postToWx(str(params["curid"]) + ' makeData has error!')

            print str(Exception)
            print str(e)
            print str(e.message)
            os._exit(0)
    ip_proxy = getIp()
    if wjx_type == "wj":
        host = "www.wjx.cn"
    if wjx_type == "tp":
        host = "tp.wjx.top"
    if wjx_type == "ks":
        host = "ks.wjx.top"

    if str(curId).isdigit():
        re = "https://%s/m/%s.aspx" % (host, curId)
    else:
        re = "https://%s/vm/%s.aspx" % (host, curId)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "519",
        "Content-Type": "application/x-www-form-urlencoded",
        # "Cookie": Cookie,
        "Host": host,
        "Origin": host,
        "Referer": re,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }
    try:

        proxies = {"http": "http://%s" % ip_proxy,
                   "https": "https://%s" % ip_proxy}

        '''
        u_asec = "099%23" + ''.join(random.sample(string.ascii_letters + string.digits, 18))
        if str(params["curid"]).isdigit():
            url = 'https://www.wjx.cn/joinnew/processjq.ashx?curId=' + str(params["curid"])
        else:
            url = 'https://www.wjx.cn/joinnew/processjq.ashx?shortid=' + str(params["curid"])
        url = url + '&starttime=' + str(
        params["starttime"]) + '&source=' + params["source"] + '&submittype=1&ktimes=' + str(
        params["ktimes"]) + '&hlv=1&rn=' + str(
        params["rn"]) + '&t=' + str(int(round((time.time()) * 1000))) + '&jqnonce=' + str(
        params["jqnonce"]) + '&jqsign=' + str(params["jqsign"]) + '&u_atype=2&u_asec=' + str(u_asec) +'&jqpram=' + str(params["jqParam"])
        '''
        url = "https://www.wjx.cn/joinnew/processjq.ashx"

        # if params.has_key("nc_token"):
        #    url = url + "&" + "nc_token=" + str(params["nc_token"])
        #    url = url + "&" + "nc_sig=" + str(params["nc_sig"][0])
        #    url = url + "&" + "nc_csessionid=" + str(params["nc_csessionid"][0])
        #    url = url + "&" + "nc_scene=" + str(params["nc_scene"][0])

        if params["source"] == "微信":
            url = url + "?access_token=44_2TDADMPw8cFOCyHCC4iVvmwhnTRz3LIyRm-kshboozYxndLqe85dci8E_x0-OeHS6ULi1VK2AwIyoU-eVom7fwc9lHTLKw2pCFri1xK-94s&openid=o2Ex11Lt6V" + ''.join(
                random.sample(string.ascii_letters + string.digits, 18)) + "&jpm=13&isMtitle=0&iwx=1"

        res = sess.post(url, headers=headers, data=data, timeout=3, params=params, proxies=proxies)
        print res.text
        if res.text.find("arg1") != -1:
            arg1 = re.search('arg1=\'[0-9A-Z]+\'', res.text).group().replace('arg1=', '').replace('\'', '')
            cookie = getCookie(arg1)
            print cookie
            headers["Cookie"] = headers["Cookie"] + ";acw_sc__v2=" + str(cookie)
            res = sess.post(url, headers=headers, data=data, proxies=proxies, timeout=3)
            print res.text

    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        return False, data

    if "shortid" in params:
        params["curid"] = params["shortid"]
    if res.text.find("sojump") != -1:
        f = open('result_' + str(params["curid"]) + '.txt', 'a+')
        f.write('total is: ' + res.text + "\n")
        f.write('starttime is: ' + params["starttime"] + "\n")
        # f.write('ip is: ' + str(params["ip"]) + "\n")
        f.write('count is: ' + str(count) + "\n")
        f.write('proxy-ip is: ' + str(proxies) + "\n")
        f.write('answer is: ' + str(data) + "\n\n\n")
        f.close()

        f = open('cap_' + str(params["curid"]) + '.txt', 'a+')
        f.write('cap is : ' + str(cap) + "\n")
        f.close()

        if len(stash_list) > 0:
            import csv
            filename = str(params["curid"]) + ".csv"
            if os.path.isfile(filename) == False:
                x = []
                for i in range(1, len(stash_list) + 1):
                    x.append(i)
                with open(filename, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(x)

            with open(filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(stash_list)

        intoDB(params["curid"], params["starttime"], str(ip_proxy), str(data))
        return True, ''

    if res.text.find("此问卷正在编辑或者暂停状态") != -1:
        postTo(str(params["curid"]) + ' 此问卷正在编辑或者暂停状态 has error!')
        postToWx(str(params["curid"]) + ' 此问卷正在编辑或者暂停状态 has error!')
        sys.exit()

    if res.text.find("问卷发布者有效期") != -1:
        postTo(str(params["curid"]) + ' 问卷发布者有效期 has error!')
        postToWx(str(params["curid"]) + ' 问卷发布者有效期 has error!')
        sys.exit()

    if res.text.find("提交的答案不符合要求") != -1:
        postTo(str(params["curid"]) + ' 提交的答案不符合要求 has error!')
        postToWx(str(params["curid"]) + ' 提交的答案不符合要求 has error!')
        sys.exit()

    if res.text.find("验证码") != -1:
        postTo(str(params["curid"]) + ' 验证码 has error!')
        global Verify
        Verify = 1
        # postToWx(str(params["curid"]) + ' 验证码 has error!', "gz")

    return False, data


def postTo(content):
    url = "https://openapi.seatalk.io/webhook/group/0WlJoFIbTwS7dN8SC7DXKg"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "tag": "text",
        "text": {"content": content}
    }
    try:
        res = requests.post(url, headers=headers, data=json.dumps(data), timeout=3)
        print res.text
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)


def postToWorkWx(content):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1415349d-a544-4950-8834-9044cb77d248"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {"content": content}
    }
    try:
        res = requests.post(url, headers=headers, data=json.dumps(data), timeout=3)
        print res.text
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)


def postToWx(content, people=None):
    import json
    ids = ["o1mph6trZSViZDYVn4b4PkghaOmc"]  # , "o1mph6t-Gx41bDRhxdAzgDx4ywl4"]
    ids = ["o1mph6trZSViZDYVn4b4PkghaOmc", "o1mph6k38Op6Y05_pVUX25vEcigs", "o1mph6iU6VdJ7N7fFcNGtWg5I3Rw",
           "o1mph6tuNT1FupwYChQbZpPGSpIY"]

    if people == "gz":
        ids = ["o1mph6trZSViZDYVn4b4PkghaOmc"]

    try:
        s = requests.get(
            "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx3ec9004dc153e861&secret=fcd99ef6ada7e89dde42c7deee90500f")
        j = json.loads(s.text)
        print j
        access_token = j["access_token"]

        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % access_token
        print url
        for id in ids:
            data = {
                "touser": str(id),
                "template_id": "Z1B5SQNcbyApnDPMgCrFmm8CI5pbyEsJ6H2ghZcva7w",
                "url": "http://weixin.qq.com/download",
                "topcolor": "#FF0000",
                "data": {
                    "message": {
                        "value": content,
                        "color": "#173177"
                    }
                }
            }
            print data

            res = requests.post(url, data=json.dumps(data))
            print res.text
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)


def postToWx2(content, people=None):
    ids = ["SCT43559TGIppKngHeu9KHj7pzEiDN4Qh", "SCT43565T7BJaCybUIfZvmzEZf0KV4SVD",
           "SCT43564Tl7sRnSkonV0aT27RsOLM30o9", "SCT43563Tqh9AmipU9mX9MSoLLhgkZ0OO"]
    if people == "gz":
        ids = ["SCT43559TGIppKngHeu9KHj7pzEiDN4Qh"]
    for id in ids:
        url = "https://sctapi.ftqq.com/%s.send?title=%s" % (
        id, content + " " + time.strftime('%H:%M:%S', time.localtime((time.time()))))
        try:
            res = requests.get(url)
            print res.text
        except Exception, e:
            print str(Exception)
            print str(e)
            print str(e.message)


def get_city_3(appointCity=None):
    s = ""
    try:
        f = open('/Users/xuanhao.guo/Downloads/city3.txt', 'r')
        s = f.read()
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        f.close()
    city_name = []
    for p in s.split("#"):
        p_name = p.split('$')[0]
        p_chilren = p.split('$')[1]
        for city in p_chilren.split("|"):
            for i in range(1, len(city.split(","))):
                if p_name not in ["香港", "澳门", "台湾"]:
                    city_name.append(p_name + '-' + city.split(",")[0] + '-' + city.split(",")[i])
    if appointCity == None:
        c = random.choice(city_name)
        global ccc
        ccc = c.split("-")
        return c
    city_name2 = []
    for city in city_name:
        for appint in appointCity:
            if city.find(appint) != -1:
                city_name2.append(city)
                break
    c = random.choice(city_name2)
    global ccc
    ccc = c.split("-")
    return c


def get_city_2(appointCity=None):
    s = ""
    try:
        f = open('/Users/xuanhao.guo/Downloads/city2.txt', 'r')
        s = f.read()
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        f.close()
    city_name = []
    for p in s.split("#"):
        p_name = p.split('$')[0]
        p_chilren = p.split('$')[1]
        for city in p_chilren.split(","):
            if p_name not in ["香港", "澳门", "台湾"]:
                city_name.append(p_name + '-' + city)
    if appointCity == None:
        c = random.choice(city_name)
        global ccc
        ccc = c.split("-")
        return c
    city_name2 = []
    for city in city_name:
        for appint in appointCity:
            if city.find(appint) != -1:
                city_name2.append(city)
                break
    c = random.choice(city_name2)
    global ccc
    ccc = c.split("-")
    return c


def getIplist1(appointIps=None):
    if appointIps == None:
        return []
    ips = []
    try:
        file = open('/Users/xuanhao.guo/Downloads/ips.txt')
        while 1:
            line = file.readline()
            if not line:
                break
            for ip in appointIps:
                if line.find(ip) != -1:
                    ips.append(line.split("(")[0][:-3])
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        file.close()
    print '获取到' + str(len(ips)) + '个段的ip，大约有ip数 : ' + str(250 * len(ips))
    return ips


def get_people():
    z = ['赵', '钱', '孙', '李', '周', '吴', '王', '郭', '牛', '黄', '范', '刘', '陈', '方', '张', '胡', '宋', '鹿',
         '白', '刘', '宁', "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩",
         "杨", "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜", "戚",
         "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦", "昌",
         "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳", "酆", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷",
         "贺", "倪", "汤", "滕", "殷", "罗"]
    zx = ["行", "锋", "舒", "善", "夏", "孝", "歌", "媚", "媛", "麟", "键", "麦", "锦", "铖", "锡", "武", "圣", "正",
          "聪", "康", "舟", "加", "云", "学", "桥", "亚", "劲", "隆", "亦", "亨", "亭", "京", "亮", "功", "问", "棋",
          "玲", "铭", "玺", "薇", "洁", "予", "玥", "玫", "洋", "玮", "环", "冈", "弘", "洲", "弟", "活", "弋", "玉",
          "致", "羿", "壮", "柏", "士", "政", "柔", "鍵", "柑", "声", "柠", "灵", "火", "柱", "柳", "焕", "琴", "妍",
          "如", "妹", "然", "西", "嘉", "妮", "路", "冰", "腾", "冬", "子", "航", "冠", "孟", "信", "军", "保", "基",
          "培", "俊", "再", "访", "渝", "芝", "礼", "渊", "清", "策", "芷", "花", "芳", "坤", "山", "筠", "芸", "顺",
          "芬", "芯", "帆", "显", "忻", "翔", "希", "蓉", "昱", "昭", "蓓", "江", "春", "昧", "翀", "蓝", "星", "志",
          "昕", "翰", "惠", "昌", "明", "忆", "昊", "昆", "汶", "翠", "有", "月", "朋", "沅", "沄", "墨", "朝", "沛",
          "虹", "敬", "朔", "朗", "边", "本", "河", "森", "治", "敏", "增", "鸿", "益", "婕", "钰", "鹏", "璧", "盛",
          "婉", "钦", "钧", "鹤", "国", "婵", "固", "婷", "璇", "钊", "婧", "漫", "谕", "莲", "莹", "卿", "莺", "韵",
          "泰", "升", "宛", "千", "莉", "华", "谷", "莎", "源", "南", "卓", "谦", "博", "建", "廷", "萱", "力", "宣",
          "崇", "陶", "济", "富", "维", "海", "绍", "经", "赵", "高", "浦", "起", "烟", "萍", "宪", "浩", "强", "涌",
          "群", "德", "思", "巧", "逸", "丽", "逢", "启", "涛", "佩", "蔚", "微", "羽", "君", "樑", "美", "征", "怡",
          "涵", "律", "斯", "奕", "晓", "奎", "方", "要", "奇", "晟", "新", "斌", "毅", "文", "晨", "景", "帮", "晶",
          "晴", "智", "燕", "伶", "仁", "健", "贵", "传", "伦", "伯", "付", "育", "剑", "心", "陆", "树", "泉", "会",
          "仪", "荔", "标", "伊", "任", "栋", "尚", "苑", "香", "小", "秦", "捷", "轮", "科", "轩", "英", "汉", "湖",
          "秀", "湘", "秉", "秋", "若", "纯", "爱", "纨", "沂", "爽", "磊", "红", "沁", "舜", "纾", "飘", "飞", "度",
          "峰", "峻", "意", "瑜", "溢", "庆", "燊", "骏", "李", "杏", "勤", "哲", "烨", "权", "瑗", "泓", "法", "烽",
          "材", "波", "杭", "烈", "郁", "来", "松", "泳", "品", "罡", "泽", "杰", "東", "评", "丹", "毓", "兴", "兰",
          "瑾", "中", "全", "瑶", "诚", "青", "业", "静", "世", "瑞", "言", "光", "先", "克", "万", "兆", "允", "元",
          "一", "竹", "植", "菲", "程", "楠", "菁", "馨", "菊", "豪", "才", "茜", "茗", "可", "召", "叶", "辉", "茂",
          "辰", "澄", "戈", "茹", "友", "达", "发", "福", "澜", "风", "成", "影", "恒", "彼", "淇", "珠", "蕊", "彤",
          "献", "彦", "彬", "彩", "淑", "彪", "珍", "珏", "金", "珊", "珂", "恩", "蕾", "里", "融", "淳", "睿", "裕",
          "皆", "娟", "娜", "娇", "娅", "威", "四", "皓", "素", "娴", "鸣", "紫", "娥", "娣", "佳", "龙", "赫", "田",
          "寒", "甲", "以", "阳", "桦", "利", "佑", "桐", "桑", "刚", "胜", "则", "桂", "寿", "生", "慰", "承", "汕",
          "雪", "雨", "雯", "立", "梦", "振", "宝", "楚", "梓", "雁", "楣", "雅", "雄", "勇", "耀", "楷", "梁", "梅",
          "蛟", "慧", "祺", "岚", "慷", "祥", "贞", "炜", "颖", "碧", "艳", "璐", "岳", "艺", "滨", "满", "滢", "岩",
          "良", "旭", "熙", "日", "天", "林", "旺", "旻", "枝", "观", "旋", "枫", "园", "琬", "露", "琪", "琦", "镇",
          "坚", "琼", "均", "自", "黛", "霭", "琰", "琳", "霖", "霞", "琅", "理", "乐", "之", "霆", "震", "霄", "义",
          "琛", "欣", "欢", "坪", "宁", "东", "宇", "安", "宏", "凯", "侠", "宗", "官", "凡", "双", "宜", "侨", "凤",
          "越", "凝", "倩", "依", "榕", "超", "家", "宸", "宽", "战", "运", "连", "远", "进", "伟", "迎", "第", "述",
          "荷", "馥", "厚", "迪", "荣", "曼", "炬", "悟", "邦", "民", "炳", "时", "缇", "炎", "水", "平", "悦", "和",
          "幻", "咏", "永", "广", "真", "眉", "煦", "姬", "姣"]
    if random.randint(0, 10) < 7:
        strz = z[random.randint(0, len(z) - 1)] + zx[random.randint(0, len(zx) - 1)] + zx[
            random.randint(0, len(zx) - 1)]
    else:
        strz = z[random.randint(0, len(z) - 1)] + zx[random.randint(0, len(zx) - 1)]
    return strz


def get_tel():
    x = [random.randint(130, 139), random.randint(150, 159), random.randint(170, 179), random.randint(180, 189)]
    strx = str(x[random.randint(0, 3)])
    for i in range(0, 8):
        b = random.randint(0, 9)
        strx = strx + str(b)
    return strx


def getCookie(x):
    import execjs
    # var arg1 = 'D903259129C2726AE4093900A0687AAEADDBE11F';
    ctx = execjs.compile("""

    var arg_parse = function(arg){
    var _0x4b082b = [0xf,0x23,0x1d,0x18,0x21,0x10,0x1,0x26,0xa,0x9,0x13,0x1f,0x28,0x1b,0x16,0x17,0x19,0xd,0x6,0xb,0x27,0x12,0x14,0x8,0xe,0x15,0x20,0x1a,0x2,0x1e,0x7,0x4,0x11,0x5,0x3,0x1c,0x22,0x25,0xc,0x24];
    var _0x4da0dc = [];

    var _0xl2605e = '';
    for (var _0x20a7bf = 0; _0x20a7bf < arg["length"]; _0x20a7bf++) {
        var _0x385ee3 = arg.substr(_0x20a7bf,1);
        for (var _0x217721 = 0; _0x217721 < _0x4b082b["length"]; _0x217721++) {
            if (_0x4b082b[_0x217721] == _0x20a7bf + 1) {
                _0x4da0dc[_0x217721] = _0x385ee3;
            }
        }
    }
    _0x12605e = _0x4da0dc["\x6a\x6f\x69\x6e"]("");
    return _0x12605e;
};

var l = function(arg1) {
    ;var _0x5e8b26 = '3000176000856006061501533003690027800375'
    String["prototype"]['hexXor'] = function(_0x4e08d8) {
        var _0x5a5d3b = '';
        for (var _0xe89588 = 0x0; _0xe89588 < this["length"] && _0xe89588 < _0x4e08d8["length"]; _0xe89588 += 0x2) {
            var _0x401afl = parseInt(this["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x105f59 = parseInt(_0x4e08d8["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x189e2c = (_0x401afl ^ _0x105f59)["toString"](0x10);
            if (_0x189e2c["length"] == 0x1) {
                _0x189e2c = '\x30' + _0x189e2c;
            }
            _0x5a5d3b += _0x189e2c;
        }
        return _0x5a5d3b;
    };
    var _0x23a392 = arg_parse(arg1);
    var arg2 = _0x23a392["hexXor"](_0x5e8b26);
    return arg2
};
    """)
    return ctx.call("l", x)


def json2String(data):
    json_data = dict(data)
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


def getJqParam(needTime, curid, rndnum):
    import execjs
    jqParamJS = ""
    try:
        f = open('/Users/xuanhao.guo/Downloads/jqParam.js', 'r')
        jqParamJS = f.read()
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    finally:
        f.close()
    if jqParamJS == "":
        return 'abc'
    ctx = execjs.compile(jqParamJS)
    return ctx.call("abc", needTime, curid, rndnum)


def intoDB(wjx_id, starttime, ip, answer):
    import MySQLdb

    db = None
    try:
        db = MySQLdb.connect(db_ip, db_user, db_pass, db_name, db_port, connect_timeout=5)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        sql = 'INSERT INTO data_log(wjx_id, starttime, ip, answer, date, pwd) VALUE ("%s", "%s", "%s", "%s", "%s", "%s")' % (
        wjx_id, starttime, ip, answer, time.strftime('%Y.%m.%d', time.localtime(time.time())),
        os.path.realpath(__file__))
        # print sql
        cursor.execute(sql)
        db.commit()
        return
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        return
    finally:
        if db:
            db.close()


def notifyToDB():
    import MySQLdb

    db = None
    try:
        db = MySQLdb.connect(db_ip, db_user, db_pass, db_name, db_port, connect_timeout=5)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        sql = 'update need set id = %s; ' % (random.randint(1, 1000000))
        # print sql
        cursor.execute(sql)
        db.commit()
        return
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        return
    finally:
        if db:
            db.close()


def getFromDB():
    import MySQLdb

    db = None
    try:
        db = MySQLdb.connect(db_ip, db_user, db_pass, db_name, db_port, connect_timeout=5)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        t = datetime.datetime.now() - datetime.timedelta(minutes=9)
        t = str(t.strftime("%Y-%m-%d %H:%M:%S"))
        sql = "SELECT * FROM salary where creat_time >= '%s' and is_use = 0 limit 1 for update" % t
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) <= 0:
            return '1', '2', '3'
        for row in results:
            id = row[0]
            nc_token = row[1]
            nc_sig = row[2]
            nc_csessionid = row[3]
            creat_time = row[4]
            is_use = row[5]
            # 打印结果
            print "id=%s,nc_token=%s,nc_sig=%s,nc_csessionid=%s,creat_time=%s,is_use=%s" % \
                  (id, nc_token, nc_sig, nc_csessionid, creat_time, is_use)

        # sql = "UPDATE salary SET is_use = 1 WHERE id = %s" % (id)
        sql = "DELETE from salary  WHERE id <= %s" % (id)
        cursor.execute(sql)
        db.commit()
        return nc_token, nc_sig, nc_csessionid
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        print "Error: unable to fecth data"
        return '1', '2', '3'
    finally:
        if db:
            db.close()


def captcha(proxy):
    try:
        updateToDB()
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
    try:
        nc_token, nc_sig, nc_csessionid = getFromDB()
        if len(nc_token) >= 5 or len(nc_sig) >= 5 or len(nc_csessionid) >= 5:
            return nc_token, nc_sig, nc_csessionid
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)

    print '已经告诉生产者去生成验证码了，请等待'
    return '1', '2', '3'


def getIp():
    ips()
    if appointIP:
        url = random.choice(ip)
    else:
        url = ipURL
    try:
        s = requests.get(url, timeout=3)
        ip_str = s.text
        ip_str = ip_str.replace("\t", "")
        ip_str = ip_str.replace("\r", "")
        ip_str = ip_str.replace("\n", "")
        print(ip_str)
        return ip_str
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        return "0:0"


def getAll(curid, needTime, ip_proxy):
    if wjx_type == "wj":
        host = "www.wjx.cn"
    if wjx_type == "tp":
        host = "tp.wjx.top"
    if wjx_type == "ks":
        host = "ks.wjx.top"

    if str(curId).isdigit():
        url = "https://%s/m/%s.aspx" % (host, curId)
    else:
        url = "https://%s/vm/%s.aspx" % (host, curId)

    head = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    ipp = "0:0"
    if 1 == 2:
        ips()
        while True:
            ipp = ip[random.randint(0, len(ip) - 1)] + str(random.randint(0, 255))
            if map_ip.has_key(ipp) == False:
                map_ip[ipp] = 1
                break
        f = open('map_ip_' + str(curid) + '.txt', 'a+')
        f.write('map_ip is : ' + str(map_ip) + "\n")
        f.close()
        head["X-Forwarded-For"] = ipp

    try:
        proxies = {"http": "http://%s" % ip_proxy,
                   "https": "https://%s" % ip_proxy}

        if ip_proxy == "0:0":
            proxies = {
                "http": "http://81.68.221.80:26881",
                "https": "http://81.68.221.80:26881",
            }
        global rndnum_temp
        global cookie_temp
        global curId2
        global Verify
        if rndnum_temp == "":
            s = requests.get(url, headers=head, timeout=3)  # , proxies=proxies)
            if s.text.find("此问卷正在编辑或者暂停状态") != -1:
                postTo(str(curid) + ' 暂停了 has error!')
                postToWx(str(curid) + ' 暂停了 has error!')
                sys.exit()
                return False, False

            cookie = s.cookies
            cookies_dict = requests.utils.dict_from_cookiejar(cookie)
            c = json2String(cookies_dict)
            rndnum = re.search("rndnum=\".+\";", s.text).group(0)[8:-2]
            if str(curid).isdigit():
                Verify = 0
            else:
                x1 = s.text.find("activityId =")
                x2 = s.text[x1:].find(";")
                curId2 = int(s.text[x1 + 12:x1 + x2]) ^ 2130030173
            rndnum_temp = rndnum
            cookie_temp = c

            Verify = s.text.find("useAliVerify =1")
        else:
            rndnum = rndnum_temp
            c = cookie_temp

        if Verify != -1:
            notifyToDB()
            nc_token, nc_sig, nc_csessionid = captcha(ip_proxy)
            # s = requests.get(url, headers=head, proxies=proxies, timeout=3)

        # jqnonce = re.search("jqnonce=\".+\";", s.text).group(0)[9:-2]
        jqnonce = '%s-%s-%s-%s-d8e0d8e8f40a' % (''.join(random.sample(string.ascii_letters + string.digits, 8)),
                                                ''.join(random.sample(string.ascii_letters + string.digits, 4)),
                                                ''.join(random.sample(string.ascii_letters + string.digits, 4)),
                                                ''.join(random.sample(string.ascii_letters + string.digits, 4))
                                                )
        ktimes = random.randint(110, 428) + 2
        from urllib import quote
        jqsign = str(getJqsign(jqnonce, ktimes))
        ran_str1 = ''.join(random.sample(string.ascii_letters + string.digits, 18))
        ran_str2 = ''.join(random.sample(string.ascii_letters + string.digits, 18))
        u_asec = "099%23" + ''.join(random.sample(string.ascii_letters + string.digits, 18))
        c = c + ";u_asec=%s;CNZZDATA4478442=cnzz_eid=%d-%d-&ntime=%d;ssxmod_itna=%s;ssxmod_ktimd=%s" % (
            u_asec, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), ran_str2, str(ktimes))

        if str(curid).isdigit():
            jqParam = getJqParam(needTime, curid, rndnum)
            params = {
                "curid": curid,
                "starttime": needTime,
                "source": 'directphone',
                "submittype": 1,
                "ktimes": ktimes,
                "hlv": 1,
                "rn": rndnum,
                "t": int(time.time() * 1000),
                "jqnonce": jqnonce,
                "jqsign": jqsign,
                "jqpram": jqParam,
            }
        else:
            jqParam = getJqParam(needTime, curId2, rndnum)

            params = {
                "shortid": curid,
                "starttime": needTime,
                "source": 'directphone',
                "submittype": 1,
                "ktimes": ktimes,
                "hlv": 1,
                "rn": rndnum,
                "t": int(time.time() * 1000),
                "jqnonce": jqnonce,
                "jqsign": jqsign,
                "jqpram": jqParam,
            }

        if random.randint(1, 10) <= 5:
            params["source"] = "微信"

        if Verify != -1:
            params["nc_token"] = nc_token
            params["nc_sig"] = nc_sig,
            params["nc_csessionid"] = nc_csessionid,
            params["nc_scene"] = "ic_activity",
    except Exception, e:
        print str(Exception)
        print str(e)
        print str(e.message)
        params, c = False, False
    return params, c


def number_to_base26(number):
    if number == 0:
        return 'A'
    result = ''
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        result = chr(remainder + 65) + result
    return result


if __name__ == '__main__':
    curId = 'eaHPyBq'

    time1 = 120
    time2 = 200
    url = "https://www.wjx.cn/joinnew/processjq.ashx"

    doNumber = 15  # 刷几次
    titleNumber = 42  # 多少个题目

    makeData(titleNumber)

    debug = False
    if debug:
        for i in range(doNumber):
            print(i)
            makeData(titleNumber)
            count = count + 1

    hezuo = False

    i = 0
    data = ''
    while i < doNumber:

        current_time = datetime.datetime.now()
        while current_time.hour in range(0, 7):
            current_time = datetime.datetime.now()
            print 'now time is %s:%s, so we cannot run it' % (current_time.hour, current_time.minute)
            time.sleep(60)

        ip_proxy = ""
        print i
        needTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime((time.time() - random.randint(time1, time2))))
        params, Cookie = getAll(curId, needTime, ip_proxy)
        if params == False:
            print 'a is not ok, restart!!!'
            time.sleep(10)
            continue
        ip_proxy = ""
        print 'start -- ' + str(i + 1) + ' -- '
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        suc, data = wjx(titleNumber, url, Cookie, params, data, ip_proxy)
        print 'end --' + str(i + 1) + ' -- '
        if suc == False:
            print 'is not ok, restart!!!'
            time.sleep(10)
        else:
            global count
            count = count + 1
            i = i + 1
            # time.sleep(random.randint(20, 80)) # 大约1.5小时填100份
            # time.sleep(random.randint(20, 120)) # 大约2小时填100份
            time.sleep(random.randint(20, 180))  # 大约2.5小时填100份
            # time.sleep(random.randint(20, 280)) # 大约4小时填100份
            # time.sleep(random.randint(20, 580)) # 大约8.5小时填100份

    postToWx(str(curId) + ' 本次run已经完成， 共' + str(doNumber) + '份')
    if hezuo:
        postToWorkWx(str(curId) + ' 本次run已经完成， 共' + str(doNumber) + '份')
    if len(stash_list) > 0:
        os.system("/usr/bin/python3 /Users/xuanhao.guo/Downloads/spss.py %s" % curId)
        postToWx('http://106.52.55.33/download?id=%s' % curId)
