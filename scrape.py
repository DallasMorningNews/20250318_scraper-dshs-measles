import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

os.makedirs('data', exist_ok=True)

dshs_url = 'https://www.dshs.texas.gov/news-alerts/measles-outbreak-2025'

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

r = requests.get(dshs_url, headers=headers)

soup = BeautifulSoup(r.text)

tables = soup.find_all("table")

## Age range
# print(tables[1])
age_df = pd.read_html(str(tables[1]))[0]
age_df.to_csv('data/raw_age-range.csv')
age_df['age_total'] = age_df["0 - 4 years"]+age_df["5 - 17 years"]+age_df["18+ years"]+age_df["Pending"]
age_df["Ages 0-4"] = age_df["0 - 4 years"]/age_df['age_total']
age_df["Ages 5 - 17 years"] = age_df["5 - 17 years"]/age_df['age_total']
age_df["Ages 18+"] = age_df["18+ years"]/age_df['age_total']
age_df["Age unknown"] = age_df["Pending"]/age_df['age_total']
age_df = age_df.T
age_df.columns=['Value']
age_df = age_df.reset_index().rename(columns={'index': 'Category'})
age_df.to_csv('data/parsed-age-range.csv', index=False)

## Vax stats
vax_df = pd.read_html(str(tables[2]))[0]
vax_df = vax_df.T
vax_df.columns = vax_df.iloc[0] 
vax_df = vax_df[1:].reset_index(drop=True) 
vax_df.to_csv('data/raw_vax.csv')
vax_df['vax_total'] = vax_df["Unvaccinated/Unknown"]+vax_df["Vaccinated: 1 dose"]+vax_df["Vaccinated: 2+ doses"]
vax_df["Not vaccinated, or unknown*"] = vax_df["Unvaccinated/Unknown"]/vax_df['vax_total']
vax_df["Vaccinated with only one dose"] = vax_df["Vaccinated: 1 dose"]/vax_df['vax_total']
vax_df["Vaccinated with at least two doses"] = vax_df["Vaccinated: 2+ doses"]/vax_df['vax_total']
vax_df = vax_df.T
vax_df.columns=['Value']
vax_df = vax_df.reset_index().rename(columns={'index': 'Test'})
vax_df = vax_df.rename(columns={0:"Category"})
vax_df.to_csv('data/parsed_vax.csv', index=False)

cdf = pd.concat([age_df, vax_df])
cdf.to_csv('data/parsed_both.csv', index=False)