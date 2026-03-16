import os, requests, pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv('BLS_API_KEY')

SERIES = {
    'unemployment_bls':         'LNS14000000',
    'nonfarm_employment_bls':   'CES0000000001',
    'labor_participation_rate': 'LNS11300000',
}

def fetch_all(start_year=2000, end_year=2026):
    headers = {'Content-type': 'application/json'}
    payload = {
        'seriesid': list(SERIES.values()),
        'startyear': str(start_year),
        'endyear': str(end_year),
        'registrationkey': API_KEY
    }
    print('  Calling BLS API...')
    r = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/',
                      json=payload, headers=headers)
    data = r.json()

    if data.get('status') != 'REQUEST_SUCCEEDED':
        print(f'BLS API error: {data.get("message")}')
        return pd.DataFrame()

    id_to_name = {v: k for k, v in SERIES.items()}
    frames = []
    for series in data['Results']['series']:
        name = id_to_name[series['seriesID']]
        print(f'  Processing {name}...')
        rows = [{'date': f"{d['year']}-{d['period'].replace('M','').zfill(2)}-01",
                 'value': float(d['value']),
                 'metric': name,
                 'source': 'BLS',
                 'fetched_at': datetime.now()}
                for d in series['data']]
        frames.append(pd.DataFrame(rows))
    return pd.concat(frames, ignore_index=True)

if __name__ == '__main__':
    print('=== Fetching BLS data ===')
    df = fetch_all()
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/bls_raw.csv', index=False)
    print(f'Done! {len(df)} rows saved to data/bls_raw.csv')