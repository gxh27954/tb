# encoding: UTF-8
import requests
import time
import random
import sys
import re
import json
import string
import datetime
import csv
#from urllib import quote


ip = []
cap = []
map_ip = {}
ipURL = "http://api.xiequ.cn/VAD/GetIp.aspx?act=get&num=1&time=30&plat=1&re=0&type=2&so=1&ow=1&spl=1&addr=&db=1"
for i in range(0, 200):
    cap.append([0])

QQ = -1



def ips():
    global ip
    ip = getIplist(["通辽"]) #["-"]是全部地区随机的意思

#ips()
appointIP = False
# regression = False


import csv
csv_file_path = 'huigui-120.csv'

def write_data_to_csv(rows):
    # 定义要写入的CSV文件的路径

    # 打开文件以写入模式（如果文件不存在，将创建该文件）
    with open(csv_file_path, mode='w', newline='') as file:
        # 创建一个writer对象
        writer = csv.writer(file)

        header = []
        # 定义要写入的列名（表头）
        for i in range(1, 41):
            header.append(i)
        header = header + ['01', '02', '03', '04','05']
        writer.writerow(header)

        # 定义要写入的数据（每行数据是一个列表）
        # rows = [
        #     ['Data1_1', 'Data1_2', 'Data1_3'],
        #     ['Data2_1', 'Data2_2', 'Data2_3'],
        #     ['Data3_1', 'Data3_2', 'Data3_3'],
        # ]

        # 逐行写入数据
        for row in rows:
            writer.writerow(row)

    print(f"Data has been written to {csv_file_path}")


def regression_judge(data_x, data_y, z=0):
    import pandas as pd
    import statsmodels.api as sm

    # 读取CSV文件
    data = pd.read_csv(csv_file_path)

    # 选择自变量（特征）和因变量（目标）
    X = data[data_x]
    y = data[data_y[0]]

    # 为了使用statsmodels进行回归分析，我们需要添加一个常数项（截距）
    X = sm.add_constant(X)  # 这会在X的前面添加一列全为1的列，作为截距项

    # 进行线性回归分析
    model = sm.OLS(y, X).fit()

    # 打印回归模型的摘要
    # print(model.summary())

    # 从摘要中提取p值
    pvalues = model.pvalues

    # 设置一个显著性水平（例如0.05），以确定哪些变量是显著的
    significance_level = 0.05

    count = 0
    for i, pvalue in enumerate(pvalues):

        if i == 0:
            continue

        if z == 1 and i == 1:
            if pvalue > significance_level:
                count = count + 1
        else:
            if pvalue < significance_level:
                count = count + 1

    return [], count, model.rsquared

    # 找出显著的变量
    significant_variables = pvalues[pvalues < significance_level].index

    # 打印显著的变量
    #print("Significant variables at significance level", significance_level, ":")
    variable_list = []
    for variable in significant_variables:
        if variable != 'const':  # 忽略截距项
            # print(variable)
            variable_list.append(variable)

    return variable_list, len(variable_list), model.rsquared

regressionList = []

def check_tiaojie():
    import pandas as pd
    from statsmodels.formula.api import ols
    df = pd.read_csv(csv_file_path)  # 替换为你的列名
    model = ols('Q("06") ~ Q("05") + Q("07") + Q("05"):Q("07")', data=df).fit()
    interaction_p_value = model.pvalues['Q("05"):Q("07")']
    print(f"交互项A:B的p值为: {interaction_p_value}")
    return interaction_p_value

def regression_analysis(list):
    k = 70
    global regressionList
    regressionList = []
    #[4,'5-14'], [15,'16-20'], [21,22,23,24,25,26,27,28]
    if random.randint(0, 100) < k:

        X = [6,3,7] #-7
        Y = ['8-19']

        X = setGroup(X, list)
        Y = setGroup(Y, list)
        regressionList.append([X, Y])



    if random.randint(0, 100) < 90:
        X = [6,3,7,'8-19'] #-7
        Y = ['20-40']

        X = setGroup(X, list)
        Y = setGroup(Y, list)
        regressionList.append([X, Y])




def regression_all():
    count_all = 0
    r2_limit = 0.3


    x = ['01','02','03']
    y = ['04']
    variable_list, count, r2 = regression_judge(x, y)
    print(variable_list, count, r2)
    if r2 > r2_limit:
        count_all = count_all + count

    x = ['01','02','03','04']
    y = ['05']
    variable_list, count, r2 = regression_judge(x, y)
    print(variable_list, count, r2)
    if r2 > r2_limit:
        count_all = count_all + count


    return count_all


def factor():
    print('fac')
    import pandas as pd
    from factor_analyzer import FactorAnalyzer, Rotator
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    column_list = []
    for i in range(8, 21):
        column_list.append(i)


    # 读取CSV文件并选择特定列
    df = pd.read_csv(csv_file_path, usecols=column_list)  # 替换为你的列名
    print(column_list)
    # 数据标准化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)


    # 确定因子数（基于特征值大于1）
    # 注意：这里我们并不直接使用FactorAnalyzer来确定因子数，而是先计算协方差矩阵的特征值
    cov_matrix = np.cov(scaled_data, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # 找出特征值大于1的因子数
    n_factors = np.sum(eigenvalues > 1)
    print(f"根据特征值大于1确定的因子数: {n_factors}")
    return n_factors

    # # 执行因子分析
    # fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
    # fa.fit(scaled_data)
    #
    # # 输出因子载荷矩阵
    # print("因子载荷矩阵:")
    # print(fa.loadings_)
    #
    # # 输出每个因子的方差解释比例
    # print("每个因子的方差解释比例:")
    # print(fa.get_factor_variance())

list = []
def makeData(n):
    global list
    list = []
    cronbach = []
    cronbachR = []
    cronbachNum = []
    Y_value = []
    answer = {}
    Y_pointer = []

    for i in range(0, 200):
        list.append([1, 0])
        cronbach.append([0])
        cronbachR.append([0])
        cronbachNum.append(0)
        Y_pointer.append(0)
        Y_value.append(None)
        answer[i] = None

    list[1] = [1, [1, 41], [2, 40]]
    list[2] = [1, [1, 11], [2, 30], [3, 40], [4, 25], [5, 9]]
    list[3] = [1, [1, 5], [2, 30], [3, 30], [4, 10]]
    list[4] = [1, [1, 23], [2, 2], [3, 3], [4, 2]]

    list[5] = [1, [1, 5], [2, 5], [3, 20], [4, 20], [5, 11]]
    list[6] = [1, [1, 0], [2, 14], [3, 27], [4, 25], [5, 11], [6, 2]]
    list[7] = [1, [1, 12], [2, 23], [3, 10], [4, 5], [5, 2]]

    list[8] = [1, [1, 2], [2, 8], [3, 22], [4, 35], [5, 15]]
    list[9] = [1, [1, 2], [2, 12], [3, 19], [4, 28], [5, 17]]
    list[10] = [1, [1, 2], [2, 9], [3, 17], [4, 21], [5, 12]]
    list[11] = [1, [1, 30], [2, 15], [3, 28], [4, 27], [5, 20]]
    list[12] = [1, [1, 29], [2, 12], [3, 28], [4, 38], [5, 15]]
    list[13] = [1, [1, 31], [2, 19], [3, 22], [4, 31], [5, 25]]
    list[14] = [1, [1, 39], [2, 33], [3, 17], [4, 40], [5, 20]]

    list[15] = [1, [1, 6], [2, 10], [3, 29], [4, 27], [5, 12]]
    list[16] = [1, [1, 28], [2, 37], [3, 37], [4, 35], [5, 26]]
    list[17] = [1, [1, 11], [2, 22], [3, 25], [4, 16], [5, 12]]

    list[18] = [1, [1, 24], [2, 30], [3, 33], [4, 28], [5, 30]]
    list[19] = [1, [1, 35], [2, 38], [3, 15], [4, 27], [5, 17]]
    list[20] = [1, [1, 2], [2, 5], [3, 22], [4, 34], [5, 14]]
    list[21] = [1, [1, 10], [2, 25], [3, 34], [4, 18], [5, 37]]
    list[22] = [1, [1, 31], [2, 31], [3, 35], [4, 28], [5, 36]]
    list[23] = [1, [1, 40], [2, 36], [3, 33], [4, 28], [5, 10]]
    list[24] = [1, [1, 18], [2, 35], [3, 34], [4, 13], [5, 40]]
    list[25] = [1, [1, 38], [2, 12], [3, 28], [4, 18], [5, 18]]
    list[26] = [1, [1, 2], [2, 10], [3, 20], [4, 30], [5, 14]]
    list[27] = [1, [1, 16], [2, 21], [3, 11], [4, 27], [5, 11]]
    list[28] = [1, [1, 36], [2, 37], [3, 30], [4, 13], [5, 13]]
    list[29] = [1, [1, 14], [2, 17], [3, 30], [4, 11], [5, 11]]
    list[30] = [1, [1, 37], [2, 13], [3, 29], [4, 27], [5, 24]]
    list[31] = [1, [1, 31], [2, 10], [3, 35], [4, 14], [5, 12]]
    list[32] = [1, [1, 40], [2, 26], [3, 20], [4, 36], [5, 32]]
    list[33] = [1, [1, 3], [2, 7], [3, 11], [4, 20], [5, 11]]
    list[34] = [1, [1, 36], [2, 36], [3, 34], [4, 21], [5, 39]]
    list[35] = [1, [1, 38], [2, 16], [3, 31], [4, 15], [5, 33]]
    list[36] = [1, [1, 31], [2, 23], [3, 30], [4, 13], [5, 14]]
    list[37] = [1, [1, 27], [2, 36], [3, 29], [4, 11], [5, 10]]
    list[38] = [1, [1, 24], [2, 39], [3, 22], [4, 22], [5, 16]]
    list[39] = [1, [1, 32], [2, 11], [3, 19], [4, 20], [5, 34]]
    list[40] = [1, [1, 31], [2, 35], [3, 20], [4, 33], [5, 26]]
    ff = 0


    #cronbach[3] = [1, [1, 2], [2, 10], [3, 15], [4, 10], [5, 5]]
    #cronbach[18] = [1, [1, 2], [2, 5], [3, 10], [4, 15], [5, 7]]

    cronbachTemps = [[8,'9-100']
                     ]



    if random.randint(1, 100) <= 180:
        ff = 1
        cronbachTemps = [[15, 16, 17], [9, 12, 13], [8, 11, 19], [10, 14, 18], [20, '21-25'], [26, '27-32'], [33, '34-40']]





    # if random.randint(1, 100) <= 50:
    #     list[1] = [1, [1, 30], [2, 30]]
    #     list[2] = [1, [1, 42], [2, 40], [3, 45], [4, 43], [5, 42]]
    #
    #     list[3] = [1, [1, 0], [2, 17], [3, 18], [4, 14], [5, 15]]
    #     list[4] = [1, [1, 2], [2, 16], [3, 17], [4, 24], [5, 17], [6, 12]]
    #     list[5] = [1, [1, 11], [2, 10], [3, 12], [4, 15], [5, 13], [6, 16], [7, 15], [8, 18]]
    #
    #     list[7] = [1, [1, 12], [2, 13], [3, 13], [4, 18]]
    #
    #     list[10] = [1, [1, 21], [2, 29]]
    # k = random.randint(1, 100)
    # if ff == 0:
    #     if k <= 20:
    #         list[1] = [1, [1, 10]]
    #         list[2] = [1, [3, 10], [4, 10]]
    #         list[3] = [1, [4, 10], [5, 10]]
    #         list[12] = [1, [1, 2], [2, 5], [3, 10], [4, 11], [5, 35], [6, 1122], [7, 1110]]
    #
    #     elif k <= 40:
    #         list[1] = [1, [2, 20]]
    #         list[2] = [1, [1, 10], [2, 10], [5, 10], [6, 10], [7, 10]]
    #         list[3] = [1, [1, 10], [2, 10]]
    #         list[12] = [1, [1, 1112], [2, 1115], [3, 10], [4, 11], [5, 35], [6, 22], [7, 10]]

    count = random.randint(0, 1)


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



    regression_analysis(list)

    choose = []
    for xxx in range(2):

        for rr in range(0, 200):
            Y_pointer[rr] = 0
        data = ''
        for i in range(1, n + 1):
            # if xxx == 0 and i in [1, 2, 3]:
            #     continue
            # print list[i]
            data = data + str(i) + '$'  # 序号

            dateTemp = ''
            yyy, zzz = check_i(i, answer, Y_value)
            if list[i][0] != 20 and answer.get(i, None) != None and yyy == False:
                dateTemp = dateTemp + str(answer[i])
            else:
                if list[i][0] == 10:  # 多选
                    length = len(list[i])
                    slice = []
                    while len(slice) == 0:
                        for j in range(1, length):
                            rand = random.randint(0, 100)
                            if rand <= list[i][j][1]:
                                slice.append(list[i][j][0])
                    random.shuffle(slice)
                    _ansString = ''

                    for j in range(0, len(slice)):
                        _ansString = _ansString + str(slice[j])
                        choose.append(slice[j])
                        if j < len(slice) - 1:
                            _ansString = _ansString + '|'
                    answer[i] = _ansString
                    cronbachNum[i] = _ansString
                    dateTemp = dateTemp + _ansString

                elif list[i][0] == 11:  # 多选,最多选几项
                    slice = []
                    length = len(list[i])

                    while len(slice) == 0 or len(slice) > list[i][1]:
                        slice = []
                        for j in range(2, length):
                            rand = random.randint(0, 100)
                            if rand <= list[i][j][1]:
                                slice.append(list[i][j][0])

                    random.shuffle(slice)
                    _ansString = ''
                    for j in range(0, len(slice)):
                        _ansString = _ansString + str(slice[j])
                        if j < len(slice) - 1:
                            _ansString = _ansString + '|'
                    answer[i] = _ansString
                    dateTemp = dateTemp + _ansString

                elif list[i][0] == 12:  # 多选,最少选几项
                    slice = []
                    length = len(list[i])

                    while len(slice) == 0 or len(slice) < list[i][1]:
                        slice = []
                        for j in range(2, length):
                            rand = random.randint(0, 100)
                            if rand <= list[i][j][1]:
                                slice.append(list[i][j][0])
                    random.shuffle(slice)
                    _ansString = ''
                    for j in range(0, len(slice)):
                        _ansString = _ansString + str(slice[j])
                        if j < len(slice) - 1:
                            _ansString = _ansString + '|'
                    answer[i] = _ansString
                    dateTemp = dateTemp + _ansString

                elif list[i][0] == 13:  # 最少选几项，最多选几项
                    slice = []
                    length = len(list[i])

                    while len(slice) == 0 or len(slice) < list[i][1] or len(slice) > list[i][2]:
                        slice = []
                        for j in range(3, length):
                            rand = random.randint(0, 100)
                            if rand <= list[i][j][1]:
                                slice.append(list[i][j][0])
                    random.shuffle(slice)
                    _ansString = ''
                    for j in range(0, len(slice)):
                        _ansString = _ansString + str(slice[j])
                        if j < len(slice) - 1:
                            _ansString = _ansString + '|'
                    answer[i] = _ansString
                    dateTemp = dateTemp + _ansString

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
                    judge, pos = check_i(i, answer, Y_value)
                    if judge:
                        # print Y_value
                        # print Y_pointer
                        d = Y_value[pos][Y_pointer[pos]]
                        dateTemp = dateTemp + str(d)
                        cronbachNum[i] = d
                        answer[i] = d
                        Y_pointer[pos] = Y_pointer[pos] + 1
                        if i == 2 and slice[size] == 1:
                            list[4] = [1, [1, 10]]

                    elif cronbach[i][0] == 2:
                        size = cronbachNum[cronbach[i][1]]
                        a = random.randint(0, 100)
                        x = 0
                        y = 100
                        if 1 <= i <= 22:
                            x = 0
                            y = 100
                        if a < x:
                            b = max(1, size - 2)
                        elif a < 30:
                            b = max(1, size - 1)
                        elif a < 70:
                            b = size
                        elif a < y:
                            b = min(size + 1, len(list[cronbach[i][1]]) - 1)
                        else:
                            b = min(size + 2, len(list[cronbach[i][1]]) - 1)

                        if cronbachR[i][0] == 1:
                            dateTemp = dateTemp + str(cronbachR[i][1] - b + 1)
                            answer[i] = cronbachR[i][1] - b + 1
                            cronbachNum[i] = cronbachR[i][1] - b + 1
                        else:
                            dateTemp = dateTemp + str(b)
                            answer[i] = b
                            cronbachNum[i] = b

                    else:
                        # 以下设置比例
                        length = len(list[i])
                        slice = []
                        for j in range(1, length):
                            #print(list[i])
                            for k in range(0, list[i][j][1]):
                                slice.append(list[i][j][0])
                        # 以上设置比例
                        length = len(slice)
                        if cap[i][0] == 0:
                            size = random.randint(0, length - 1)
                            dateTemp = dateTemp + str(slice[size])
                            cronbachNum[i] = slice[size]
                            answer[i] = slice[size]
                            if i == 3 and slice[size] <= 2:
                                list[5] = [1, [1, 16], [2, 40], [3, 34], [4, 0], [5, 0]]
                                list[6] = [1, [1, 15], [2, 24], [3, 27], [4, 15], [5, 0], [6, 0]]






























                        else:
                            while True:
                                size = random.randint(0, length - 1)
                                pos = 0
                                for tr in range(1, len(list[i])):
                                    if list[i][tr][0] == slice[size]:
                                        pos = tr
                                        break
                                #global cap
                                if cap[i][pos][1] > 0:
                                    dateTemp = dateTemp + str(slice[size])
                                    cronbachNum[i] = slice[size]
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
                        #print(f, size)



                        # if ff == 0 and i == 3 and size >= 4:
                        #
                        #     list[14] = [1, [1, 0], [2, 40]]
                        #     list[15] = [1, [random.randint(18, 26), 10]]
                        #
                        #
                        #     list[16] = [1, [1, 12], [2, 25], [3, 0], [4, 0], [5, 0]]
                        #
                        # if ff == 0 and i == 3 and size <= 2:
                        #     list[14] = [1, [1, 10], [2, 0]]
                        #     list[15] = [1, [random.randint(27, 42), 10]]
                        #     list[16] = [1, [1, 0], [2, 0], [3, 0], [4, 10], [5, 10]]



                        for j in range(1, len(list[i])):

                            judge, pos = check_i(str(i) + '-' + str(j), answer, Y_value)
                            if judge:
                                d = Y_value[pos][Y_pointer[pos]]
                                dateTemp = dateTemp + str(j) + '!' + str(d)
                                answer[str(i) + '-' + str(j)] = d
                                Y_pointer[pos] = Y_pointer[pos] + 1
                            elif answer.get(str(i) + '-' + str(j), None) != None:
                                # print i, j
                                if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                                    dateTemp = dateTemp + str(j) + '!' + str(
                                        cronbachR[i][1] - answer[str(i) + '-' + str(j)] + 1)
                                else:
                                    dateTemp = dateTemp + str(j) + '!' + str(answer[str(i) + '-' + str(j)])

                            else:
                                a = random.randint(0, 100)
                                if a < 20:
                                    b = max(1, size - 1)
                                elif a < 80:
                                    b = size
                                else:
                                    b = min(size + 1, len(cronbach[i]) - 1)

                                if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                                    dateTemp = dateTemp + str(j) + '!' + str(cronbachR[i][1] - b + 1)
                                else:
                                    dateTemp = dateTemp + str(j) + '!' + str(b)
                                answer[str(i) + '-' + str(j)] = str(b)
                            if j != len(list[i]) - 1:
                                dateTemp = dateTemp + ','
                    elif cronbach[i][0] == 2:
                        size = cronbachNum[cronbach[i][1]]
                        size = random.choice([size, max(1, size - 1), min(len(cronbach[cronbach[i][1]]) - 1, size + 1)])
                        for j in range(1, len(list[i])):
                            judge, pos = check_i(str(i) + '-' + str(j), answer, Y_value)
                            if judge:
                                d = Y_value[pos][Y_pointer[pos]]
                                dateTemp = dateTemp + str(j) + '!' + str(d)
                                answer[str(i) + '-' + str(j)] = d
                                Y_pointer[pos] = Y_pointer[pos] + 1
                            elif answer.get(str(i) + '-' + str(j), None) != None:
                                if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                                    dateTemp = dateTemp + str(j) + '!' + str(
                                        cronbachR[i][1] - answer[str(i) + '-' + str(j)] + 1)
                                else:
                                    dateTemp = dateTemp + str(j) + '!' + str(answer[str(i) + '-' + str(j)])
                            else:
                                a = random.randint(0, 100)
                                if a < 20:
                                    b = max(1, size - 1)
                                elif a < 80:
                                    b = size
                                else:
                                    b = min(size + 1, len(cronbach[cronbach[i][1]]) - 1)

                                if cronbachR[i][0] == 1 and j in cronbachR[i][2]:
                                    dateTemp = dateTemp + str(j) + '!' + str(cronbachR[i][1] - b + 1)
                                else:
                                    dateTemp = dateTemp + str(j) + '!' + str(b)
                                answer[str(i) + '-' + str(j)] = str(b)
                            if j != len(list[i]) - 1:
                                dateTemp = dateTemp + ','
                    else:
                        for j in range(1, len(list[i])):
                            judge, pos = check_i(str(i) + '-' + str(j), answer, Y_value)
                            # print judge
                            if judge:
                                d = Y_value[pos][Y_pointer[pos]]
                                dateTemp = dateTemp + str(j) + '!' + str(d)
                                answer[str(i) + '-' + str(j)] = d
                                Y_pointer[pos] = Y_pointer[pos] + 1

                            elif answer.get(str(i) + '-' + str(j), None) != None:
                                dateTemp = dateTemp + str(j) + '!' + str(answer[str(i) + '-' + str(j)])
                            else:
                                slice = []
                                for k in range(len(list[i][j])):
                                    for x in range(0, list[i][j][k][1]):
                                        slice.append(list[i][j][k][0])
                                # print slice
                                b = slice[random.randint(0, len(slice) - 1)]
                                dateTemp = dateTemp + str(j) + '!' + str(b)
                                answer[str(i) + '-' + str(j)] = str(b)
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
                    _ansString = ''
                    for j in range(0, len(slice)):
                        _ansString = _ansString + str(slice[j])
                        if j < len(slice) - 1:
                            _ansString = _ansString + '|'
                    answer[i] = _ansString
                    dateTemp = dateTemp + _ansString
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
            #print(str1)
            data = data + dateTemp  # 答案

            if i < n:
                data = data + '}'  # 分隔符


    '''
    print '%s\t' % cronbachNum[3]
    print '%s\t' % str((int(answer["8-1"]) + int(answer["8-2"]) + int(answer["8-3"]) + int(answer["8-4"])) / 4.0),
    print '%s\t' % str((int(answer["9-1"]) + int(answer["9-2"])) / 2.0),
    print '%s\t' % str((int(answer["10-1"]) + int(answer["10-2"]) + int(answer["10-3"]) + int(answer["10-4"] + int(answer["10-5"])) / 5.0),
    print '%s\t' % str((int(answer["11-1"]) + int(answer["11-2"]) + int(answer["11-3"])) / 3.0),
    print '%s\t' % str((int(answer["12-1"]) + int(answer["12-2"]) + int(answer["12-3"])) / 3.0),
    print '%s\t' % str((int(answer["14-1"]) + int(answer["14-2"]) + int(answer["14-3"]) + (int(answer["14-4"]) + int(answer["14-5"]) + int(answer["14-6"]) + cronbachNum[13]) / 7.0),
    print '%s\t' % str((int(answer["18-1"]) + int(answer["18-2"]) + int(answer["18-3"]) + int(answer["18-4"])) / 4.0),
    '''

    #print '%s\t' % str((int(answer["19-1"]) + int(answer["19-2"])) / 2.0),

    #print ''
    '''
    s1 = 1.0
    for rt in range(1, 5):
        print '%s\t' % int(answer["8-%s" % rt]),
        s1 = s1 + int(answer["8-%s" % rt])


    s2 = 1.0
    for rt in range(1, 4):
        print '%s\t' % int(answer["9-%s" % rt]),
        s2 = s2 + int(answer["9-%s" % rt])


    s3 = 1.0
    for rt in range(1, 5):
        print '%s\t' % int(answer["10-%s" % rt]),
        s3 = s3 + int(answer["10-%s" % rt])


    s4 = 1.0
    for rt in range(1, 6):
        print '%s\t' % int(answer["11-%s" % rt]),
        s4 = s4 + int(answer["11-%s" % rt])

    '''

    list1 = []

    for i in range(1, 41):
        #print(i, list[i])
        if list[i][0] == 20:
            for j in range(1, len(list[i])):
                #print('%s\t' % int(answer["%s-%s" % (i, j)]))
                list1.append(int(answer["%s-%s" % (i, j)]))
        else:
            #print('%s\t' % (cronbachNum[i])),
            list1.append(answer[i])

    #print(len(list1))

    # for i in range(3, 13):
    #     s = 0
    #     k = 0
    #     for j in range(1, len(list[i])):
    #         s = s + int(answer["%s-%s" % (i, j)])
    #         k = k + 1
    #         # if i == 13:
    #         #     print(int(answer["%s-%s" % (i, j)]))
    #     #print(s/k),
    #     # if i == 13:
    #     #     print(s, k)
    #     list1.append(s/k)

    #[4,'5-14'], [15,'16-20'], [21,22,23,24,25,26,27,28]
    #[6,7,8], [11,12,13], [4,9,10], [16,'17-19'], [20,21,22,23,24],[25,26,27,28,29]

    #[1,'2-22'], [23,'24-49'], [50,'51-71'], [72,'73-87']

    #[[12,13,14], [15,16,17], [18,19,20], [21,22,23], [24,25,26], [27,28,29], [30,31,32], [33,34,35],
    #                 [36,37,38,39,40],[41,'42-44'],[45,'46-53'],[54,'55-78']]

    #[[5,6,7], [8,9,10,11], [12,13,14], [15,16,17], [22,23,24], [25,26,27]]
    # [[13,'14-25'], [26,27,28], [29,30,31], [32,33,34,35], [36,'37-41']]

    s = 0.0
    k = 0
    for rt in range(6, 7):
        #print '%s\t' % int(answer["11-%s" % rt]),
        s = s + cronbachNum[rt]
        k = k + 1
    list1.append(s*1.0 / k)

    s = 0.0
    k = 0
    for rt in range(3, 4):
        #print '%s\t' % int(answer["11-%s" % rt]),
        s = s + cronbachNum[rt]
        k = k + 1
    list1.append(s*1.0 / k)

    s = 0.0
    k = 0
    for rt in range(7, 8):
        #print '%s\t' % int(answer["11-%s" % rt]),
        s = s + cronbachNum[rt]
        k = k + 1
    list1.append(s*1.0 / k)


    s = 0.0
    k = 0
    for rt in range(8, 20):
        #print '%s\t' % int(answer["11-%s" % rt]),
        s = s + cronbachNum[rt]
        k = k + 1
    #print(s*1.0 / k)
    list1.append(s*1.0 / k)


    s = 0.0
    k = 0
    for rt in range(20, 41):
        #print '%s\t' % int(answer["11-%s" % rt]),
        s = s + cronbachNum[rt]
        k = k + 1
    list1.append(s*1.0 / k)



    # print answer
    #print(data)
    return list1



def setGroup(X, list):
    a = []
    for x in X:
        if type(x) == type(10):
            if list[x][0] == 1:
                a.append(x)
            if list[x][0] == 20:
                for j in range(1, len(list[x])):
                    a.append(str(x) + '-' + str(j))
        if type(x) == type(10.0):
            a.append(str(str(x).split(".")[0]) + '-' + str(str(x).split(".")[1]))
        if type(x) == type('10-20'):
            if x.find('.') == -1:
                c = x.split('-')
                # print c
                aa = int(c[0])
                bb = int(c[1])
                for j in range(aa, bb + 1):
                    if list[j][0] == 1:
                        a.append(j)
                    if list[j][0] == 20:
                        for k in range(1, len(list[j])):
                            a.append(str(j) + '-' + str(k))
                    # a.append(j)
            else:
                c = x.split('-')
                aa = str(c[0])
                bb = str(c[1])
                #print int(aa.split(".")[1])
                #print int(bb.split(".")[1])
                for j in range(int(aa.split(".")[1]), int(bb.split(".")[1]) + 1):
                    a.append(aa.split(".")[0] + '-' + str(j))
    return a


def check_i(i, answer, Y_value ):
    #print Y_value
    length = 0
    for data in regressionList:
        if i in data[1]:
            if Y_value[length] != None:
                return True, length
            is_ok = True
            for x in data[0]:
                if answer.get(x, None) == None:
                    is_ok = False
            if is_ok:
                data_list = do_regression(data[0], data[1], answer)
                Y_value[length] = data_list
                return True, length
            else:
                return False, -1
        length = length + 1
    return False, -1


def do_regression(data_x, data_y, answer):
    #print(data_x, data_y, answer)

    s = 0.0


    #7,10,13,15,16
    #list[2] = [1, [1, 32], [2, 32], [3, 32], [4, 32]]
    #list[4] = [1, [1, 17], [2, 9]]
    #list[5] = [1, [1, 30], [2, 13], [3, 13], [4, 6]]
    global list

    if 1300 in data_y:
        s1 = 0.0
        k = 0
        for rt in range(6, 7):
            #print '%s\t' % int(answer["11-%s" % rt]),
            s1 = s1 + answer[rt]
            k = k + 1
        s1 = s1*1.0 / k
        #list1.append(s*1.0 / k)
        #倒U
        s = 1.0 * s1 - 0.3 * s1 * s1 + 3
        print(s)

    else:

        for data in data_x:
            len1 = 5#len(list[data_y[0]]) - 1
            len2 = len(list[data]) - 1
            # if data == 3:
            #     len2 = 4
            # if data == 6:
            #     len2 = 6
            s = s + (1.0) / (len(data_x))  * (len1*1.0/len2) * float(answer[data])
        #s = s + (1.0) / (len(data_x)) * float(answer[data])


    count = len(data_y)
    s = s * count
    bb = []

    for x in range(0, count):
        f = s / (count - x)
        if f - int(s / (count - x)) >= 0.2:
            f = f + 1

        f = int(f)
        f = max(1, f)
        f = min(5, f)
        bb.append(f)
        s = s - f


    random.shuffle(bb)

    # if 31 in data_y:
    #     for rt in range(len(bb)):
    #         bb[rt] = 8 - bb[rt]

    #bb[0] = 3 - bb[0]

    # print('自变量', data_x)
    # print('因变量', data_y)
    # print(bb)
    return bb











def get_people():
    z = ['赵', '钱', '孙', '李', '周', '吴', '王', '郭', '牛', '黄', '范', '刘', '陈', '方', '张', '胡', '宋', '鹿', '白', '刘', '宁']
    zx = ['一', '桐', '涵', '轩', '雨', '伟', '微', '思', '旭', '百', '彦', '杰', '铭', '芸', '安', '平', '楠', '冰', '琛', '优']
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
    except Exception as e:
        print(str(Exception))
    finally:
        f.close()
    if jqParamJS == "":
        return 'abc'
    ctx = execjs.compile(jqParamJS)
    return ctx.call("abc", needTime, curid, rndnum)


def updateToDB():
    import MySQLdb
    db = MySQLdb.connect("106.55.33.220", "root", "isd@cloud123", "test", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        sql = "UPDATE need SET nc_token = '%s' WHERE id = 1" % random.randint(1, 30000000)
        cursor.execute(sql)
        db.commit()
        return
    except Exception as e:
        print(str(Exception))

        return
    finally:
        db.close()


def getFromDB():
    import MySQLdb
    db = MySQLdb.connect("172.16.0.7", "root", "isd@cloud", "test", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    t = datetime.datetime.now() - datetime.timedelta(minutes=9)
    t = str(t.strftime("%Y-%m-%d %H:%M:%S"))
    sql = "SELECT * FROM salary where creat_time >= '%s' and is_use = 0 limit 1" % t
    try:
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
            print("id=%s,nc_token=%s,nc_sig=%s,nc_csessionid=%s,creat_time=%s,is_use=%s" % \
                  (id, nc_token, nc_sig, nc_csessionid, creat_time, is_use))

        sql = "UPDATE salary SET is_use = 1 WHERE id = %s" % (id)
        cursor.execute(sql)
        db.commit()
        return nc_token, nc_sig, nc_csessionid
    except Exception as e:
        return '1', '2', '3'
    finally:
        db.close()


def captcha(proxy):
    try:
        updateToDB()
    except Exception as e:
        print("")
    try:
        nc_token, nc_sig, nc_csessionid = getFromDB()
        if len(nc_token) >= 5 or len(nc_sig) >= 5 or len(nc_csessionid) >= 5:
            return nc_token, nc_sig, nc_csessionid
    except Exception as e:
        print("")


    print('已经告诉生产者去生成验证码了，请等待')
    return '1', '2', '3'


def getIp():
    ip = "0:0"
    if ip != "0:0":

        return ip
    url = ipURL
    try:
        s = requests.get(url)
        return s.text
    except Exception as e:

        return "0:0"


def getAll(curid, needTime, ip_proxy):
    if str(curid).isdigit():
        url = 'https://www.wjx.cn/m/' + str(curid) + '.aspx'
    else:
        url = 'https://www.wjx.cn/vm/' + str(curid) + '.aspx'

    head = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'www.wjx.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    ipp = "0:0"
    if appointIP:
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
        proxies = {"http": "http://756605998:rwb50msr@%s" % ip_proxy,
                   "https": "https://756605998:rwb50msr@%s" % ip_proxy}

        if ip_proxy == "0:0":
            proxies = {
                "http": "http://81.68.221.80:26881",
                "https": "http://81.68.221.80:26881",
            }

        s = requests.get(url, headers=head, timeout=3, proxies=proxies)
        Verify = s.text.find("useAliVerify =1")
        if str(curid).isdigit():
            Verify = 0
        else:
            x1 = s.text.find("activityId =")
            x2 = s.text[x1:].find(";")
            curId2 = s.text[x1 + 12:x1 + x2]
        if Verify != -1:
            nc_token, nc_sig, nc_csessionid = captcha(ip_proxy)
            # s = requests.get(url, headers=head, proxies=proxies, timeout=3)

        cookie = s.cookies
        cookies_dict = requests.utils.dict_from_cookiejar(cookie)
        c = json2String(cookies_dict)
        rndnum = re.search("rndnum=\".+\";", s.text).group(0)[8:-2]
        jqnonce = re.search("jqnonce=\".+\";", s.text).group(0)[9:-2]

        ktimes = random.randint(110, 428) + 2
        from urllib import quote
        jqsign = str(quote(getJqsign(jqnonce, ktimes)))
        ran_str1 = ''.join(random.sample(string.ascii_letters + string.digits, 18))
        ran_str2 = ''.join(random.sample(string.ascii_letters + string.digits, 18))
        u_asec = "099%23" + ''.join(random.sample(string.ascii_letters + string.digits, 18))
        c = c + ";u_asec=%s;CNZZDATA4478442=cnzz_eid=%d-%d-&ntime=%d;ssxmod_itna=%s;ssxmod_ktimd=%s" % (
            u_asec, random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), ran_str2, str(ktimes))

        if str(curid).isdigit():
            jqParam = getJqParam(needTime, curid, rndnum)
        else:
            jqParam = getJqParam(needTime, curId2, rndnum)

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
            "jqParam": jqParam,
            "ip": ipp
        }

        if random.randint(1, 10) <= 5:
            params["source"] = "微信"

        if Verify != -1:
            params["nc_token"] = nc_token
            params["nc_sig"] = nc_sig,
            params["nc_csessionid"] = nc_csessionid,
            params["nc_scene"] = "ic_activity",
    except Exception as e:

        params, c = False, False
    return params, c


def sem():
    from semopy import Model
    import pandas as pd
    import semopy
    import statsmodels.api as sm

    # 假设我们有一个数据集
    # 数据集包含自变量 X1, X2, X3 和因变量 Y
    data = pd.read_csv(csv_file_path)
    df = pd.DataFrame(data)
    #[1,2,3,5], [6,8,9], [11,13,14,15], [16,17,18],[22,23,25],[26,27,28,29],[31,32,33],[36,37,39,40]
    #[[12,13,14], [15,16,17], [18,19,20], [21,22,23], [24,25,26], [27,28,29], [30,31,32], [33,34,35],
    #                 [36,37,38,39,40],[41,'42-44'],[45,'46-53'],[54,'55-78']]
    desc = '''  
    # 定义测量模型  
    # 假设有三个潜变量Y1, Y2, Y3，分别由多个观测变量x1-x9表示（这里只是示例，具体根据你的数据）  
    x1 =~ 12 + 13 + 14
    x2 =~ 15 + 16 + 17
    x3 =~ 18 + 19 + 20
    x4 =~ 21 + 22 + 23 
    x5 =~ 24 + 25 + 26
    x6 =~ 27 + 28 + 29
    x7 =~ 30 + 31 + 32
    x8 =~ 33 + 34 + 35
    x9 =~ 36 + 37 + 38 + 39 + 40

    # 定义结构模型  
    # 假设Y1影响Y2，Y2影响Y3（这里只是示例，具体根据你的研究假设）  

    x8 ~ x1 + x2 + x3 + x4 + x5 + x6 + x7
    x9 ~ x4 + x7

    '''

    # 创建模型对象
    model = Model(desc)

    # 拟合模型到数据
    # 注意：这里的数据应该是经过适当预处理的，比如处理缺失值、标准化等
    # 还需要确保数据集中的变量名与模型描述中的观测变量名相匹配
    model.fit(data)

    # 输出模型结果
    # 可以打印模型的参数估计、标准误、t值、p值等信息
    # 还可以评估模型的拟合度，比如比较拟合指数（CFI）、近似误差均方根（RMSEA）等
    rs = model.inspect()
    print(rs[:9])


    #print(rs.pvalues)
    #print(model.inspect())

    s = 0
    max_k = -1
    max_pos = -1
    for i in range(0, 9):
        if rs.values[i][6] < 0.05:
            s = s + 1
            print(i, rs.values[i][0],rs.values[i][2],'<',rs.values[i][6])
        else:
            # if i == 7:
            #     s = s + 1
            print(i, rs.values[i][0], rs.values[i][2], '>',rs.values[i][6])

        if rs.values[i][3] > max_k:
            max_k = rs.values[i][3]
            max_pos = i

    max_pos_2 = -1
    max_k = -1
    for i in range(0, 9):
        if i == max_pos:
            continue
        if rs.values[i][3] > max_k:
            max_k = rs.values[i][3]
            max_pos_2 = i

    print("max_pos: ", max_pos, max_pos_2)



    stats = semopy.calc_stats(model)
    print(stats.T)
    print("sem count: ", s)
    return s


#if __name__ == '__main__':
if __name__ == '__main__':
    curId = 'PN613JP'#'O8ZrR3p'

    # sem()
    # time.sleep(10)

    time1 = 120
    time2 = 200
    url = "https://www.wjx.cn/joinnew/processjq.ashx"

    doNumber = 500  # 刷几次
    titleNumber = 40  # 多少个题目


    for i in range(1, titleNumber + 1):
        print('%s\t' % i),

    while True:
        data_list = []
        for i in range(0, 200):
            d = makeData(titleNumber)
            data_list.append(d)
        print(len(data_list[0]))
        write_data_to_csv(data_list)

        if regression_all() >= 7 and factor() >= 4:

            break
    #
    # i = 0
    # data = ''
    # while i < doNumber:
    #     ip_proxy = getIp()
    #
    #     print i
    #     needTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime((time.time() - random.randint(time1, time2))))
    #     params, Cookie = getAll(curId, needTime, ip_proxy)
    #     if params == False:
    #         print 'a is not ok, restart!!!'
    #         time.sleep(1)
    #         continue
    #     print 'start -- ' + str(i + 1) + ' -- '
    #     print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     suc, data = wjx(titleNumber, url, Cookie, params, data, ip_proxy)
    #     print 'end --' + str(i + 1) + ' -- '
    #     if suc == False:
    #         print 'is not ok, restart!!!'
    #         time.sleep(1)
    #     else:
    #         i = i + 1
    #         time.sleep(random.randint(2, 16))
