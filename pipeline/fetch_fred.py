import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
fred = Fred(api_key=os.getenv('FRED_API_KEY'))

SERIES = {
    'unemployment_rate': 'UNRATE',
    'cpi':               'CPIAUCSL',
    'gdp':               'GDP',
    'fed_funds_rate':    'FEDFUNDS',
    'nonfarm_payrolls':  'PAYEMS',
    'yield_spread':      'T10Y2Y',
}

def fetch_all(start='2000-01-01'):
    frames = []
    for name, series_id in SERIES.items():
        print(f'  Fetching {name}...')
        s = fred.get_series(series_id, observation_start=start)
        df = s.reset_index()
        df.columns = ['date', 'value']
        df['metric'] = name
        df['source'] = 'FRED'
        df['fetched_at'] = datetime.now()
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

if __name__ == '__main__':
    print('=== Fetching FRED data ===')
    df = fetch_all()
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/fred_raw.csv', index=False)
    print(f'Done! {len(df)} rows saved to data/fred_raw.csv')