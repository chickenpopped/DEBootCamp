
import os
import pandas as pd
from sqlalchemy import create_engine
import argparse


def main(params):
    user = params.user
    password = params.password        
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/tag/misc/taxi_zone_lookup.csv"
    csv_name = 'output.csv'
    
    if url.endswith('.csv.gz'):
        csv_name = 'zones.csv.gz'
    else:
        csv_name = 'zones.csv'
    
    os.system(f"wget {url} -O {csv_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv(csv_name)
    
    df.to_sql(name =table_name, con = engine)

   
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Ingest CSV to postgres')

    # user

    parser.add_argument('--user', help = 'username for postgres')
    parser.add_argument('--password', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'database name for postgres')
    parser.add_argument('--table_name', help = 'table name for postgres')
    
    args = parser.parse_args()
    
    main(args)