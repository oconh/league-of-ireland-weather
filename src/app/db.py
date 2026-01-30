import os
import psycopg2
import pandas as pd

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "weather"),
        user=os.getenv("DB_USER", "weather_user"),
        password=os.getenv("DB_PASS"),
        port=int(os.getenv("DB_PORT", 5432))
    )

def fetch_df(query, params=None):
    conn = get_conn()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
