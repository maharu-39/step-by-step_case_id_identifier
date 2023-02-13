import pandas as pd
import numpy as np
import datetime as dt
from argparse import ArgumentParser
import csv
import os.path as osp

'''
The argument is an integrated log which is csv file.
To import to Disco, the case IDs which contain noises are removed.
'''

def main():
  parser = ArgumentParser()
  parser.add_argument('data')
  parser.add_argument('case_num')
  parser.add_argument('out_dir')
  args = parser.parse_args()
  data = pd.read_csv(args.data)
  
  data = data.sort_values('time')
  case = data['case'].to_numpy()
  task = data['activity'].to_numpy()
  time = data['time'].to_numpy()
  t = []
  bo = int(args.case_num)
  for i in range(len(time)):
      t.append([time[i], task[i],case[i]])
  sup = {} 
  tmp = {} 
  for i in range(len(case)):
      if case[i] in tmp:
          tmp[case[i]].append(task[i])
          sup[str(case[i])].append((task[i],time[i]))
      else:
          tmp[case[i]] = [task[i]]
          sup[str(case[i])] = [(task[i],time[i])]
  dic = {}
  for process in tmp.values():
      for i in range(1,len(process)):
          if (process[i-1],process[i]) not in dic:
              dic[(process[i-1],process[i])] = 1
          else:
              dic[(process[i-1],process[i])] += 1
  s = set()
  for k,v in dic.items():
      if v < bo * 0.01:
          s.add(k)
  case = set()
  for k, v in tmp.items():
      for i in range(1,len(v)):
          if (v[i-1],v[i]) in s:
              break
          if i == len(v) - 1:
              case.add(k)
  ans = [["time","activity","case"]]
  for i in t:
      if i[2] in case:
          ans.append(i)
  
  f = open(f"{args.out_dir}/{osp.basename(args.data)}", "w", newline='')
  writer = csv.writer(f)
  writer.writerows(ans)
  f.close()

if __name__ == '__main__':
  main()