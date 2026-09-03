# MetroPulse Metric Dictionary

## Trip-Level Metrics
- trip_duration_minutes: dropoff_datetime minus pickup_datetime, in minutes
- trip_distance: distance traveled per the taxi meter, in miles
- fare_amount: base metered fare, in USD, before extras/tax/tip
- total_amount: full charged amount including fare, extras, tax, tip, tolls, surcharges
- tip_amount: tip charged on card payments only (cash tips are not captured in this data source)
- tip_percentage: tip_amount divided by fare_amount, expressed as a percentage
- fare_per_mile: fare_amount divided by trip_distance, used to detect pricing anomalies
- pickup_hour: hour of day (0-23) extracted from pickup_datetime
- pickup_day_of_week: day of week (0=Sunday to 6=Saturday) extracted from pickup_datetime
- pickup_borough / dropoff_borough: NYC borough of the pickup/dropoff zone, joined from the official taxi zone lookup table
- rate_code_id: fare type code (1=standard, 2=JFK, 3=Newark, 4=Nassau/Westchester, 5=negotiated, 6=group ride)
- payment_type: 1=credit card, 2=cash, 3=no charge, 4=dispute

## Daily-Level Metrics
- total_trips: count of trips with a given pickup_date
- total_revenue: sum of total_amount for a given day
- avg_trip_distance / avg_trip_duration_minutes / avg_tip_percentage: daily averages across all trips that day
- total_subway_ridership: sum of subway ridership across all NYC stations for a given day
- is_precipitation_day: TRUE if rain_mm > 0 OR snowfall_cm > 0 on that day, else FALSE

## Statistical Terms Used
- 95% Confidence Interval (CI): the range within which we are 95% confident the true population value lies, given our sample
- Correlation: a measure (-1 to 1) of linear association between two variables; a correlation does NOT imply that one causes the other
- Statistical significance: when a 95% CI for a difference between two groups excludes 0, we say the difference is statistically significant at that level

## A Note on Skewed Metrics
Fare and duration data are right-skewed (most trips are short/cheap, with a
long tail of expensive/long trips). Where this matters, medians and
percentage/rate-based views are more representative than simple means - for
example, median fare ($13.50) is meaningfully lower than mean fare ($19.69)
in this dataset, reflecting that skew. Mean is used for direct dollar-impact
metrics (e.g., total/average revenue), while proportions and rates are used
for behavioral comparisons.