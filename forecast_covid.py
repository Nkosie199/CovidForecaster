import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import csv
from datetime import datetime, timedelta
import os
import re
import json
import warnings
warnings.filterwarnings("ignore")

# Fetch data from local csv to test
def load_data_from_csv():
    df = pd.read_csv('./docs/owid-covid-data-south-africa.csv', parse_dates=['date'])
    if 'new_cases' not in df.columns:
        raise ValueError("The CSV file must contain a 'new_cases' column.")
    new_cases_data = df['new_cases'].tolist()
    end_date = df['date'].iloc[-1]
    return new_cases_data, end_date

def load_data_from_url():
    url = 'https://www.worldometers.info/coronavirus/country/south-africa/'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', string=re.compile('graph-cases-daily'))
    if not script_tag:
        raise ValueError("Script tag containing Highcharts data not found.")
    script_content = script_tag.string
    categories_pattern = r'categories:\s*\[(.*?)\]'
    data_pattern = r'data:\s*\[(.*?)\]'
    categories_match = re.search(categories_pattern, script_content, re.DOTALL)
    data_match = re.search(data_pattern, script_content, re.DOTALL)
    if categories_match and data_match:
        categories_raw = categories_match.group(1).strip()
        data_raw = data_match.group(1).strip()
        dates = re.findall(r'"(.*?)"', categories_raw)
        converted_dates = []
        for date_str in dates:
            date_obj = datetime.strptime(date_str, "%b %d, %Y")
            converted_dates.append(date_obj.strftime("%Y-%m-%d"))
        new_cases = []
        for item in data_raw.split(','):
            item = item.strip()
            if item != 'null':
                new_cases.append(int(item))
    else:
        print("No match found.")
        return
    len_new_cases = len(new_cases)
    dates_trimmed = converted_dates[:len_new_cases]
    new_cases_data = new_cases
    end_date = datetime.strptime(dates_trimmed[-1], "%Y-%m-%d")
    return new_cases_data, end_date

def forecast_cases(cases_data, start_date, end_date, days_ahead=7):
    cases_series = pd.Series(cases_data)
    date_range = pd.date_range(end=end_date, periods=len(cases_data))
    cases_series.index = date_range
    if start_date not in cases_series.index:
        raise ValueError(f"The provided start_date {start_date.strftime('%Y-%m-%d')} is not within the range of the series")
    if cases_series.index[-1] != end_date:
        raise ValueError(f"The provided end_date {last_date.strftime('%Y-%m-%d')} does not match the last date in the series {cases_series.index[-1].strftime('%Y-%m-%d')}")
    truncated_series = cases_series.loc[:start_date]
    print(truncated_series)
    model = ARIMA(truncated_series, order=(5, 1, 3))
    fit_model = model.fit()
    forecast = fit_model.forecast(steps=days_ahead)
    future_dates = [start_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
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
    start_date = datetime.strptime('2022-06-14', "%Y-%m-%d")
    print("start_date:", start_date)
    cases_data, end_date = load_data_from_url() # Fetch data from worldometers using scraping
    forecast_series = forecast_cases(cases_data, start_date, end_date)
    save_forecast_to_csv(forecast_series)
    plot_forecast(forecast_series)

if __name__ == "__main__":
    main()
