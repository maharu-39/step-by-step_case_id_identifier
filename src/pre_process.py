# Copyright (C) 2023 The University of Tokyo and Nippon Telegraph and Telephone Corporation

import pm4py
import pandas as pd
import os
import os.path as osp
from pm4py.objects.conversion.log import converter as log_converter

def to_csv(dataset):
  '''
  .xes to .csv
  '''
  log = pm4py.read_xes(dataset)
  dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
  dataframe.to_csv(f"datasets/{osp.splitext(osp.basename(dataset))[0]}.csv")

def f(x):
    if len(x) == 25:
        return x[:19] + ".000"
    else:
        return x[:23]
  
def process(dataset):
  '''
  process data
  '''
  data = pd.read_csv(dataset)
  print(dataset)
  if dataset == "datasets/BPI_Challenge_2017.csv":
    aandw = data[(data["EventOrigin"] == "Application") | (data["EventOrigin"] == "Workflow")]
    aando = data[(data["EventOrigin"] == "Application") | (data["EventOrigin"] == "Offer")]
    oandw = data[(data["EventOrigin"] == "Offer") | (data["EventOrigin"] == "Workflow")]
  elif dataset == "datasets/BPI_Challenge_2012.csv":
    aandw = data[data["concept:name"].str.startswith("A") | data["concept:name"].str.startswith("W")]
    aando = data[data["concept:name"].str.startswith("A") | data["concept:name"].str.startswith("O")]
    oandw = data[data["concept:name"].str.startswith("O") | data["concept:name"].str.startswith("W")]
  else:
    print("DATASET ERROR\n")
    exit()
  data["time:timestamp"] = data["time:timestamp"].map(f)
  aandw["time:timestamp"] = aandw["time:timestamp"].map(f)
  aando["time:timestamp"] = aando["time:timestamp"].map(f)
  oandw["time:timestamp"] = oandw["time:timestamp"].map(f)
  if not osp.exists("datasets/edited"):
    os.makedirs("datasets/edited")
  aandw.to_csv("datasets/edited/aandw.csv")
  aando.to_csv("datasets/edited/aando.csv")
  oandw.to_csv("datasets/edited/oandw.csv")
