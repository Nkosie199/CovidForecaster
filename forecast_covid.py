import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import csv
from datetime import datetime, timedelta
import os

def load_data_from_csv():
    df = pd.read_csv('./owid-covid-data-south-africa.csv', parse_dates=['date'])
    if 'new_cases' not in df.columns:
        raise ValueError("The CSV file must contain a 'new_cases' column.")
    new_cases_data = df['new_cases'].tolist()
    last_date = df['date'].iloc[-1]
    return new_cases_data, last_date

def forecast_cases(cases_data, last_date, days_ahead=7):
    cases_series = pd.Series(cases_data)
    cases_series.index = pd.date_range(end=last_date, periods=len(cases_data))
    model = ARIMA(cases_series, order=(5, 1, 0))
    fit_model = model.fit()
    forecast = fit_model.forecast(steps=days_ahead)
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
    forecast_series = pd.Series(forecast, index=future_dates)
    return forecast_series

def save_forecast_to_csv(forecast_series, file_name="forecast.csv"):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "new_cases"])
        for date, new_cases in forecast_series.items():
            writer.writerow([date.strftime("%Y-%m-%d"), new_cases])

def plot_forecast(forecast_series, file_name="forecast.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(forecast_series.index, forecast_series.values, label="Forecast")
    plt.title("COVID-19 Cases Forecast")
    plt.xlabel("Date")
    plt.ylabel("New Cases")
    plt.legend()
    plt.grid(True)
    plt.savefig(file_name)
    plt.close()

def main():
    cases_data, last_date = load_data_from_csv()
    forecast_series = forecast_cases(cases_data, last_date)
    save_forecast_to_csv(forecast_series)
    plot_forecast(forecast_series)

if __name__ == "__main__":
    main()
