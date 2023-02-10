from collections import defaultdict

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
  print("case:precisionは",ans[index][1])
  print("case:precisionは",ans[index][2])
  # 正解フローは何本か
  print("flow:precisionは",same/num)
  print("flow:recallは",same/cor_num)