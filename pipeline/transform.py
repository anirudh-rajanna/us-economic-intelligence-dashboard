import pandas as pd

def transform(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['value', 'date'])
    df = df.drop_duplicates(subset=['date', 'metric'])

    # Pivot to wide format
    wide = df.pivot_table(index='date', columns='metric',
                          values='value', aggfunc='last').reset_index()
    wide = wide.sort_values('date').reset_index(drop=True)

    # Calculate YoY inflation from CPI
    if 'cpi' in wide.columns:
        cpi_monthly = wide[['date', 'cpi']].dropna().sort_values('date').reset_index(drop=True)
        cpi_monthly['inflation_yoy_pct'] = cpi_monthly['cpi'].pct_change(12) * 100
        wide = wide.merge(cpi_monthly[['date', 'inflation_yoy_pct']], on='date', how='left')

    # Recession risk: yield spread < 0 = inverted yield curve
    if 'yield_spread' in wide.columns:
        wide['recession_risk'] = (wide['yield_spread'] < 0).astype(int)

    return wide

if __name__ == '__main__':
    print('=== Running Transform ===')
    fred = pd.read_csv('data/fred_raw.csv')
    bls  = pd.read_csv('data/bls_raw.csv')
    combined = pd.concat([fred, bls], ignore_index=True)
    clean = transform(combined)
    clean.to_csv('data/economic_data.csv', index=False)
    print(f'Done! {len(clean)} rows, {len(clean.columns)} columns')
    print(f'Columns: {list(clean.columns)}')