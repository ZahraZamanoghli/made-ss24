import os
import requests
import pandas as pd
import sqlite3
from urllib.parse import urlparse

data_urls = {
    "datasource1": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/cei_gsr010?format=SDMX-CSV&compressed=false",
    "datasource2": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/egi_co2_1?format=SDMX-CSV&compressed=false",
}

data_dir = "../data"

GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
BLUE = '\033[34m'
RESET = '\033[0m'

def get_filename_from_url(url):
    return os.path.basename(urlparse(url).path)

def download(url, ds_key):
    response = requests.get(url)
    filename = get_filename_from_url(url)
    file_path = os.path.join(data_dir, f"{ds_key}_{filename}.csv")
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(GREEN + f"Downloaded {url} to {file_path}" + RESET)
    return file_path

def transform(file_path):
    df = pd.read_csv(file_path)
    df.drop(["DATAFLOW", "LAST UPDATE", "freq", "OBS_FLAG"], axis=1, inplace=True)
    print(YELLOW + "Data transformed" + RESET)
    return df

def save(df, db_name, table_name):
    conn = sqlite3.connect(os.path.join(data_dir, db_name))
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(CYAN + f"Data saved to database {db_name} with table name {table_name}" + RESET)
    conn.close()

def main():
    for name, url in data_urls.items():
        file_path = download(url, name)
        df = transform(file_path)
        save(df, "dataset.db", name)

if __name__ == "__main__":
    main()
