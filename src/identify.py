import pandas as pd
import numpy as np
import datetime as dt
import load







def case_cor(t,cor,inter,c_pattern, T_threshold,n1_threshold,v1_threshold,n2_threshold):
    # 指標1.1
    # T = dt.timedelta(days=0, seconds=1, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    T = T_threshold
    # 結合パターン
    pattern = {}
    ans1 = set()
    t1 =t[0][0]
    l = len(t)
    for i in range(1,l):
        t2 = t[i][0]
        if t2 - t1 < T:
            if (t[i-1][1],t[i][1]) in pattern:
                pattern [(t[i-1][1],t[i][1])] += 1
                if (pattern [(t[i-1][1],t[i][1])] > n1_threshold and t[i-1][1][0] != t[i][1][0]):
                    ans1.add((t[i-1][1],t[i][1]))
            else:
                pattern [(t[i-1][1],t[i][1])] = 1
        t1 = t2

    case1 = t[0][3]
    task1 = t[0][1]
    l = len(t)
    for i in range(1,l):
        case2 = t[i][3]
        task2 = t[i][1]
        # もしcase名が異なっていたら，かつ，組織も違っており，かつ，もしそのタスクの組み合わせがあり得るものだったら
        # A->B，B->Aは出ないようになっている
        # if case1 != case2 and case1[-1] != case2[-1] and (task1,task2) in pair:
        if case1 != case2 and case1[-1] != case2[-1] and (task1,task2) in ans1:
            if (case1,case2) not in c_pattern:
                if (case2,case1) not in c_pattern:
                    c_pattern[(case1,case2)] = 1
                else:
                    c_pattern[(case2,case1)] += 1
            else:
                c_pattern[(case1,case2)] += 1
        case1 = case2
        task1 = task2


    # あるケースが複数ケースと結びつく場合を排除する工程(指標1.1の整理)
    # もしあるケースが複数のケースと結びつく可能性があった場合 → カウントが多い方と結びつくようにする
    # つまり3回以上同じかも判定されたものの中で，
    # 同じかも判定された数の多い順に対応づけする．
    # liは[ケース，ケース]という対応づけられたケース名のペアが要素の配列
    import copy
    import datetime
    for_sort = []
    
    #　指標1.1の整理
    m = 40
    li = list(c_pattern.values())
    
    for k, v in c_pattern.items():
        if v > v1_threshold:
            # A -> Oの順番にする
            if k[0][-1] == 'O':
                for_sort.append([k[1],k[0],v])
            else:
                for_sort.append([k[0],k[1],v])
    for_sort.sort()

    li = []
    i = 0
    while i < len(for_sort):
        j = 1
        tmp = [for_sort[i][0],for_sort[i][1],for_sort[i][2]]
        while 1:
            if i + j == len(for_sort) or for_sort[i][0] != for_sort[i+j][0]:
                li.append(tmp)
                break
            else:
                if tmp[2] < for_sort[i+j][2]:
                    tmp = [for_sort[i+j][0],for_sort[i+j][1], for_sort[i+j][2]]
                j += 1
        i += j
    for_sort = copy.deepcopy(li)
    for_sort.sort(key=lambda x: x[1])
    li = []
    i = 0
    while i < len(for_sort):
        j = 1
        tmp = [for_sort[i][0],for_sort[i][1],for_sort[i][2]]
        while 1:
            if i + j == len(for_sort) or for_sort[i][1] != for_sort[i+j][1]:
                li.append([tmp[0],tmp[1]])
                break
            else:
                if tmp[2] < for_sort[i+j][2]:
                    tmp = [for_sort[i+j][0],for_sort[i+j][1], for_sort[i+j][2]]
                j += 1
        i += j

    for i in li:
        cor[i[0]] = i[1]
        cor[i[1]] = i[0]

    nt = []
    for i in range(len(t)):
        if t[i][3] not in cor:
            nt.append(t[i])

            

    # 評価
    # 全ケース数
    num = set()
    for i in t:
        num.add(i[2])
    a = len(num)
    #print("残っているデータの全ケース数",a)

    # 対応づけられたケース数と誤って対応づけられたケース数
    correct_num = 0
    miss = 0
    for k, v in cor.items():
        if k[:-2] != v[:-2]:
            miss+=1
        else:
            correct_num+=1
    #print("対応づけられたケース数は",correct_num+miss)
    #print("誤って対応づけられたケース数は",miss)
    # 対応づけた中でのケースの正解率
    #if correct_num+miss != 0:
    #    print("適合率(Precision)は",correct_num/(correct_num+miss))
    #    print("再現率(Recall)は",correct_num/(31509*2))
    #print("\n")

    
    # 組織間を跨ぐ移動をしている部分のタスクのペアと時間差を抽出し，それをまだケースが対応づけられていない部分に適用してみる
    # dicはケース名がkey，（タスク,時刻)の流れがvalueの辞書
    dic = {}
    for i in t:
        if i[3] in cor:
            # もしケース名がdicに入っていなかったら
            if i[3] not in dic:
                if cor[i[3]] not in dic:
                    dic[i[3]] = [(i[1],i[0])]
                else:
                    dic[cor[i[3]]].append((i[1],i[0]))
            else:
                dic[i[3]].append((i[1],i[0]))
    
    # interはタスクのペアをkey,[時間差の配列, カウント]をvalueとした辞書
    for v in dic.values():
        pre = v[0]
        for i in range(1,len(v)):
            # もし異なる組織だったら(taskの名前の頭文字で判別)
            if pre[0][0] != v[i][0][0]:
                if (pre[0],v[i][0]) not in inter:
                    inter[(pre[0],v[i][0])] = [[v[i][1] - pre[1]],1]
                else:
                    inter[(pre[0],v[i][0])][0].append(v[i][1] - pre[1])
                    inter[(pre[0],v[i][0])][1] += 1
            pre = v[i]
    
    #print("検出されたタスクペア数は",len(inter))
    f_inter = {}
    for k, v in inter.items():
        if v[1] > n2_threshold:
            f_inter[k] = v[0]
    #print("閾値nによって絞られた後のタスクペア数は",len(f_inter))
    
    import statistics
    from scipy import stats
    task_time = {}
    for k, v in f_inter.items():
        li = [i.total_seconds() for i in v]
        if len(li) < 10:
            continue
        c = 0
        for diff in li:
            if diff <= T.total_seconds():
                c += 1
        if c/len(li) > 0.95:
        # if statistics.variance(li) < 10*5:
        # if statistics.variance(li) < 10**50:
            #t_dist = stats.t(loc=statistics.mean(li),scale=np.sqrt(statistics.variance(li)/10),df=len(li)-1)
            #alphaが求めたい区間に含まれる確率#alphaも閾値
            # 値を小さくすると条件が厳しくなる
            #bottom, up = t_dist.interval(alpha=0.95)
            bottom, up = np.percentile(li,q=[2.5,97.5])
            #print(bottom,up)
            task_time[k] = [statistics.mean(li),statistics.median(li),bottom,up]
            #print(k)
            
    import bisect
    # bisectのために時間のみの配列を作る(始めてから何秒経ったか)
    for_bisect = []
    # 記録が取られ始めた時間
    start = datetime.datetime(2016, 1, 1, 9, 51, 15)
    for row in nt:
        for_bisect.append((row[0]-start).total_seconds())
    
    
    # ntの長さはO(10^5)くらい
    for i in range(len(nt)):
        # task_timeの長さはO(10^2)くらい
        for tasks, time in task_time.items():
            if nt[i][1] == tasks[0]:
                # time[2](時間差の中央値)後にtasks[1]が存在するかを調べる．計算量的にO(100)くらいの探索しかできない(全てでO(10^10~10^11)となる．)
                # (現在の時間+時間差)にあたる時間が何行目になるかを検索しなくてはならない．二分探索をするとO(log100000) = O(17)
                # 統計的に決定する．
                #index = bisect.bisect_left(for_bisect,(for_bisect[i]+time[1]-margin))
                index = bisect.bisect_left(for_bisect,(for_bisect[i]+max(0,time[2])))
                j = 1
                #while index+j < len(for_bisect) and for_bisect[index+j] < for_bisect[i]+time[1]+margin:
                while index+j < len(for_bisect) and for_bisect[index+j] < for_bisect[i]+time[3]:
                    if nt[i][3] == nt[index+j][3]:
                        break
                    if tasks[1] == nt[index+j][1]:
                        if (nt[i][3],nt[index+j][3]) not in c_pattern:
                            if (nt[index+j][3],nt[i][3]) not in c_pattern:
                                c_pattern[(nt[i][3],nt[index+j][3])] = 1
                            else:
                                c_pattern[(nt[index+j][3],nt[i][3])] += 1
                        else:
                            c_pattern[(nt[i][3],nt[index+j][3])] += 1
                    j += 1


    

    t = copy.deepcopy(nt)
    nt = []
    for i in range(len(t)):
        if t[i][3] not in cor:
            nt.append(t[i])
    return nt, cor, inter, c_pattern


def identify(t,n1,v,n2,T_set,bo):
    noize = 0
    ans = []
    precision = 0
    recall = 0
    for n1_threshold in n1:
        for v_threshold in v:
            for n2_threshold in n2:
                for T in T_set:
                    print(n1_threshold,v_threshold,n2_threshold,T)
                    nt = t
                    cor = {}
                    inter = {}
                    c_pattern = {}
                    tmp = 0
                    for i in range(20):
                        nt, cor, inter, c_pattern = case_cor(nt,cor,inter,c_pattern,T,n1_threshold,v_threshold,n2_threshold)
                        if tmp == len(nt) or len(nt) == 0:
                            break
                        tmp = len(nt)
                    correct_num = 0
                    miss = 0
                    for k, vv in cor.items():
                        if k[:-2] != vv[:-2]:
                            miss+=1
                        else:
                            correct_num+=1
                    if correct_num+miss != 0:
                        print("適合率(Precision)は",correct_num/(correct_num+miss))
                        print("再現率(Recall)は",correct_num/(bo*2))
                        print("\n")
                    #対応づけられたケースからプロセスを作成
                    dic = {}
                    for i in t:
                        if i[3] in cor:
                            if i[3] not in dic:
                                if cor[i[3]] not in dic:
                                    dic[i[3]] = [i[1]]
                                else:
                                    dic[cor[i[3]]].append(i[1])
                            else:
                                dic[i[3]].append(i[1])

                    from collections import defaultdict
                    d = defaultdict(int)
                    for process in dic.values():
                        d[tuple(process)] += 1
                    flow = defaultdict(int)
                    for process,num in d.items():
                        for i in range(1,len(process)):
                            flow[(process[i-1],process[i])] += num
                    c = 0
                    boundary = bo * 0.01
                    out = {}
                    for pair,num in flow.items():
                        if num < boundary:
                            c += 1
                        else:
                            out[pair] = num
                    if correct_num+miss != 0:
                        ans.append([c,correct_num/(correct_num+miss),correct_num/(bo*2),out,cor,len(cor)/(bo*2)])
                    else:
                        ans.append([c,'-','-',out,cor,len(cor)/(bo*2)])
    return ans