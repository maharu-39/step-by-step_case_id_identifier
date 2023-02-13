from collections import defaultdict
import csv

def select_param(ans):
  ans.sort(key=lambda x: x[0])
  index = 0
  for index in range(len(ans)):
      if ans[index][1] != '-' and ans[index][5] > 0:
          break
  return index

def eval(t,ans,index,boundary):
  # 正解データのとりこみ(2017,2012兼用 / ノイズ除去機構あり)
  dic = {}
  for i in t:
      if i[2] not in dic:
          dic[i[2]] = [i[1]]
      else:
          dic[i[2]].append(i[1])
  dic2 = {}
  for v in dic.values():
      org = set()
      for i in v:
          org.add(i[0])
      if len(org) > 1:
          if tuple(v) not in dic2:
              dic2[tuple(v)] = 1
          else:
              dic2[tuple(v)] += 1
  cor_fl = defaultdict(int)
  cor_flow = defaultdict(int)
  for k,v in dic2.items():
      for i in range(1,len(k)):
          if (k[i-1],k[i]) not in cor_fl:
              cor_fl[(k[i-1],k[i])] = v
          else:
              cor_fl[(k[i-1],k[i])] += v
  for k,v in cor_fl.items():
      if v > boundary:
          cor_flow[k] = v
  cor_num= len(cor_flow)

  flow = ans[index][3]
  num = 0
  same = 0
  for k, v in flow.items():
      if v > 0:
          num += 1
          if cor_flow[k] > 0:
              same += 1

  
  #ケース対応付け
  print("case:precision",ans[index][1])
  print("case:precision",ans[index][2])
  # 正解フローは何本か
  print("flow:precision",same/num)
  print("flow:recall",same/cor_num)


def save(t,ans,index,out_path):
  fin = {}
  token = 0
  for k,v in ans[index][4].items():
      if k not in fin and v not in fin:
          fin[k] = token
          fin[v] = token
          token += 1

  for i in range(len(t)):
      if t[i][3] in fin:
          t[i].append(fin[t[i][3]])
  ansdata = [["time","activity","real","tmp","case"]]
  for i in t:
      if len(i) == 5:
          ansdata.append(i)
  for i in range(1,len(ansdata)):
      ansdata[i][0] = ansdata[i][0].strftime('%Y-%m-%d %H:%M:%S.%f')
  f = open(f"results/{out_path}", 'w', newline='')
  writer = csv.writer(f)
  writer.writerows(ansdata)
  f.close()