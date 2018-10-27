import os
from pandas import read_csv, DataFrame, concat, to_numeric
import matplotlib.pyplot as plt
from json import loads
from pandas.io.json import json_normalize
from pandasql import sqldf
from sklearn.cluster import KMeans
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

JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']

class ETL():

    def read_in_dataframe(self):
        return read_csv('data/train.csv',
                         converters={column: loads for column in JSON_COLUMNS},
                         dtype={'fullVisitorId': 'str'},
                         nrows=5000)

    def get_json_columns(self, df):
        building_df = DataFrame()
        for index, row in df.iterrows():
            temp_dfs = []
            for column in JSON_COLUMNS:
                temp_df = json_normalize(row[column])
                temp_df.columns = ["{}.{}".format(
                    column, subcolumn) for subcolumn in temp_df.columns]
                temp_dfs.append(temp_df)
            final_temp_df = concat(temp_dfs, axis=1)
            building_df = concat([building_df, final_temp_df], ignore_index=True)
        df.drop(JSON_COLUMNS, axis=1, inplace=True)
        df = concat([df, building_df], axis=1)
        df.to_csv("tables/_rows_5000.csv")
        return df

    def fix_transaction_revenue(self, df):
        df['totals.transactionRevenue'] = df['totals.transactionRevenue'].fillna(0)
        return df

    def convert_columns_to_numeric(self, df):
        for column in ['totals.bounces', 'totals.hits', 'totals.newVisits', 'totals.pageviews', 'totals.transactionRevenue', 'totals.visits']:
            df[column] = to_numeric(df[column], errors="coerce")
        return df

    def add_k_means_cluster_id(self, df):
        X = df[['visitNumber','totals.bounces','totals.hits','totals.newVisits','totals.pageviews','totals.visits']].values
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        df.loc[:, 'cluster_ids'] = kmeans.labels_
        return df, kmeans
        # kmeans.predict([[0, 0], [4, 4]])

#
# Index(['channelGrouping', 'date', 'fullVisitorId', 'sessionId',
#        'socialEngagementType', 'visitId', 'visitNumber', 'visitStartTime',
#        'device.browser', 'device.browserSize', 'device.browserVersion',
#        'device.deviceCategory', 'device.flashVersion', 'device.isMobile',
#        'device.language', 'device.mobileDeviceBranding',
#        'device.mobileDeviceInfo', 'device.mobileDeviceMarketingName',
#        'device.mobileDeviceModel', 'device.mobileInputSelector',
#        'device.operatingSystem', 'device.operatingSystemVersion',
#        'device.screenColors', 'device.screenResolution', 'geoNetwork.city',
#        'geoNetwork.cityId', 'geoNetwork.continent', 'geoNetwork.country',
#        'geoNetwork.latitude', 'geoNetwork.longitude', 'geoNetwork.metro',
#        'geoNetwork.networkDomain', 'geoNetwork.networkLocation',
#        'geoNetwork.region', 'geoNetwork.subContinent', 'totals.bounces',
#        'totals.hits', 'totals.newVisits', 'totals.pageviews',
#        'totals.transactionRevenue', 'totals.visits', 'trafficSource.adContent',
#        'trafficSource.adwordsClickInfo.adNetworkType',
#        'trafficSource.adwordsClickInfo.criteriaParameters',
#        'trafficSource.adwordsClickInfo.gclId',
#        'trafficSource.adwordsClickInfo.isVideoAd',
#        'trafficSource.adwordsClickInfo.page',
#        'trafficSource.adwordsClickInfo.slot', 'trafficSource.campaign',
#        'trafficSource.isTrueDirect', 'trafficSource.keyword',
#        'trafficSource.medium', 'trafficSource.referralPath',
#        'trafficSource.source'],


    def get_initial_features(self, df):
        return sqldf("""
        SELECT
            a.`totals.hits` AS hits
          , a.`totals.pageviews` AS page_views
          , a.`trafficSource.source` AS traffic_source
          , a.`geoNetwork.country` AS country
          , a.`geoNetwork.city` AS city
          , a.`geoNetwork.networkDomain` AS network_domain
          , a.`geoNetwork.region` AS region
          , CASE WHEN strftime('%w', substr(a.date,0,5) || "-" || substr(a.date,5,2) || "-" || substr(a.date,7,2)) IN ('0', '6') THEN 1 ELSE 0 END AS is_weekend
          , a.`device.deviceCategory` AS device_category
          , a.visitNumber AS visit_number
          , a.`totals.newVisits` AS new_visits
          , a.`channelGrouping` AS channel_grouping
          , a.`trafficSource.medium` AS medium
          , IF(a.`geoNetwork.subContinent` = 'Northern America', 1, 0) AS is_sub_continent_north_america
          , a.visitStartTime AS visit_start_time
          , a.`geoNetwork.metro` AS metro
          , a.`trafficSource.referralPath` AS referral_path
          , a.cluster_id
          , a.`trafficSource.keyword` AS keyword
          , a.`totals.hits` / a.`totals.pageviews` AS hits_per_pageview
          , CAST(strftime('%W', substr(a.date,0,5) || "-" || substr(a.date,5,2) || "-" || substr(a.date,7,2)) AS unsigned) AS week_of_year 
          , b.month_unique_user_count
          , b.month_unique_sessions
          , c.network_domain_hits
          , c.network_domain_mean_hits
          , c.network_domain_mean_page_views
          , d.day_unique_user_count
          , d.day_mean_hits
          , d.day_var_like_formula_hits
          , d.day_unique_sessions
          , e.country_max_pageviews
          , e.country_mean_pageviews
          , f.city_mean_pageviews
          , g.weekday_unique_sessions

        from df a
        INNER JOIN
            (
            SELECT
                SUBSTR(date, 0, 5) year
              , CAST(SUBSTR(date, 5, 2) AS int) month
              , COUNT(distinct fullVisitorId) AS month_unique_user_count
              , COUNT(distinct fullVisitorId || "_" || visitId) AS month_unique_sessions
            FROM df
            GROUP BY 1,2
            ) b ON b.year = SUBSTR(a.date, 0, 5)
               AND b.month = CAST(SUBSTR(a.date, 5, 2) AS int)
        INNER JOIN
            (
            SELECT
                `geoNetwork.networkDomain`
              , SUM(`totals.hits`) AS network_domain_hits
              , AVG(`totals.hits`) AS network_domain_mean_hits
              , AVG(`totals.pageviews`) AS network_domain_mean_page_views
            FROM df
            GROUP BY 1
            ) c ON c.`geoNetwork.networkDomain` = a.`geoNetwork.networkDomain`
        INNER JOIN
            (
            SELECT
                date
              , COUNT(distinct fullVisitorId) AS day_unique_user_count
              , AVG(`totals.hits`) AS day_mean_hits
              , (SUM(`totals.hits` * `totals.hits`) / COUNT(*)) - ((SUM(`totals.hits`)/COUNT(*))*(SUM(`totals.hits`)/COUNT(*))) AS day_var_like_formula_hits
              , COUNT(distinct fullVisitorId || "_" || visitId) AS day_unique_sessions
            FROM df
            GROUP BY 1
            ) d ON d.date = a.date
        INNER JOIN
            (
            SELECT
                geoNetwork.country
              , MAX(`totals.pageviews`) AS country_max_pageviews
              , AVG(`totals.pageviews`) AS country_mean_pageviews
            FROM df
            GROUP BY 1
            ) e ON e.`geoNetwork.country` = a.`geoNetwork.country`
        INNER JOIN
            (
            SELECT
                geoNetwork.city
              , AVG(`totals.pageviews`) AS city_mean_pageviews
            FROM df
            GROUP BY 1
            ) f ON f.`geoNetwork.city` = a.`geoNetwork.city`
        INNER JOIN
            (
            SELECT
                strftime('%w', substr(a.date,0,5) || "-" || substr(a.date,5,2) || "-" || substr(a.date,7,2)) AS weekday
              , COUNT(distinct fullVisitorId || "_" || visitId) AS weekday_unique_sessions
            FROM df a
            GROUP BY 1
            ) g ON g.weekday = strftime('%w', substr(a.date,0,5) || "-" || substr(a.date,5,2) || "-" || substr(a.date,7,2))
        """, locals())

    def save(self, df):
        df.to_csv('tables/etl.csv')

if __name__ == '__main__':
    etl = ETL()
    df = etl.read_in_dataframe()
    df = etl.get_json_columns(df)
    df = etl.fix_transaction_revenue(df)
    df = etl.convert_columns_to_numeric(df)
    df, kmeans = etl.add_k_means_cluster_id(df)
    df = etl.get_initial_features(df)
    etl.save(df)
    print(df.head())
