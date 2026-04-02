import os
import pandas as pd
from sqlalchemy import create_engine


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER', 'weather_user')}:"
        f"{os.getenv('DB_PASS', 'weather_pass')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'weather')}"
    )


def read_table(table_name):
    return pd.read_sql_table(table_name, get_engine())
