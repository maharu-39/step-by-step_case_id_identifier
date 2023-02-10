import pandas as pd
import numpy as np
import datetime as dt
import os.path as osp
from argparse import ArgumentParser

import pre_process
import identify
import post_process

def main():
    parser = ArgumentParser()
    parser.add_argument('datasets')
    args = parser.parse_args()
    pre_process.to_csv(args.datasets)
    pre_process.process(f"{osp.splitext(args.datasets)[0]}.csv")
  
    df = pd.read_csv("datasets/edited/aando.csv")
    tmp = df["time:timestamp"].str.split('+').to_numpy()
    time = []
    for i in tmp:
        time.append(i[0])
    event = df["concept:name"].to_numpy()
    case = df["case:concept:name"]
    t = []
    for i in range(len(tmp)):
        t.append([dt.datetime.fromisoformat(time[i].replace(' ','T')), event[i],case[i]])
    t.sort()
    for i in t:
        if i[1][0] == 'A':
            i.append(i[2]+'_A')
        else:
            i.append(i[2]+'_O')
    bo = 0
    tmp = {}
    for i in t:
        if i[2] in tmp:
            if i[3][-1] not in tmp[i[2]]:
                tmp[i[2]].add(i[3][-1])
                bo += 1
        else:
            tmp[i[2]] = {i[3][-1]}
    boundary = bo * 0.01
    

    n1 = [1,4,16,64,256,1000,4000,16000]
    v = [0,1,2,3,4,6,8]
    n2 = [1,4,16,64,256,1000,4000,16000]
    T_set = [dt.timedelta(seconds=1),dt.timedelta(seconds=10),dt.timedelta(seconds=100),dt.timedelta(seconds=1000)]
    ans = identify.identify(t,n1,v,n2,T_set,bo)
    index = post_process.select_param(ans)
    post_process.eval(t,ans,index,boundary)





if __name__ == '__main__':
  main()