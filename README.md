# Google-Analytics-Customer-Revenue-Prediction

### Question

Can we predict the lifetime value of a customer with the provided dataset?  Planning to give my best effort without spending over 20 hours on this project.

### Hypothesis

We can predict the lifetime value of a customer using the data provided.  

### Data Sources

- https://www.kaggle.com/c/ga-customer-revenue-prediction/data

### Data Descriptions

- fullVisitorId: A unique identifier for each user of the Google Merchandise Store.
- channelGrouping: The channel via which the user came to the Store.
- date: The date on which the user visited the Store.
- device: The specifications for the device used to access the Store.
- geoNetwork: This section contains information about the geography of the user.
- sessionId: A unique identifier for this visit to the store.
- socialEngagementType: Engagement type, either "Socially Engaged" or "Not Socially Engaged".
- totals: This section contains aggregate values across the session.
- trafficSource: This section contains information about the Traffic Source from which the session originated.
- visitId: An identifier for this session. This is part of the value usually stored as the utmb cookie. This is only unique to the user. For a completely unique ID, you should use a combination of fullVisitorId and visitId.
- visitNumber: The session number for this user. If this is the first session, then this is set to 1.
- visitStartTime: The timestamp (expressed as POSIX time).

### Steps

- Pass a parameter to start at step X
- ETL
  - X Realized other kernels used json_normalize, but their code didn't work for me.
  - X Loop over dataframes and do json_normalize to build a new dataframe or something (only works one row at a time last I tried)
  - X Missing transactionRevenue means no transaction
  - X Features (Give credit for the feature names found on Kernels, won't copy anyone's feature engineering code)
    - https://www.kaggle.com/youhanlee/stratified-sampling-for-regression-lb-1-6595
      - X total hits
      - X total pageviews
      - X trafficSource.source
      - X network country
      - X network city  
      - X month unique user count
      - X mean hits per network domain
      - X day unique user count
      - X network domain
      - X network region
      - X mean hits per day
      - X mean page views per network domain
      - X count hits per network domain
      - X total new visits
    - https://www.kaggle.com/erikbruin/google-analytics-eda-with-screenshots-of-the-app
      - X Saturday/Sunday appear to have low sales (Very low conversion rate too)
    - https://www.kaggle.com/nulldata/ga-eda-digital-analytics-h2o-rf-1-86
      - X pageviews
      - X hits
      - X visit number
    - https://www.kaggle.com/prashantkikani/howmuch-train-test-data-are-different
      - X browser_category
      - X count hits per network domain
      - X month unique user count
      - X day unique user count
      - X sum hits per day
      - X var hits per day
    - https://www.kaggle.com/plasticgrammer/customer-revenue-prediction-playground
      - X new visits
      - X channel grouping referral
      - X medium referral
      - X sub continent north america
    - https://www.kaggle.com/scirpus/a-bit-of-gp-clustering
      - X KMeans clustering K=2 as feature
    - https://www.kaggle.com/sudalairajkumar/simple-exploration-baseline-ga-customer-revenue
      - X visit start time
      - X metro
      - X referral path
      - X keyword
    - https://www.kaggle.com/kailex/xgb-for-gstore-1-67
      - X pageviews max country
    - https://www.kaggle.com/kailex/r-eda-for-gstore-xgb
      - X pageviews mean country
      - X visit start time
      - X page views mean city
    - https://www.kaggle.com/prashanththangavel/unique-session-counts-helps-sure-lb-1-6647
      - X unique day/month/weekday session counts
    - https://www.kaggle.com/prashantkikani/rstudio-lgb-single-model-lb1-6607
      - X hit vs view
      - X week of year
      - X max pageview WoY
      - X hit mean pageviews per network domain
      - X mean hits per day
    - self
      - X multiply some of the best features together (including squared)
      - X use the features for both regression and the classification mask
    - Forgot
      - Classification problem (average CR)
      - Check conversion rate by month
      - Check conversion rate by week day
      - Check conversion rate by medium
      - Check conversion rate by source
      - Check conversion rate by device category
      - Check conversion rate by os
      - Check conversion rate by country
      - Check conversion rate by city
      - Check conversion rate by domains
      - Check conversion rate by regions
- Exploration
  - What should be cleaned?
  - % in train/test with 0 revenue
  - two color density plot of distribution of non-zero revenue
  - one variable plots
  - two variable plots
  - Consider adding steps to prepare data based on exploration
- Prepare Data
  - Clean
    - Might be a few duplicates based on sessionId
    - Might need to group "sources" together that are similar.
    - Missing Data
      - Build a baseline (mean/mode) model and LightGBM model to fill in the values for the following:
        - 100 missing page views
        - 69 missing trafficSource.source
        - 1468 missing network country
        - 542491 missing network city  
        - 390915 missing network domain
        - 536056 missing network regions
      - Verify that all these missing values are filled in
      - Fill in the rest of the missing values with mean/mode
  - Upsample to 33% non-zero revenue (Use this for classification, and not yet for regression)
- Spot Check Algorithms
  - Iteratively create a CV and test the CV score against the public leaderboard
  - Try 30 regression algorithms
  - LightGBM CV, and Kaggle submission
- Improve Results
  - Try with/without stratified sampling for the regression
  - stratified binary classification whether nonzero & Regression run as normal.  Modify the regression value to 0 if the classification is class 0.  Compare results with/without classification.
  - From the above two points, choose the preferred answer
  - Quickly skim high scoring kernels
  - If time, check prediction distribution, error analysis, hard examples
  - If time, do course/fine grid search on LightGBM
  - Lastly, Ensemble: maybe H2O AutoML with LightGBM (Compare CV if better with/without h2o?)
- Present Results
  - Plot feature importance for LightGBM
  - List the public leaderboard score
  - Convert to HTML and put on site
  - Add the project tags to the site (new category values)

### Project Tags

- Normalize JSON
- Upsampling
- LightGBM
- Models to fill NA
- Marketing

### Notes

The data is at the session level, but predictions at user level.  Will ignore this until the final scoring.

### Conclusion
