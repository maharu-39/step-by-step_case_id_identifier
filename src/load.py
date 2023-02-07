import pm4py
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
# from pm4py.objects.log.exporter.csv import factory as csv_exporter

log = pm4py.read_xes("BPI Challenge 2012.xes")
process_model = pm4py.discover_bpmn_inductive(log)
# pm4py.view_bpmn(process_model)
print(log[0])
print(log[0][0])

# csv_exporter.export(log, "data.csv")

dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
dataframe.to_csv("BPIC2012.csv")