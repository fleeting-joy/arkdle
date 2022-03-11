from codecs import open
from csv import reader
from math import log2
from copy import deepcopy

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

while 1:
    print()
    print()
    print("新游戏开始。")
    topt = deepcopy(operators)
    times = 0 # 记录已经猜的次数
    while 1:
        times += 1
        tot = len(topt.values())
        print()
        print()
        print(f"当前剩余{tot}位干员符合已有条件")
        results = []
        #枚举所有干员，计算猜测他能够得到的信息熵
        for x in operators.values():
            dtb = dict()
            for y in topt.values(): #枚举剩余满足条件的干员，进行分类
                ret = guess(x, y)
                if ret in dtb.keys():
                    dtb[ret] += 1
                else:
                    dtb[ret] = 1
            entro = 0
            for i in dtb.values(): #根据概率分布计算信息熵
                p = i / tot
                entro -= p * log2(p)
            results.append((entro, int(x[0] in topt), x[0]))
        results.sort(reverse=True) #排序输出结果
        print(f"下面是程序计算得到期望信息量前10的干员，干员名后的第一个数字表示")
        print(f"其能获得的期望信息量，第二个数字表示其是否符合已有条件，1为符合，0为不符合")
        for i in range(10):
            if results[i][2] == "阿米娅(近卫)":
                name = "阿米娅(近卫)  "
            elif results[i][2] in ["Castle-3", "Lancet-2", "THRM-EX", "W", "12F"]:
                name = results[i][2] + ' ' * (14 - len(results[i][2]))
            else:
                name = results[i][2] + ' ' * (14 - 2 * len(results[i][2]))
            print(f"{name} {results[i][0]:.4f} {results[i][1]}")
        name = input("请输入你这次猜测的干员(阿米娅(近卫)请使用英文括号)：")
        while name not in operators.keys():
            print("该干员不存在")
            name = input("请输入你这次猜测的干员(阿米娅(近卫)请使用英文括号)：")
        print("请按照下面的格式输入这次猜测得到的反馈：")
        print("你应该输入一个由五个数字组成的字符串，中间没有空格，依次代表稀有度、阵营、职业、种族、画师的反馈。")
        print("1表示完全正确，0表示完全错误，对于稀有度，2表示干员的实际稀有度更低，3表示干员的实际稀有度更高")
        print("对于其他属性，2表示部分正确，这一项不做输入的正确性检查（懒）")
        feedback = input()
        if feedback == "11111":
            print(f"恭喜你猜对了，总共使用{times}次")
            break
        #删除不符合已知要求的干员
        to_be_del = []
        for i in topt.keys():
            if guess(operators[name], topt[i]) != feedback:
                to_be_del.append(i)
        for i in to_be_del:
            del topt[i]
        ttot = len(topt)
        print(f"该次猜测获得的实际信息量为{-log2(ttot/tot):.4f}")
