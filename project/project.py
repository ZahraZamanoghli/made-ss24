import os
import requests
import pandas as pd
import sqlite3

data_urls = {
    "datasource1": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/cei_gsr010?format=SDMX-CSV&compressed=false",
    "datasource2": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/egi_co2_1?format=SDMX-CSV&compressed=false",
}

data_dir = "../data"

def download(url, filename):
    response = requests.get(url)
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

def transform(file_path):
    df = pd.read_csv(file_path)
    df.drop(["DATAFLOW", "OBS_FLAG"], axis=1, inplace=True)
    return df

def save(df, db_name, table_name):
    conn = sqlite3.connect(os.path.join(data_dir, db_name))
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def main():
    for name, url in data_urls.items():
        file_path = download(url, f"{name}.csv")

        df = transform(file_path)

        save(df, "dataset.db", name)

if __name__ == "__main__":
    main()
