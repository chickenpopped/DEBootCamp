
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
    data_table = params.data_table
    zone_table = params.zone_table
    data_url = params.data_url
    zone_url = params.zone_url
    
    if zone_url.endswith('.csv.gz'):
        zone_name = 'zones.csv.gz'
    else:
        zone_name = 'zones.csv'
    
    os.system(f"wget {zone_url} -O {zone_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    zone_df = pd.read_csv(zone_name)
    zone_df.to_sql(name=zone_table, con=engine)
    
    
    if data_url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {data_url} -O {csv_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator = True, chunksize=100000, compression = 'gzip')
    
    # iter through first csv

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            t_end = time()
            df.to_sql(name = data_table, con = engine, if_exists='append')
            print('chunk inserted ..., took %.3f second' % (t_end - t_start))
            
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
    
   
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Ingest CSV to postgres')

    # user

    parser.add_argument('--user', help = 'username for postgres')
    parser.add_argument('--password', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'database name for postgres')
    parser.add_argument('--data_table', help = 'data table name for postgres')
    parser.add_argument('--zone_table', help = 'zone table name for postgres')
    parser.add_argument('--data_url', help = 'url of csv for postgres')
    parser.add_argument('--zone_url', help = 'url of csv for postgres')
    
    args = parser.parse_args()

    print("Parsed arguments:", args)
    
    main(args)