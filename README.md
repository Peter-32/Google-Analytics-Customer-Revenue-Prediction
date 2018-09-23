# Google-Analytics-Customer-Revenue-Prediction

### Question

Can we predict the lifetime value of a customer with the provided dataset?

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

### Notes

- Challenges
  - parse the data and normalize it with json https://www.kaggle.com/youhanlee/stratified-sampling-for-regression-lb-1-6595
  - Stratified sampling of 0 values of target https://www.kaggle.com/youhanlee/stratified-sampling-for-regression-lb-1-6595
    - only around 1.27% of sessions led to a transaction
    - Should I convert this to a classification problem, then do a regression on top of all the ones with positive revenue?  I think so.
  - understanding missingness https://www.kaggle.com/mithrillion/finding-useful-information-in-missingness
    - focus on the best features
    - build a model to predict these missing values one model at a time (primarily the most important features)
  - might be a few duplicates based on sessionId
  - Might need to group "sources" together that are similar.


- Notes
  - Missing transactionRevenue means no transaction
  - LightGBM seems to work well
  - Convert project to R if doing well at end
  - Course grain, to fine grain, and understand reasoning for features in each model.
  - Classification problem
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
  - A second classification problem to classify as likely a high/medium/low revenue
  - Lastly a regression problem to classify as the amount (subset) (All this multiple model stuff with regression/classification might be bad because you have less data)
  - Social has many clicks but practically no revenue (Important for classification)
  - Remove the unnecessary to find the solution/problem
  - maybe use fast.ai as part of this
  - Always use an average model to predict unknowns, but you can always build models to attempt to improve this baseline model
  - The more supervised learning problems you think of, the better the overall model.  You build a system that relies on tons of supervised learning, maybe even the same dataset.
  - Ensemble: maybe H2O AutoML, LightGBM, and NN (maybe use someone elses public kernel results as part of ensemble)


- Model
  - Model to predict the value of missing fields, then fill them in: (Choose the most likely classification or numeric?)
    - 100 missing page views
    - 69 missing trafficSource.source
    - 1468 missing network country
    - 542491 missing network city  
    - 390915 missing network domain
    - 536056 missing network regions
  - Classification Model to predict whether there is a conversion (Stratified)
  - Regression problem to predict the amount of the conversion on that subset



  - Consider setting revenue predictions to zero for the regression for the users predicted to be 0 revenue users.
  - best features
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

### Steps

- ETL
  - Use the code included to normalize the data into a dataframe
  - Get all the features listed above
- Spot Check Algorithms
- LightGBM

### Conclusion
