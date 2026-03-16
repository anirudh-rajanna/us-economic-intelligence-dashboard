import pandas as pd
from prophet import Prophet
import os

METRICS_TO_FORECAST = [
    'unemployment_rate',
    'inflation_yoy_pct',
    'nonfarm_payrolls',
    'fed_funds_rate'
]

def forecast_metric(df, metric, periods=12):
    series = df[['date', metric]].dropna()
    series = series.rename(columns={'date': 'ds', metric: 'y'})
    if len(series) < 12:
        print(f'  Skipping {metric} — insufficient data')
        return None
    model = Prophet(yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False)
    model.fit(series)
    future = model.make_future_dataframe(periods=periods, freq='MS')
    forecast = model.predict(future)
    forecast['metric'] = metric
    forecast['is_forecast'] = forecast['ds'] > series['ds'].max()
    return forecast[['ds', 'metric', 'yhat', 'yhat_lower', 'yhat_upper', 'is_forecast']]

def forecast_all(df):
    results = []
    for metric in METRICS_TO_FORECAST:
        print(f'  Forecasting {metric}...')
        result = forecast_metric(df, metric)
        if result is not None:
            results.append(result)
    return pd.concat(results, ignore_index=True)

if __name__ == '__main__':
    print('=== Running Forecast ===')
    df = pd.read_csv('data/economic_data.csv', parse_dates=['date'])
    forecasts = forecast_all(df)
    os.makedirs('output', exist_ok=True)
    forecasts.to_csv('output/forecast_results.csv', index=False)
    print(f'Done! {len(forecasts)} rows saved to output/forecast_results.csv')