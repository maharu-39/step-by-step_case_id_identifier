'''
Data Loader
'''
import pm4py
import pandas as pd
import os.path as osp
from pm4py.objects.conversion.log import converter as log_converter

def load(dataset):
  #log = pm4py.read_xes("BPI Challenge 2012.xes")
  log = pm4py.read_xes(dataset)
  dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
  #dataframe.to_csv("BPIC2012.csv")
  dataframe.to_csv(f"{osp.basename(dataset)}.csv")