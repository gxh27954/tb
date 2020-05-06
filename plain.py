# encoding: UTF-8

import requests
import sys
from bs4 import BeautifulSoup
import random
from string import Template
import time

listString = ""
relationString = ""

list = []
typeList = [-1, ]
for i in range(0, 200):
    list.append([1000, 0])


def copy_model(curId, allTitles):
    with open('model.txt') as f:
        data = f.read()

    data = Template(data)
    data = data.safe_substitute(list=listString, curId=curId, titleNumber=allTitles, relation=relationString)

    filename =  str(time.strftime("%m-%d %H.%M.%S ", time.localtime()) ) + str(curId) + '.py'
    with open(filename, 'w') as f:
        f.write(data)
    f.close()
    print '生成了文件' + filename
    print '题目数为' + str(allTitles) + ',请仔细和对'



def danxuan(every, num):
    list[num] = [1]
    count = 1
    #print len(every.contents[1].contents)
    for i in every.contents[1].contents:
        #choice = i.find('input')
        #print choice
        #if choice.attrs.has_key('jumpto'):
        #    print (str(num) + ' choice '+ str(count + 1) + ' will jumpTo '+ choice.attrs['jumpto'])
        list[num].append([count, 10])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' +  'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def jumpToDanxuan(every, num):
    if every.attrs.has_key("anyjump") and every.attrs['anyjump'] != '0':
        to = int(every.attrs['anyjump'])
        global relationString
        relationString = relationString + '                ' + 'if i == ' + str(num) + \
                         ' and slice[size] != ' + '-3' + ':' + '\n'
        if to == 1:
            to = len(typeList)
        for x in range(num + 1, to):
            if typeList[x] == 3 or typeList[x] == 4:
                relationString = relationString + '                ' + '    list[' + str(x) + '] = [1, [-3, 10]]' + '\n'
            else:
                print str(x) + ' 跳题要注意'
        return
    count = 1
    print len(every.contents[1].contents)
    for i in every.contents[1].contents:
        choice = i.find('input')
        print choice
        if choice.attrs.has_key('jumpto'):
            print (str(num) + ' choice ' + str(count + 1) + ' will jumpTo ' + choice.attrs['jumpto'])
            to = int(choice.attrs['jumpto'])
            global relationString
            relationString = relationString + '                ' + 'if i == ' + str(num) + \
            ' and slice[size] == ' + str(count) + ':' + '\n'
            if to == 1:
                to = len(typeList)
            for x in range(num, to):
                if typeList[x] == 3 or typeList[x] == 4:
                    relationString = relationString + '                ' + '    list[' + str(x) + '] = [1, [-3, 10]]' + '\n'
                else:
                    print str(x) + ' 跳题要注意'
        count = count + 1


def tiankong(every, num):
    list[num] = [1]
    for i in range(5):
        list[num].append(["", 10])
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def duoxuan(every, num):
    list[num] = [10]
    count = 1
    for i in every.contents[1].children:
        list[num].append([count, random.randint(20, 80)])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def zuishao(every, num, min):
    min = int(min)
    list[num] = [12, min]
    count = 1
    for i in every.contents[1].children:
        list[num].append([count, 80])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def zuiduo(every, num, max):
    max = int(max)
    list[num] = [11, max]
    count = 1
    for i in every.contents[1].children:
        list[num].append([count, 80])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def xianzhi(every, num, min, max):
    min = int(min)
    max = int(max)
    list[num] = [13, min, max]
    count = 1
    for i in every.contents[1].children:
        list[num].append([count, 80])
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
    print '#num ' + str(num) + ' row is ' + str(rowR) + ' column is ' + str(column)
    for i in range(rowR):
        temp = []
        for j in range(column):
            temp.append([j + 1, 10])
        list[num].append(temp)
    #print 'list[' + str(num) + '] = ' + str(list[num])
    print 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\'
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = [' + str(list[num][0]) + ', \\' + '\n'
    for i in range(1, len(list[num])):
        print str(list[num][i]) + ', \\'
        listString = listString + '    ' + str(list[num][i]) + ', \\' + '\n'
    print ']'
    listString = listString + '    ' + ']' + '\n'

def table(every, num):
    list[num] = [1]
    count = 1
    for i in every.contents[1].table.tbody.tr.next_sibling.children:
        #print i
        '''
        if count == 1:
            list[num].append([count, 3])
        if count == 2:
            list[num].append([count, 10])
        if count == 3 :
            list[num].append([count, random.randint(20,  23)])
        if count == 4 :
            list[num].append([count, random.randint(35,  40)])
        if count == 5 :
           list[num].append([count, random.randint(15,18)])
        '''
        list[num].append([count, 10])
        count = count + 1
    print 'list[' + str(num) + '] = ' + str(list[num])
    global listString
    listString = listString + '    ' + 'list[' + str(num) + '] = ' + str(list[num]) + '\n'

def plain(s):
    Soup = BeautifulSoup(s.text)
    #i = Soup.fieldset.contents
    num = 1
    for i in Soup.find_all("fieldset"):
        #print i
        for every in i:

            if every.attrs.has_key("type") == False:
                continue
            type = every.attrs["type"]
            type = int(type)
            typeList.append(type)
            if type == 1:
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
            else:
                print '第 ' + str(num) + '题是未知的'


            if every.attrs.has_key("relation"):
                print '#第 ' + str(num) + '题有简单跳题，以下内容放到elif list[i][0] == 1的逻辑下去'
                relation = every.attrs["relation"]
                relationlist = relation.split(",")
                k = relationlist[1].split(";")
                if len(k) == 1:
                    if type == 3 or type == 4:
                        print 'if i == ' + relationlist[0] + ' and slice[size] != ' + relationlist[1] + ':'
                        print '    list[' + str(num) + '] = [1, [-3, 10]]'
                        global relationString
                        relationString = relationString + '                ' + 'if i == ' + relationlist[0] + ' and slice[size] != ' + relationlist[1] + ':' + '\n'
                        relationString = relationString + '                ' + '    list[' + str(num) + '] = [1, [-3, 10]]' + '\n'
                    else:
                        print '第 ' + str(num) + '题有复杂跳题，我还没有研究到'
                else:
                    if type == 3 or type == 4:
                        xstring = ""
                        xstring = 'if i == ' + relationlist[0] + " and ("
                        for x in range(0, len(k)):
                            xstring = xstring + " slice[size] != " + k[x]
                            if x != (len(k) - 1):
                                xstring = xstring + " and "
                            else:
                                xstring = xstring + " ): "
                        print xstring
                        print '    list[' + str(num) + '] = [1, [-3, 10]]'
                        global relationString
                        relationString = relationString + '                ' + xstring + '\n'
                        relationString = relationString + '                ' + '    list[' + str(
                            num) + '] = [1, [-3, 10]]' + '\n'
                    else:
                        print '第 ' + str(num) + '题有复杂跳题，我还没有研究到'



            num = num + 1

    allTitles = num - 1
    print '#一共' + str(num - 1) + '个题数'

    Soup = BeautifulSoup(s.text)
    # i = Soup.fieldset.contents
    num = 1
    for i in Soup.find_all("fieldset"):
        for every in i:
            if every.attrs.has_key("type") == False:
                continue
            type = every.attrs["type"]
            type = int(type)
            if every.attrs.has_key("hasjump"):
                #print '第 ' + str(num) + '题有复杂跳题，做不了'
                jumpToDanxuan(every, num)

            num = num + 1

    return allTitles

if __name__ == '__main__':
    curId = 75259387
    url = "http://www.wjx.cn/m/%s.aspx" % curId
    print len(sys.argv)
    if len(sys.argv) >= 2:
        print sys.argv
        url = 'http://www.wjx.cn/m/' + str(sys.argv[1]) + '.aspx'
    s = requests.get(url, verify=False)
    allTitles = plain(s)
    copy_model(curId, allTitles)

