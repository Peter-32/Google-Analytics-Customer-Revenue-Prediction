import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
from pandas.io.json import json_normalize
import missingno as msno
from sklearn.preprocessing import StandardScaler
from pandasql import sqldf
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

# ETL


JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']
df = pd.read_csv('/Users/peterjmyers/Work/Google-Analytics-Customer-Revenue-Prediction/data/train.csv',
                 converters={column: json.loads for column in JSON_COLUMNS},
                 dtype={'fullVisitorId': 'str'},
                 nrows=5)
building_df = pd.DataFrame()
for index, row in df.iterrows():
    temp_dfs = []
    for column in JSON_COLUMNS:
        temp_df = json_normalize(row[column])
        temp_df.columns = ["{}.{}".format(
            column, subcolumn) for subcolumn in temp_df.columns]
        temp_dfs.append(temp_df)
    final_temp_df = pd.concat(temp_dfs, axis=1)
    building_df = pd.concat([building_df, final_temp_df], ignore_index=True)
df.drop(JSON_COLUMNS, axis=1, inplace=True)
df = pd.concat([df, building_df], axis=1)
df


df['transactionRevenue']
