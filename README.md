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
- visitId: An identifier for this session. This is part of the value usually stored as the _utmb cookie. This is only unique to the user. For a completely unique ID, you should use a combination of fullVisitorId and visitId.
- visitNumber: The session number for this user. If this is the first session, then this is set to 1.
- visitStartTime: The timestamp (expressed as POSIX time).

### Steps

- ETL
  - Use the code from another kernel to normalize the data into a dataframe
  - Missing transactionRevenue means no transaction
  - Features (Give credit for the feature names found on Kernels, won't copy anyone's feature engineering code)
    - https://www.kaggle.com/youhanlee/stratified-sampling-for-regression-lb-1-6595
      - total hits
      - total pageviews
      - trafficSource.source
      - network country
      - network city  
      - month unique user count
      - mean hits per network domain
      - day unique user count
      - network domain
      - network region
      - mean hits per day
      - mean page views per network domain
      - count hits per network domain
      - total new visits
      - var hits per day
    - https://www.kaggle.com/erikbruin/google-analytics-eda-with-screenshots-of-the-app
      - Saturday/Sunday appear to have low sales (Very low conversion rate too)
    - https://www.kaggle.com/nulldata/ga-eda-digital-analytics-h2o-rf-1-86
      - pageviews
      - hits
      - visit number
    - https://www.kaggle.com/prashantkikani/howmuch-train-test-data-are-different
      - browser_category
      - count hits per network domain
      - month unique user count
      - day unique user count
      - sum hits per day
      - var hits per day
    - https://www.kaggle.com/plasticgrammer/customer-revenue-prediction-playground
      - new visits
      - channel grouping referral
      - medium referral
      - sub continent north america
    - https://www.kaggle.com/scirpus/a-bit-of-gp-clustering
      - KMeans clustering K=2 as feature
    - https://www.kaggle.com/sudalairajkumar/simple-exploration-baseline-ga-customer-revenue
      - visit start time
      - metro
      - referral path
      - keyword
    - https://www.kaggle.com/kailex/xgb-for-gstore-1-67
      - pageviews max country
    - https://www.kaggle.com/kailex/r-eda-for-gstore-xgb
      - pageviews mean country
      - visit start time
      - page views mean city
    - https://www.kaggle.com/prashanththangavel/unique-session-counts-helps-sure-lb-1-6647
      - unique day/month/weekday session counts
    - https://www.kaggle.com/prashantkikani/rstudio-lgb-single-model-lb1-6607
      - hit vs view
      - week of year
      - max pageview WoY
      - hit mean pageviews per network domain
      - mean hits per day
    - self
      - multiply some of the best features together (including squared)
      - use the features for both regression and the classification mask
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
- H2O AutoML
- (Add/remove from this list)

### Conclusion
