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
  data = pd.read_csv(f"datasets/{osp.splitext(osp.basename(dataset))[0]}.csv")
  aandw = data[(data["EventOrigin"] == "Application") | (data["EventOrigin"] == "Workflow")]
  aando = data[(data["EventOrigin"] == "Application") | (data["EventOrigin"] == "Offer")]
  oandw = data[(data["EventOrigin"] == "Offer") | (data["EventOrigin"] == "Workflow")]
  data["time:timestamp"] = data["time:timestamp"].map(f)
  aandw["time:timestamp"] = aandw["time:timestamp"].map(f)
  aando["time:timestamp"] = aando["time:timestamp"].map(f)
  oandw["time:timestamp"] = oandw["time:timestamp"].map(f)
  if not osp.exists("datasets/edited"):
    os.makedirs("datasets/edited")
  aandw.to_csv("edited/aandw.csv")
  aando.to_csv("edited/aando.csv")
  oandw.to_csv("edited/oandw.csv")

def load(dataset):
  '''
  load csv file
  '''