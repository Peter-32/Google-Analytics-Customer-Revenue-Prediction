import os
from pandas import read_csv, DataFrame, concat, to_numeric
import matplotlib.pyplot as plt
from json import loads
from pandas.io.json import json_normalize
from pandasql import sqldf
# import seaborn as sns
# import numpy as np
#import missingno as msno
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error
# from sklearn import linear_model, neighbors, tree, svm, ensemble
# from xgboost import XGBRegressor
# from sklearn.pipeline import make_pipeline
# from tpot.builtins import StackingEstimator
# from sklearn.model_selection import KFold
# from sklearn.model_selection import cross_val_score
# from sklearn.grid_search import GridSearchCV
# from sklearn.pipeline import Pipeline
# from scipy.stats import boxcox
# from scipy.special import inv_boxcox

def q(q): return sqldf(q, globals())

# read_csv('data/train.csv',
#                  converters={column: loads for column in JSON_COLUMNS},
#                  dtype={'fullVisitorId': 'str'},
#                  nrows=5000)

df = DataFrame({'a':[1,2,3]})

print(q("""select substr("20160802",0,5) || "-" || substr("20160802",5,2) || "-" || substr("20160802",7,2) from df"""))
