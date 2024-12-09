# encoding: UTF-8

import requests
import sys
from bs4 import BeautifulSoup
import random
from string import Template
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #set default encoding to utf-8


listString = ""
relationString = ""
jump = ""
danxuan100 = []
gundong100 = []
gundongtable = []
notFindList = []
list = []
LEN = []
titleContent = []
typeList = [-1, ]
for i in range(0, 2000):
    list.append([1000, 0])
    LEN.append(0)
    notFindList.append("0")


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"

    else:
        print
        "---  There is this folder!  ---"




def addempty(s):
    list = s.split("\n")
    r = ""
    for i in range(len(list)):
        r = r + "        " + list[i] + "\n"
    return r

def copy_model(curId, allTitles, type):
    global jump
    global relationString
    relationString = addempty(relationString)
    jump = addempty(jump)

    with open('model_new5.txt') as f:
    #with open('model3.txt') as f:
        data = f.read()
    #print listString
    #print relationString
    print(relationString)
    print(listString)
    data = Template(data)
    data = data.safe_substitute(list=listString, curId=curId, titleNumber=allTitles, relation=relationString, jump=jump, type=type, danxuan100=danxuan100, \
                                gundongtable=gundongtable, gundong100=gundong100
                                )

    #file = "0528"
    #mkdir(file)
    filename =  str(time.strftime("%m-%d_%H.%M.%S_", time.localtime()) ) + str(curId) + '.py'
    with open(filename, 'w') as f:
        f.write(data)
    f.close()
    print '生成了文件' + filename
    print '题目数为' + str(allTitles) + ',请仔细和对'



def danxuan(every, num):
    notFindList[num] = "[1, [-3, 10]]"
    list[num] = [1]
    count = 1
    x = -1
    try:
        for i in range(0, len(every.contents)):
            #print every.contents[i].get("class")
            if len(every.contents[i].get("class")) > 0:
                if 'field-label' in every.contents[i].get("class"):
                    titleContent.append([u'第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
                if 'ui-controlgroup' in every.contents[i].get("class"):
                    x = i
                    break
        print x
        for i in every.contents[x].contents:
            list[num].append([count, random.randint(10, 40)])
            count = count + 1
        print 'list[' + str(num) + '] = ' + str(list[num])
        global listString
        listString = listString + '    ' +  'list[' + str(num) + '] = ' + str(list[num]) + '\n'
    except:
        print 'a'


def table(every, num):
    notFindList[num] = "[1, [-3, 10]]"
    list[num] = [1]
    count = 1

    x = -1
    try:
        for i in range(0, len(every.contents)):
            if len(every.contents[i].get("class")) > 0:
                if 'scale-div' in every.contents[i].get("class"):
                    x = i
                    break
        for i in every.contents[x].contents[0].contents[1]:
            list[num].append([count, random.randint(10,40)])
            count = count + 1
        print 'list[' + str(num) + '] = ' + str(list[num])
        global listString
        listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

    except:
        print 'a'


def xiala(every, num):
    notFindList[num] = "[1, [-3, 10]]"
    list[num] = [1]
    count = 1
    try:
        x = -1
        for i in range(0, len(every.contents)):
            print every.contents[i].get("class")
            if len(every.contents[i].get("class")) > 0:
                if 'field-label' in every.contents[i].get("class"):
                    titleContent.append([u'第%s题：' % num, str(every.contents[i].contents).decode('unicode_escape')])
                if 'ui-select' in every.contents[i].get("class"):
                    x = i
                    break

        for i in range(1, len(every.contents[x].contents[0].contents[0])):

            list[num].append([count, random.randint(10, 40)])
            count = count + 1
        print 'list[' + str(num) + '] = ' + str(list[num])
        global listString
        listString = listString + '    ' +  'list[' + str(num) + '] = ' + str(list[num]) + '\n'
    except:
        print 'a'

def paixu(every, num):
    list[num] = [25]
    count = 1
    w = 0
    for x in range(0, len(every.contents)):
        if len(every.contents[x].get("class")) > 0:
            #if 'field-label' in every.contents[i].get("class"):
            #    titleContent.append([u'第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
            if 'ui-controlgroup' in every.contents[x].get("class"):
                w = x
                break

    if every.attrs.has_key("maxvalue"):
        if every.attrs.has_key("minvalue"):
            list[num].append('random.randint(%s, %s)' % (every.attrs["minvalue"], every.attrs["maxvalue"]))
        else:
            list[num].append('random.randint(%s, %s)' % (1, every.attrs["maxvalue"]))
    else:
        if every.attrs.has_key("minvalue"):
            list[num].append('random.randint(%s, %s)' % (every.attrs["minvalue"], len(every.contents[w].contents)))
        else:
            list[num].append('random.randint(%s, %s)' % (1, len(every.contents[w].contents)))



    for i in every.contents[w].contents:
        list[num].append([count, random.randint(10, 40)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' +  'list[' + str(num) + '] = ' + str(list[num]) + '\n'
    LEN[num] = len(every.contents[1].contents)

    rt = "[1, ['"
    for temp in range(0, LEN[num]):
        rt = rt + "-3,"
    notFindList[num] = rt[:-1] + "', 10]]"
    #print 'aaaa', notFindList[num]


def tiankong(every, num):
    notFindList[num] = "[1, ['(跳过)', 10]]"
    list[num] = [1]
    for i in range(5):
        list[num].append(["", 10])
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def duoxuan(every, num):
    notFindList[num] = "[1, [-3, 10]]"
    list[num] = [10]
    count = 1
    x = -1
    for i in range(0, len(every.contents)):
        print every.contents[i].get("class")
        if len(every.contents[i].get("class")) > 0:
            if 'field-label' in every.contents[i].get("class"):
                titleContent.append([u'第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
            if 'ui-controlgroup' in every.contents[i].get("class"):
                x = i
                break
    for i in every.contents[x].children:
        list[num].append([count, random.randint(20, 80)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'


def zuishao(every, num, min):
    notFindList[num] = "[1, [-3, 10]]"
    min = int(min)
    list[num] = [12, min]
    count = 1
    x = -1
    for i in range(0, len(every.contents)):
        print every.contents[i].get("class")
        if len(every.contents[i].get("class")) > 0:
            if 'field-label' in every.contents[i].get("class"):
                titleContent.append([u'第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
            if 'ui-controlgroup' in every.contents[i].get("class"):
                x = i
                break
    for i in every.contents[x].children:
        list[num].append([count, random.randint(20, 80)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'


def zuiduo(every, num, max):
    notFindList[num] = "[1, [-3, 10]]"
    max = int(max)
    list[num] = [11, max]
    count = 1
    x = -1
    for i in range(0, len(every.contents)):
        print every.contents[i].get("class")
        if len(every.contents[i].get("class")) > 0:
            if 'field-label' in every.contents[i].get("class"):
                titleContent.append(['第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
            if 'ui-controlgroup' in every.contents[i].get("class"):
                x = i
                break
    for i in every.contents[x].children:
        list[num].append([count, random.randint(20, 80)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def xianzhi(every, num, min, max):
    notFindList[num] = "[1, [-3, 10]]"
    min = int(min)
    max = int(max)
    list[num] = [13, min, max]
    count = 1
    x = -1
    for i in range(0, len(every.contents)):
        print every.contents[i].get("class")
        if len(every.contents[i].get("class")) > 0:
            if 'field-label' in every.contents[i].get("class"):
                titleContent.append([u'第%s题：' % num , str(every.contents[i].contents).decode('unicode_escape')])
            if 'ui-controlgroup' in every.contents[i].get("class"):
                x = i
                break
    for i in every.contents[x].children:
        list[num].append([count, random.randint(20, 80)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def juzhen(every, num):
    list[num] = [20]
    rows =  every.tbody
    count = 0
    rowR = 0
    for row in rows:
        count = count + 1
        a = dict(row.attrs)
        if a.has_key('rowindex'):
            rowR = rowR + 1
        if count == 1:
            column = len(row.contents)

    if str(row.contents[0]).find("rowtitlediv") !=- 1:
        column = column - 1
    #print '#num ' + str(num) + ' row is ' + str(rowR) + ' column is ' + str(column)
    for i in range(rowR):
        temp = []
        for j in range(column):
            temp.append([j + 1, random.randint(10, 50)])
        list[num].append(temp)
    #print 'list[' + str(num) + '] = ' + str(list[num])
    print 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\'
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\' + '\n'
    LEN[num] = len(list[num])
    rt = "[1, ['"
    for temp in range(1, LEN[num]):
        rt = rt + str(temp) + "!-3,"

    notFindList[num] = rt[:-1] + "', 10]]"
    for i in range(1, len(list[num])):
        print str(list[num][i]) + ', \\'
        listString = listString + '    ' + str(list[num][i]) + ', \\' + '\n'
    print ']'
    listString = listString + '    ' + ']' + '\n'


def gundong(every, num):
    list[num] = [20]
    rows =  every.tbody
    count = 0
    rowR = 0
    column = -1
    try:
        for row in rows:
            count = count + 1
            a = dict(row.attrs)
            if a.has_key('id'):
                rowR = rowR + 1
            if count == 2:
                #column = len(row.contents)
                column1 = int(row.contents[0].contents[0].contents[0].attrs["max"])
        #print '#num ' + str(num) + ' row is ' + str(rowR) + ' column is ' + str(column)

        gundongtable.append(num)
        if column1 == 100:
            column = 5
            gundong100.append(num)
        else:
            column = column1
        rowR = rowR / 2
        for i in range(rowR):
            temp = []
            for j in range(column):
                temp.append([j + 1, random.randint(10, 50)])
            list[num].append(temp)

        #print 'list[' + str(num) + '] = ' + str(list[num])
        print 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\'
        global listString
        listString = listString + '    ' + 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\' + '\n'
        LEN[num] = len(list[num])
        rt = "[1, ['"
        for temp in range(1, LEN[num]):
            rt = rt + str(temp) + "!-3^"

        notFindList[num] = rt[:-1] + "', 10]]"
        for i in range(1, len(list[num])):
            print str(list[num][i]) + ', \\'
            listString = listString + '    ' + str(list[num][i]) + ', \\' + '\n'
        print ']'
        noti = ''
        if column1 == 100:
            noti = '#按1~5做即可，后面会自动乘以20-random(0,19)'
        listString = listString + '    ' + ']' + noti + '\n'

    except Exception as e:
        print(e)


def huaidong(every, num):
    try:

        list[num] = [1]
        import re
        rows = every.input
        rows = int(re.search("max=\"[0-9]+\"", str(every.input)).group(0)[5:-1])
        count = 1
        notFindList[num] = "[1, [-3, 10]]"

        column = -1
        if rows == 100:
            column = 5
            danxuan100.append(num)

        else:
            column = rows

        for i in range(0, column):
            list[num].append([count, random.randint(10, 40)])
            count = count + 1
        print 'list[' + str(num) + '] = ' + str(list[num])
        global listString
        noti = ""
        if rows == 100:
            noti = '#按1~5做即可，后面会自动乘以20-random(0,19)'
        listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + noti + '\n'
        #print(listString)



    except Exception as e:
        print(e)


def quanzhong(every, num):
    list[num] = [16]
    rows =  every.tbody
    total = int(every.attrs["total"])
    print(total)
    count = 0
    rowR = 0
    column = -1
    try:
        for row in rows:
            count = count + 1
            a = dict(row.attrs)
            if a.has_key('id'):
                rowR = rowR + 1


        rowR = rowR / 2
        print(rowR)
        temp = []
        for i in range(rowR):
            temp.append(['a%s' % i])
        list[num].append(temp)

        #print 'list[' + str(num) + '] = ' + str(list[num])
        print 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\'
        global listString
        #listString = listString + '    ' + 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\' + '\n'
        LEN[num] = len(list[num])
        rt = "[1, ['"
        for temp in range(1, rowR + 1):
            rt = rt + str(temp) + "!-3^"

        notFindList[num] = rt[:-1] + "', 10]]"

        listString = listString + '    ' + "while True: \n"

# n        while True:
#             a1 = random.randint(3, 5)  # a
#             a2 = random.randint(2, 4)  # c d
#             a3 = random.randint(2, 4)  # b
#             a4 = random.randint(2, 4)  # e
#
#             a5 = 10 - a1 - a2 - a3 - a4
#             if a5 >= 0 and a5 <= 3:
#                 list[7] = [16, [a1], [a2], [a3], [a4], [a5]]
#                 break

        t = ""
        t1 = ""
        for i in range(1, rowR + 1):
            if i < rowR:
                listString = listString + '        ' + 'a%s = random.randint(20, 30)' % i + '#这里写第%s小题的比例范围\n' % i
                t = t + "- a%s" % i
                t1 = t1 + ", [a%s]" % i
            else:
                listString = listString + '        ' + '\n'
                listString = listString + '        ' + 'a%s = %s %s' % (i, total, t) + '\n'
                listString = listString + '        ' + 'if 0 <= a%s <= 10:' % (i) + '\n'
                t1 = t1 + ", [a%s]" % i
                listString = listString + '        ' + '    ' + 'list[' + str(num) + '] = [' + str(list[num][0]) + '%s' % t1 + ']\n'
                listString = listString + '        ' + '    ' + 'break' + '\n'

        #print(listString)



    except Exception as e:
        print(e)


def jumpToDanxuan(every, num):
    if every.attrs.has_key("anyjump") and every.attrs['anyjump'] != '0':#说明这题出现了就跳到anyjump去
        to = int(every.attrs['anyjump'])
        global jump

        if to <= 1:
            to = len(typeList) + 1
        if to > num + 1:
            jump = jump + 'if i == %s and hasjump[i] == 0:\n' % num
            for x in range(num + 1, to):
                if notFindList[x] != "0":
                    jump = jump + '    list[%s] = %s\n' % (x, notFindList[x])
                    jump = jump + '    cronbach[%s] = [0]\n' % (x)
                    jump = jump + '    hasjump[%s] = 1\n' % (x)
                else:
                    jump = jump + '    list[%s] = []\n' % (x)
                    jump = jump + '    cronbach[%s] = [0]\n' % (x)
                    jump = jump + '    hasjump[%s] = 1\n' % (x)
        return
    try:
        #否则跟选项有关
        count = 1
        #print len(every.contents[1].contents)
        x = -1
        for i in range(0, len(every.contents)):
            print every.contents[i].get("class")
            if len(every.contents[i].get("class")) > 0:
                if 'ui-controlgroup' in every.contents[i].get("class"):
                    x = i
                    break
        print x
        for i in every.contents[x].contents:
            choice = i.find('input')
            print choice
            if choice.attrs.has_key('jumpto'):
                print (str(num) + ' choice ' + str(count) + ' will jumpTo ' + choice.attrs['jumpto'])
                to = int(choice.attrs['jumpto'])
                print 'to is :', to
                global jump

                if to <= 1:
                    to = len(typeList)
                    print 'to is: ', to
                if to > num + 1:
                    jump = jump + 'if i == %s and AinB(choose[%s], [%s]):\n' % (num, num, count)
                    for x in range(num+1, to):
                        if notFindList[x] != "0":
                            jump = jump + '    list[%s] = %s\n' % (x, notFindList[x])
                            jump = jump + '    cronbach[%s] = [0]\n' % (x)
                            jump = jump + '    hasjump[%s] = 1\n' % (x)
                        else:
                            jump = jump + '    list[%s] = \n' % (x)
                            jump = jump + '    cronbach[%s] = [0]\n' % (x)
                            jump = jump + '    hasjump[%s] = 1\n' % (x)
            count = count + 1
            #return
    except:
        print 'a'

    try:



        x = -1
        for i in range(0, len(every.contents)):

            print every.contents[i].get("class")
            if len(every.contents[i].get("class")) > 0:
                if 'ui-select' in every.contents[i].get("class"):
                    x = i
                    break
        count = 0
        for i in every.contents[x].contents[0].contents[0]:
            if i.attrs.has_key("jumpto"):
                print (str(num) + ' choice ' + str(count) + ' will jumpTo ' + i.attrs['jumpto'])
                to = int(i.attrs['jumpto'])
                global jump

                if to <= 1:
                    to = len(typeList) + 1
                    print 'to is: ', to
                if to > num + 1:
                    jump = jump + 'if i == %s and AinB(choose[%s], [%s]):\n' % (num, num, count)
                    for x in range(num + 1, to):
                        if notFindList[x] != "0":
                            jump = jump + '    list[%s] = %s\n' % (x, notFindList[x])
                            jump = jump + '    cronbach[%s] = [0]\n' % (x)
                            jump = jump + '    hasjump[%s] = 1\n' % (x)
                        else:
                            jump = jump + '    list[%s] = []\n' % (x)
                            jump = jump + '    cronbach[%s] = [0]\n' % (x)
                            jump = jump + '    hasjump[%s] = 1\n' % (x)
            count = count + 1

    except:
        print 'a'


#将请求的内容解析
def plain(s):
    Soup = BeautifulSoup(s.text)
    #i = Soup.fieldset.contents
    num = 1
    #print Soup.find_all("fieldset")
    for i in Soup.find_all("fieldset"):

        for every in i:
            if every.attrs.has_key("type") == False:
                continue
            type = every.attrs["type"]
            type = int(type)

            typeList.append(type)
            if type == 1:
                tiankong(every, num)
            elif type == 2:
                tiankong(every, num)
            elif type == 3:
                danxuan(every, num)
            elif type == 4:
                if every.attrs.has_key("maxvalue"):
                    if every.attrs.has_key("minvalue"):
                        xianzhi(every, num,every.attrs["minvalue"], every.attrs["maxvalue"])
                    else:
                        zuiduo(every, num, every.attrs["maxvalue"])
                elif every.attrs.has_key("minvalue"):
                    zuishao(every, num, every.attrs["minvalue"])
                else:
                    duoxuan(every, num)
            elif type == 5:
                table(every, num)
            elif type == 6:
                juzhen(every, num)
            elif type == 7:
                xiala(every, num)
            elif type == 8:
                huaidong(every, num)
            elif type == 11:
                paixu(every, num)
            elif type == 9:
                gundong(every, num)
            elif type == 12:
                quanzhong(every, num)
            else:
                print '第 ' + str(num) + '题是未知的'
            num = num + 1

    allTitles = num - 1
    print '#一共' + str(num - 1) + '个题数'

    num = 1
    for i in Soup.find_all("fieldset"):
        global relationString
        for every in i:
            if every.attrs.has_key("type") == False:
                continue
            if every.attrs.has_key("relation"):
                #print '#第 ' + str(num) + '题有relation'
                relation = every.attrs["relation"]
                print relation

                if relation == "0":
                    relationString = relationString + 'if i == 1:\n'
                    relationString = relationString + '    list[%s] = %s\n' % (num, notFindList[num])
                    relationString = relationString + '    cronbach[%s] = [0]\n' % (num)
                    relationString = relationString + '    hasjump[%s] = 1\n' % (num)

                    continue
                if relation.find("|") != -1:  #且的关系
                    s = 'if i == %s:\n'
                    s = s + '    if'
                    len1 = len(relation.split("|"))
                    relationlist = relation.split("|")
                    tihaolist = []
                    try:
                        for rt in range(0, len1):
                            a = relationlist[rt]
                            tihao = a.split(",")[0]

                            tihaolist.append(int(tihao))
                            xuanxiang = a.split(",")[1]
                            if xuanxiang.find(";") != -1:
                                xuanxianglist = xuanxiang.split(";")
                                all = False
                            elif xuanxiang.find(".") != -1:
                                xuanxianglist = xuanxiang.split(".")
                                all = True
                            else:
                                xuanxianglist = [xuanxiang]
                                all = False

                            if all:
                                s = s + ' AinBALL(choose[%s], [%s])' % (tihao, ','.join(xuanxianglist))
                            else:
                                s = s + ' AinB(choose[%s], [%s])' % (tihao, ','.join(xuanxianglist))

                            if rt < len1 - 1:
                                s = s + ' and'
                            else:
                                s = s + ' :\n'
                                s = s + '        pass\n'
                                s = s + '    else:\n'
                                s = s + '        list[%s] = %s\n' % (num, notFindList[num])
                                s = s + '        cronbach[%s] = [0]\n' % (num)
                                s = s + '        hasjump[%s] = 1\n' % (num)
                                relationString = relationString + (s % max(tihaolist))
                    except:
                        print 'aaa'

                elif relation.find("$") != -1:  # 或的关系
                    s = 'if i == %s:\n'
                    s = s + '    if'
                    len1 = len(relation.split("$"))
                    relationlist = relation.split("$")
                    tihaolist = []
                    for rt in range(0, len1):
                        a = relationlist[rt]
                        tihao = a.split(",")[0]
                        tihaolist.append(int(tihao))
                        xuanxiang = a.split(",")[1]
                        if xuanxiang.find(";") != -1:
                            xuanxianglist = xuanxiang.split(";")
                            all = False
                        elif xuanxiang.find(".") != -1:
                            xuanxianglist = xuanxiang.split(".")
                            all = True
                        else:
                            xuanxianglist = [xuanxiang]
                            all = False

                        if all:
                            s = s + ' AinBALL(choose[%s], [%s])' % (tihao, ','.join(xuanxianglist))
                        else:
                            s = s + ' AinB(choose[%s], [%s])' % (tihao, ','.join(xuanxianglist))

                        if rt < len1 - 1:
                            s = s + ' or'
                        else:
                            s = s + ' :\n'
                            s = s + '        pass\n'
                            s = s + '    else:\n'
                            s = s + '        list[%s] = %s\n' % (num, notFindList[num])
                            s = s + '        cronbach[%s] = [0]\n' % (num)
                            s = s + '        hasjump[%s] = 1\n' % (num)
                            relationString = relationString + (s % max(tihaolist))

                else:
                    #continue
                    #if num in []:
                    #    continue
                    if relation == "-1":
                        print("tiaoguo")
                        continue
                    tihao = relation.split(",")[0]
                    xuanxiang = relation.split(",")[1]
                    if xuanxiang.find(";") != -1:
                        xuanxianglist = xuanxiang.split(";")
                        all = False
                    elif xuanxiang.find(".") != -1:
                        xuanxianglist = xuanxiang.split(".")
                        all = True
                    else:
                        xuanxianglist = [xuanxiang]
                        all = False

                    if 1 == 1:#i == tihao:
                        relationString = relationString + 'if i == %s:\n' % tihao
                        if all == True:
                            relationString = relationString + '    if AinBALL(choose[%s], [%s]):\n' % (tihao, ','.join(xuanxianglist))
                            relationString = relationString + '        pass\n'
                            relationString = relationString + '    else:\n'
                            relationString = relationString + '        list[%s] = %s\n' % (num, notFindList[num])
                            relationString = relationString + '        cronbach[%s] = [0]\n' % (num)
                            relationString = relationString + '        hasjump[%s] = 1\n' % (num)
                            #if AinBALL(choose[tihao],xuanxianglist):
                            #    print '此题有意义'
                            #else:
                            #    print '此题跳过'
                        else:
                            relationString = relationString + '    if AinB(choose[%s], [%s]):\n' % (tihao, ','.join(xuanxianglist))
                            relationString = relationString + '        pass\n'
                            relationString = relationString + '    else:\n'
                            relationString = relationString + '        list[%s] = %s\n' % (num, notFindList[num])
                            relationString = relationString + '        cronbach[%s] = [0]\n' % (num)
                            relationString = relationString + '        hasjump[%s] = 1\n' % (num)
                            #if AinB(choose[tihao],xuanxianglist):
                            #    print '此题有意义'
                            ##else:
                            #    print '此题跳过'
            num = num + 1

    num = 1
    for i in Soup.find_all("fieldset"):
        for every in i:
            if every.attrs.has_key("type") == False:
                continue
            if every.attrs.has_key("hasjump"):
                jumpToDanxuan(every, num)

            num = num + 1

    print relationString
    print jump
    return allTitles


if __name__ == '__main__':

    curId = 'O1xgl1E'

    type = "wj"


    if type == "wj":
        host = "www.wjx.cn"
    if type == "tp":
        host = "tp.wjx.top"
    if type == "ks":
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
        "X-Forwarded-For": "1.2.3.4"
    }
    ip_proxy = "218.27.206.138:45163"
    proxies = {"http": "http://%s" % ip_proxy,
               "https": "https://%s" % ip_proxy}
    s = requests.get(url, headers=head, verify=False)#, proxies=proxies)
    print(s.text)



    allTitles = plain(s)
    copy_model(curId, allTitles, type)

    for title in titleContent:
        print str(title).decode('unicode_escape')
