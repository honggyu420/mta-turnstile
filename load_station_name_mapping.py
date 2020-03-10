import psycopg2
from sql_queries import create_table_queries, drop_table_queries,populate_table_raw_turnstile, transform_table_raw_turnstile
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
    drop_query = "drop table if exists station_name_mapping"
    cur.execute(drop_query)
    conn.commit()


def create_tables(cur, conn):
    create_query = """
    create table if not exists station_name_mapping(
        turnstile varchar,
        gtfs_static varchar
    )
    """
    cur.execute(create_query)
    conn.commit()


def populate_tables(cur, conn):
    raw_data_path = 'data/station_name_mapping.csv'
    
    if not os.path.exists(raw_data_path):
        raise Error("Data file does not exist".format(raw_data_paths))
    
    print("copying", raw_data_path)
    f = open(raw_data_path)
    
    cur.copy_expert("COPY station_name_mapping FROM STDIN DELIMITER ',' CSV HEADER;", f)
    conn.commit()
    
    
def start():
    cur, conn = connect_database()
    
    print("dropping")
    drop_tables(cur, conn)
    
    print("creating")
    create_tables(cur, conn)
    
    print("populating")
    populate_tables(cur, conn)
    
    conn.close()


if __name__ == "__main__":
    start()
