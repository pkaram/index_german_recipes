import os
import json
import zipfile
import logging
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

MONTH_MAPPING ={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}

def unzip_file(f):
    with zipfile.ZipFile(f,"r") as zip_ref:
        zip_ref.extractall("./data/")
    logging.info('file unzipped')

def download_data(kaggle_ds):
    with open('./kaggle.json') as json_file:
        json_data = json.load(json_file)
    os.environ['KAGGLE_USERNAME'] = json_data.get('username')
    os.environ['KAGGLE_KEY'] = json_data.get('key')
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(kaggle_ds, path="./data/")
    except Exception as e:
        logging.info('error during auth/download:{e}')
    logging.info('data downloaded')

def keep_most_recent_recipes(df):
    df['Month'] = df.apply(lambda x: MONTH_MAPPING.get(x.Month), axis=1)
    for col in ['Year','Day']:
        df[col]=pd.to_numeric(df[col])
    df['date']=pd.to_datetime(df[['Year','Month','Day']],format='%Y-%m-%d')
    df=df.sort_values('date').drop_duplicates('Url',keep='last')
    df=df.reset_index(drop=True)
    df=df.drop(columns=['Day','Year','Month','Weekday'])
    return df

def load_and_process(file):
    df = pd.read_json(file)
    df = keep_most_recent_recipes(df)
    #define an id column
    df['id']=df.Url.str.extract('(\d+)')
    return df

def doc_generator(df, index_name):
    return [{
        "_index":index_name,
        "_id": df['id'][i],
        "Url": df['Url'][i],
        "Instructions": df['Instructions'][i],
        "Ingredients": df['Ingredients'][i],            
        "Name": df['Name'][i]}
        for i in range(0, len(df))
        ]