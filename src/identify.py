import pandas as pd
import numpy as np
import datetime as dt
import load
from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('dataset')
  args = parser.parse_args()
  load(args.dataset)






if __name__ == '__main__':
  main()