from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)
csv = 'forecast.csv'
png = 'forecast.png'

@app.route('/', methods=['GET'])
def get_forecast():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def show_api():
    forecast_df = pd.read_csv(csv)
    forecast_data = forecast_df.to_dict(orient='records')
    return render_template('./api.html', forecast_data=forecast_data)

# Route to render the chart view
@app.route('/chart', methods=['GET'])
def show_chart():
    forecast_df = pd.read_csv(csv)
    chart_html = forecast_df.to_html(index=False)
    return render_template('./chart.html', table_html=chart_html)

@app.route('/timeseries', methods=['GET'])
def show_timeseries():
    if os.path.exists(png):
        return send_file(png, mimetype='image/png')
    else:
        return "Image file not found."

if __name__ == '__main__':
    app.run(debug=True)
