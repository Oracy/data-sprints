from airflow.hooks.S3_hook import S3Hook
from shutil import copyfile
from sqlalchemy import (
    create_engine,
    schema
)
import pandas as pd
import numpy as np
import os
import requests
import pathlib
import re


def download_file(**kwargs):
    path = pathlib.Path(__file__).parent.absolute()
    download_path = kwargs["download_path"]
    file_name = kwargs["file_name"]
    url = f'https://s3.amazonaws.com/data-sprints-oracy/{file_name}'
    r = requests.get(url, allow_redirects=True)
    open(f'{path}{download_path}/{file_name}', 'wb').write(r.content)


def is_json(json_file):
    try:
        json_object = pd.read_json(json_file)
        json_object = None
        return True
    except ValueError as e:
        return False


def check_is_json(**kwargs):
    source_path = kwargs["source_path"]
    transform_path = kwargs["transform_path"]
    file_name = kwargs["file_name"]
    path = pathlib.Path(__file__).parent.absolute()
    file_to_check = f'{path}{source_path}/{file_name}'
    file_transformate = f'{path}{transform_path}/{file_name}'
    file_is_json = is_json(file_to_check)
    if file_is_json is not True:
        data = []
        with open(file_to_check) as fp:
            line = fp.readline()
            cnt = 1

            while line:
                row = line.strip()
                data.append(row)
                line = fp.readline()
                cnt += 1

        f = open(file_to_check, 'w')
        for (idx, i) in enumerate(data):
            if idx == 0:
                f.write("[{},".format(i))
            elif idx < len(data)-1:
                f.write("{},".format(i))
            else:
                f.write("{}]".format(i))
        f.close()
        copyfile(file_to_check, file_transformate)
    else:
        copyfile(file_to_check, file_transformate)


def is_csv(csv_file):
    try:
        csv_object = pd.read_csv(csv_file)
        csv_object = None
        return True
    except ValueError as e:
        return False


def check_is_csv(**kwargs):
    source_path = kwargs["source_path"]
    transform_path = kwargs["transform_path"]
    file_name = kwargs["file_name"]
    path = pathlib.Path(__file__).parent.absolute()
    file_to_check = f'{path}{source_path}/{file_name}'
    file_transformate = f'{path}{transform_path}/{file_name}'
    file_is_csv = is_csv(file_to_check)
    if file_is_csv is not True:
        return False
    else:
        copyfile(file_to_check, file_transformate)


def feed_columns(df):
    df['pickup_datetime'] = df['pickup_datetime'].apply(lambda data: re.sub(r'[.].*', '', data))
    df['pickup_datetime'] = df['pickup_datetime'].apply(lambda data: data.replace("T", " "))
    df['dropoff_datetime'] = df['dropoff_datetime'].apply(lambda data: re.sub(r'[.].*', '', data))
    df['dropoff_datetime'] = df['dropoff_datetime'].apply(lambda data: data.replace("T", " "))
    return df


def create_columns(df):
    df["weekday"] = pd.to_datetime(df.pickup_datetime, utc=True).dt.dayofweek
    df['diff_trip_seconds'] = pd.to_datetime(df['dropoff_datetime'],
                                             utc=True) - pd.to_datetime(df['pickup_datetime'],
                                                                        utc=True)
    df['diff_trip_seconds'] = df['diff_trip_seconds']/np.timedelta64(1, 's')
    return df


def to_lower_columns(df):
    # Transform id to lower case
    df = df.select_dtypes(include=['object']).apply(lambda data: data.str.lower())
    return df


def strip_columns(df):
    # Remove espacos em branco sobrando
    df = df.select_dtypes(include=['object']).apply(lambda data: data.str.strip())
    return df


def transform_columns(**kwargs):
    source_path = kwargs["source_path"]
    file_name = kwargs["file_name"]
    path = pathlib.Path(__file__).parent.absolute()
    file_transformate = f'{source_path}/{file_name}'
    file_transformate_to_insert = f'{source_path}/../to_insert/{file_name}'
    df = pd.read_json(f'{path}{file_transformate}')
    df = feed_columns(df)
    df = create_columns(df)
    df = to_lower_columns(df)
    df = strip_coluns(df)
    print(df.head())
    df.to_json(f'{path}{file_transformate_to_insert}')


def check_schema_exists():
    engine = create_engine('postgresql://airflow:airflow@172.18.0.2:5432/airflow')
    if not engine.dialect.has_schema(engine, 'nyc_taxi'):
        engine.execute(schema.CreateSchema('nyc_taxi'))


def insert_df_to_db(**kwargs):
    path = pathlib.Path(__file__).parent.absolute()
    source_path = kwargs["source_path"]
    file_name = kwargs["file_name"]
    pattern = '.csv'
    table_pattern = 'vendor'
    if pattern in file_name:
        df = pd.read_csv(f'{path}{source_path}/{file_name}')
        print(df)
        engine = create_engine('postgresql://airflow:airflow@172.18.0.2:5432/airflow')
        if table_pattern in file_name:
            df.to_sql('vendor', engine, schema='nyc_taxi', if_exists='replace', index=False)
        else:
            df.columns = ['payment_type', 'payment_lookup']
            df = df.iloc[1:]
            df.to_sql('payment', engine, schema='nyc_taxi', if_exists='replace', index=False)
    else:
        df = pd.read_json(f'{path}{source_path}/{file_name}')
        engine = create_engine('postgresql://airflow:airflow@172.18.0.2:5432/airflow')
        print(df)
        df.to_sql(
            'nyctaxi_trips',
            engine,
            schema='nyc_taxi',
            if_exists='append',
            index=False,
            chunksize=100000
        )
