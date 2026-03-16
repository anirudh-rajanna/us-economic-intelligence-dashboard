import os, sys, pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(__file__))

from fetch_fred import fetch_all as fetch_fred
from fetch_bls import fetch_all as fetch_bls
from transform import transform
from forecast import forecast_all

def run():
    print(f'\n=== Economic Intelligence Pipeline ===')
    print(f'Started: {datetime.now().strftime("%Y-%m-%d %H:%M")}')

    # 1. Fetch
    print('\n[1/4] Fetching FRED data...')
    fred_df = fetch_fred()

    print('\n[2/4] Fetching BLS data...')
    bls_df = fetch_bls()

    combined = pd.concat([fred_df, bls_df], ignore_index=True)

    # 2. Transform
    print('\n[3/4] Transforming data...')
    clean = transform(combined)
    os.makedirs('output', exist_ok=True)
    clean.to_csv('output/economic_data.csv', index=False)
    print(f'  {len(clean)} rows saved to output/economic_data.csv')

    # 3. Forecast
    print('\n[4/4] Running forecasts...')
    forecasts = forecast_all(clean)
    forecasts.to_csv('output/forecast_results.csv', index=False)
    print(f'  {len(forecasts)} rows saved to output/forecast_results.csv')

    print(f'\n=== Pipeline complete! {datetime.now().strftime("%Y-%m-%d %H:%M")} ===')

if __name__ == '__main__':
    run()