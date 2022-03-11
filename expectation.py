from codecs import open
from csv import reader
from math import log2
from copy import deepcopy
from tqdm import tqdm

# 读取干员数据
f = reader(open('operator.csv','r',encoding='utf-8'))
operators = dict()
for tmp in f:
    if tmp[1] == '稀有度':
        continue
    name = tmp[0]
    rare = int(tmp[1])
    zheny = set(tmp[2].split())
    job = set(tmp[3].split("-"))
    type = set(tmp[4].split())
    drawer = tmp[5]
    operators[name] = (name, rare, zheny, job, type, drawer)

#如果猜测x，答案是y，计算得到的反馈
def guess(x, y):
    ans = []
    if y[1] < x[1]:
        ans.append('2')
    elif y[1] > x[1]:
        ans.append('3')
    else:
        ans.append('1')
    for i in range(2, 5):
        if y[i] == x[i]:
            ans.append('1')
        elif y[i] & x[i] > set({}):
            ans.append('2')
        else:
            ans.append('0')
    if y[5] == x[5]:
        ans.append('1')
    else:
        ans.append('0')
    return ''.join(ans)

#枚举答案，计算该答案下，按照信息熵进行猜测需要的步数
records = []
for _, opt in tqdm(enumerate(operators.values())):
    topt = deepcopy(operators)
    times = 0 # 记录步数
    while 1:
        times += 1
        tot = len(topt.values())
        results = []
        #枚举所有干员，计算猜测他能够得到的信息熵
        for x in operators.values():
            dtb = dict()
            for y in topt.values():  #枚举剩余满足条件的干员，进行分类
                ret = guess(x, y)
                if ret in dtb.keys():
                    dtb[ret] += 1
                else:
                    dtb[ret] = 1
            entro = 0
            for i in dtb.values():  #根据概率分布计算信息熵
                p = i / tot
                entro -= p * log2(p)
            results.append((entro, int(x[0] in topt), x[0]))
        results.sort(reverse=True)
        name = results[0][2] #选择信息熵最大的进行猜测
        feedback = guess(operators[name], opt) #计算反馈
        if feedback == "11111": #猜对的情况
            records.append((times, opt[0]))
            break
        to_be_del = [] #删去不符合已知条件的干员
        for i in topt.keys():
            if guess(operators[name], topt[i]) != feedback:
                to_be_del.append(i)
        for i in to_be_del:
            del topt[i]

#计算均值并输出
records.sort()
s = 0
i = 0
for x in records:
    if x[1] == "阿米娅(近卫)":
        name = "阿米娅(近卫)  "
    else:
        name = x[1] + ' ' * (14 - 2 * len(x[1]))
    print(f"{name}{x[0]},", end = "")
    i += 1
    s += x[0]
    if i % 8 == 0:
        print()
print()
print(f"平均需要{s/len(records):.4f}次猜测")
s = input()