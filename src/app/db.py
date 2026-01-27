import psycopg2
import pandas as pd

def get_conn():
    return psycopg2.connect(
        host="localhost",
        dbname="weather",
        user="weather_user",
        password="weather_pass",
        port=5432
    )

def fetch_df(query, params=None):
    conn = get_conn()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
