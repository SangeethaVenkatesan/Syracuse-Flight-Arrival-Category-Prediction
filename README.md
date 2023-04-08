# Syracuse-Flight-Arrival-Category-Prediction

**Problem Description**: United Airlines has direct flights into Syracuse (SYR) from four
cities: Chicago (ORD), Denver (DEN), Newark (EWR), and Washington (IAD). There could
be more than one flight from each of those cities into SYR each day. The goal is to predict
1-4 days in advance if each flight’s arrival time into SYR would be early, on-time, delayed, or severely delayed.

**Data**: One source of data is from the Bureau of Transportation Statistics https://www.transtats.bts.gov/ontime/ but there could be others.

**Additional Data**: You are welcome to read about the factors that cause airline delays. One
factor is weather and there are many sites that provide weather predictions on an hourly basis for the next few days.

**Final Predictions**: a CSV file with an empty column for predicting the
arrival time (`early, on-time, delayed, or severely delayed`). The other columns would be date (April 21-24 to be predicted on April 20), origin airport, and flight number.

**Ground Truth**: This will be based what is posted on the United Airlines website. If the
flight is more than 10 minutes early, we will call it early; if it is within 10 minutes (plus or minus) of the scheduled time, we will call it on-time; if it is more than 10 minutes late but up to 30 minutes late, we will call is late; anything beyond 30 minutes late, we will call severely late. There could be a discrepancy between the above BTS website and United, so if you are using BTS, you may want to calibrate.

**Algorithms**: Machine learning Algorithms (Regression,Classification,Time-series Analysis)

**Team Members**:

1. Sajiah Naqib
2. Sangeetha Venkatesan
3. Anusha Prakash
4. Shubadha SuryaKant Mohite
