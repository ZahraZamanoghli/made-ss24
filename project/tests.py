import os
import sqlite3
import pandas as pd
from pandas.testing import assert_frame_equal
from project import get_filename_from_url, transform, save, data_urls, data_dir

def setup_module(module):
    global db_path
    db_path = os.path.join(data_dir, "dataset.db")
    global data_sample_1
    global data_sample_2
    data_sample_1 = pd.DataFrame({
    "cons_fp": ['AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC', 'AC'],
    "unit": ['I10', 'I10', 'I10', 'I10', 'I10', 'I10', 'I10', 'I10', 'I10', 'I10'],
    "geo": ['AT', 'AT', 'AT', 'AT', 'AT', 'AT', 'AT', 'AT', 'AT', 'AT'],
    "TIME_PERIOD": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
    "OBS_VALUE": [100.0, 101.0, 97.0, 99.0, 100.0, 102.0, 103.0, 100.0, 103.0, 103.0]
})
    data_sample_2 = pd.DataFrame({
    "indic_env": ['CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP',
                  'CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP', 'CO2_CONS_FP'],
    "unit": ['THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T', 'THS_T'],
    "geo": ['EU27_2020', 'EU27_2020', 'EU27_2020', 'EU27_2020', 'EU27_2020',
            'EU27_2020', 'EU27_2020', 'EU27_2020', 'EU27_2020', 'EU27_2020'],
    "TIME_PERIOD": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
    "OBS_VALUE": [4209578.474, 4129435.641, 3887557.28, 3792652.464, 3672251.241,
                  3620813.949, 3635077.914, 3658779.547, 3698592.403, 3571730.646]
})
    os.makedirs(data_dir, exist_ok=True)

def test_get_filename_from_url():    
    assert get_filename_from_url(data_urls["datasource1"]) == "cei_gsr010"
    assert get_filename_from_url(data_urls["datasource2"]) == "egi_co2_1"

def test_transform():
    sample_csv = os.path.join(data_dir, "datasource1_cei_gsr010.csv")
    expected_columns = ['unit', 'OBS_VALUE']
    
    df = transform(sample_csv)
    
    assert isinstance(df, pd.DataFrame)
    assert set(expected_columns).issubset(set(df.columns))

def test_save():
    data = pd.DataFrame([[1, 2, 3], [3, 4, 5]], columns=['a', 'b', 'c'])
    save(data, 'test_load.db', 'example_table')
    conn = sqlite3.connect(os.path.join(data_dir, 'test_load.db'))
    result = pd.read_sql_query("SELECT * FROM example_table", conn)
    conn.close()
    assert_frame_equal(result, data)

def test_db_exist():
    assert os.path.exists(db_path)

def test_db_tables_exist():
    db_path = os.path.join(data_dir, "dataset.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        for name in data_urls.keys():
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';")
            table_exists = cursor.fetchone() is not None
            assert table_exists
    finally:
        conn.close()

def test_datasource1_data():
    db_path = os.path.join(data_dir, "dataset.db")
    conn = sqlite3.connect(db_path)
    try:
        query = "SELECT * FROM datasource1 LIMIT 10;"
        df = pd.read_sql_query(query, conn)
        assert_frame_equal(df, data_sample_1)
    finally:
        conn.close()

def test_datasource2_data():
    db_path = os.path.join(data_dir, "dataset.db")
    conn = sqlite3.connect(db_path)
    try:
        query = "SELECT * FROM datasource2 LIMIT 10;"
        df = pd.read_sql_query(query, conn)
        assert_frame_equal(df, data_sample_2)
    finally:
        conn.close()