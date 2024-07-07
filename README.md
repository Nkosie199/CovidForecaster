# Pandemic Forecasting

Using data sourced from [https://ourworldindata.org/coronavirus],
this project aims to generate a forecast of new Covid-19 cases in South Africa
for the seven days after the final date of data captured (16th of June 2024).

## Prerequisites
- Python 3.x

________________________________________________________________________________________________________

# Main Task

[forecast_covid.py] forecasts COVID-19 cases for the 7 days after the 16th of June 2024 in South Africa.
It is important to note that the forecasts_covid.py contains the following line: 
```bash
ARIMA(cases_series, order=(p, d, q))
```

which is based on assumptions and ultimately affects the accuracy of the forecast generated. 

Reasons for choosing (5, 1, 0):
- We chose p = 5 to consider the last 5 days' data to predict the current day's new cases.
This period captures short-term dependencies and trends in the data.
- Using d = 1 means that the time series is differenced once.
That is, it accounts for the difference between consecutive observations in the time series.
Differencing helps in removing trends or seasonal patterns, making the series stationary and more suitable for modeling.
- Using q = 0 indicates that there is no moving average component included in the model.
This assumes that the current value of the time series is only influenced by its own past values after differencing.

To install & run:
```bash
pip install requests beautifulsoup4 pandas statsmodels matplotlib
python forecast_covid.py
```

________________________________________________________________________________________________________

# Bonus Task

[ui.py] displays the forecast of COVID-19 cases for the 7 days after the 16th of June 2024 in South Africa.

To install & run:
```bash
pip install flask pandas matplotlib
python ui.py
```
