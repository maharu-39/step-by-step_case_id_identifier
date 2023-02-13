import pandas as pd
import numpy as np
import datetime as dt
import bisect
import copy
import statistics
from collections import defaultdict



def case_cor(t,cor,inter,c_pattern, T_threshold,n1_threshold,v1_threshold,n2_threshold,org_name):
    '''
    identify case ID one time.
    '''
    # Identification of the connection of activities
    T = T_threshold
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

    # Identification of case IDs
    case1 = t[0][3]
    task1 = t[0][1]
    l = len(t)
    for i in range(1,l):
        case2 = t[i][3]
        task2 = t[i][1]
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


    for_sort = []
    li = list(c_pattern.values())
    for k, v in c_pattern.items():
        if v > v1_threshold:
            if k[0][-1] == f"{org_name}":
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

            
    
    # Extraction of activity connections and time differences based on identified case IDs
    dic = {}
    for i in t:
        if i[3] in cor:
            if i[3] not in dic:
                if cor[i[3]] not in dic:
                    dic[i[3]] = [(i[1],i[0])]
                else:
                    dic[cor[i[3]]].append((i[1],i[0]))
            else:
                dic[i[3]].append((i[1],i[0]))
    
    for v in dic.values():
        pre = v[0]
        for i in range(1,len(v)):
            if pre[0][0] != v[i][0][0]:
                if (pre[0],v[i][0]) not in inter:
                    inter[(pre[0],v[i][0])] = [[v[i][1] - pre[1]],1]
                else:
                    inter[(pre[0],v[i][0])][0].append(v[i][1] - pre[1])
                    inter[(pre[0],v[i][0])][1] += 1
            pre = v[i]
    
    f_inter = {}
    for k, v in inter.items():
        if v[1] > n2_threshold:
            f_inter[k] = v[0]
    
    

    # Assistance for identification of case IDs
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
            bottom, up = np.percentile(li,q=[2.5,97.5])
            task_time[k] = [statistics.mean(li),statistics.median(li),bottom,up]
            
    for_bisect = []
    start = dt.datetime(2016, 1, 1, 9, 51, 15)
    for row in nt:
        for_bisect.append((row[0]-start).total_seconds())
    
    
    for i in range(len(nt)):
        for tasks, time in task_time.items():
            if nt[i][1] == tasks[0]:
                index = bisect.bisect_left(for_bisect,(for_bisect[i]+max(0,time[2])))
                j = 1
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


def identify(t,n1,v,n2,T_set,bo,org_name):
    ans = []
    for n1_threshold in n1:
        for v_threshold in v:
            for n2_threshold in n2:
                for T in T_set:
                    print(f"th1:{n1_threshold}, th2:{v_threshold}, th3:{n2_threshold}, th4:{T}")
                    nt = t
                    cor = {}
                    inter = {}
                    c_pattern = {}
                    tmp = 0
                    # identify case ID repeatedly.
                    for i in range(20):
                        nt, cor, inter, c_pattern = case_cor(nt,cor,inter,c_pattern,T,n1_threshold,v_threshold,n2_threshold,org_name)
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
                        print("Precision: ",correct_num/(correct_num+miss))
                        print("Recall: ",correct_num/(bo*2))
                        print("\n")
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