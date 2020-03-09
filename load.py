import psycopg2
from sql_queries import create_table_queries, drop_table_queries,populate_table_raw_turnstile
import os
import configparser

def connect_database():
    config = configparser.ConfigParser()
    config.read('config/db.cfg')
    pg_info = config['POSTGRES']
    dbname = pg_info['db']
    host = pg_info['host']
    user = pg_info['user']
    password = pg_info['password']

    conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password)
    cur = conn.cursor()
    return cur, conn

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def populate_tables(cur, conn):
    raw_data_path = 'scraper/raw_turnstile_data'
    if not os.path.exists(raw_data_path):
        raise Error("No raw data directory (%s)".format(raw_data_paths))
    
    if not len(os.listdir(raw_data_path)):
        raise Error("No files in data directory to process")

    for file in os.listdir(raw_data_path):
        print("copying", file)
        f = open(raw_data_path + '/' + file)
        cur.copy_expert(populate_table_raw_turnstile, f)
        
    conn.commit()

def main():
    cur, conn = connect_database()
    print("dropping")
    exit()
    drop_tables(cur, conn)
    print("creating")
    create_tables(cur, conn)
    print("populating")
    populate_tables(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
