
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse


def main(params):
    user = params.user
    password = params.password        
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'
    
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator = True, chunksize=100000, compression = 'gzip')
    
    # iter through first csv

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        t_end = time()
        df.to_sql(name = table_name, con = engine, if_exists='append')
        print('chunk inserted ..., took %.3f second' % (t_end - t_start))
    
   
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Ingest CSV to postgres')

    # user

    parser.add_argument('--user', help = 'username for postgres')
    parser.add_argument('--password', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'database name for postgres')
    parser.add_argument('--table_name', help = 'table name for postgres')
    parser.add_argument('--url', help = 'url of csv for postgres')
    
    args = parser.parse_args()
    
    main(args)