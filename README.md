# Step-by-Step Case ID Identifier based on Activity Connection for Cross-Organizational Process Mining

This repository contains the source code for the paper "Step-by-Step Case ID Identification based on Activity Connection for Cross-Organizational Process Mining".


## Getting Started
```
step-by-step_case_id_identifier
|- datasets/
        |- BPI_Challenge_2012.xes
        |- BPI_Challenge_2017.xes
|- src/
  ...
|- results/
  ...
```

### Download dataset
Please download datasets, [BPIC2012](https://data.4tu.nl/articles/dataset/BPI_Challenge_2012/12689204), [BPIC2017](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884).

### Dependencies
- Python 3.10.10
- numpy 1.23.1
- pandas 1.4.4
- pm4py 2.5.1

*** In case Arm-Based Macs, run below command to avoid an error.
`pip uninstall cvxopt`

### Quick demo
`python3 src/demo.py datasets/BPI_Challenge_2017.xes`

This will produce integrated event logs (A+O) under `step-by-step_case_id_identifier/results/`.


https://github.com/yoichiro0406/cascading_feature_extraction
https://github.com/una-dinosauria/3d-pose-baseline
