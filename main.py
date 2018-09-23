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

# Prepare Data
df = pd.read_csv("/Users/peterjmyers/Work/Google-Analytics-Customer-Revenue-Prediction/data/train.csv")
df
# , header=None, names = ['CRIM','INDUS','CHAS','NOX','RM','AGE','RAD','TAX','PTRATIO','B','LSTAT','MEDV']
# X = df.drop(["MEDV"], axis=1).values
# scaler = StandardScaler()
# X = scaler.fit_transform(X)
# y = df["MEDV"].values
