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

q = lambda q: sqldf(q, globals())

# ETL

JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']
df = pd.read_csv('/Users/peterjmyers/Work/Google-Analytics-Customer-Revenue-Prediction/data/train.csv',
                 converters={column: json.loads for column in JSON_COLUMNS},
                 dtype={'fullVisitorId': 'str'},
                 nrows=5)
df.dtypes

# df = df['totals'].apply(lambda x: json_normalize(x))
# df



for i in range()
json_normalize(df['totals'][i])
df['totals'][0]
















def load_df(csv_path='/Users/peterjmyers/Work/Google-Analytics-Customer-Revenue-Prediction/data/train.csv', nrows=None):
    JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']

    df = pd.read_csv(csv_path,
                     converters={column: json.loads for column in JSON_COLUMNS},
                     dtype={'fullVisitorId': 'str'},
                     nrows=nrows)

    for column in JSON_COLUMNS:
        print(column)
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
    print(f"Loaded {os.path.basename(csv_path)}. Shape: {df.shape}")
    return df


# pd.read_csv('/Users/peterjmyers/Work/Google-Analytics-Customer-Revenue-Prediction/data/train.csv', nrows=5)


df = load_df(nrows=5)
df


df = pd.DataFrame(load_df(nrows=5)['totals.totals'])

df.columns


df['totals.totals']


column_as_df = json_normalize(df['totals.totals'])
#column_as_df['totals'] = column_as_df['totals.totals']
column_as_df


column = "totals.totals"
column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
column_as_df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
column_as_df
