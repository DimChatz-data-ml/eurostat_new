from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from pyjstat import pyjstat
import polars as pl
import logging


def table_has_data(engine,table_name):
    try:
        with engine.connect() as conn:
            counting=conn.execute(text(f'select count(*) from {table_name}')).scalar()
    except ProgrammingError:
        counting=0
    return counting>0        

def extract_data(url):
    result=pyjstat.Dataset.read(url)
    df_pandas=result.write('dataframe')
    final_df=pl.from_pandas(df_pandas)
    logging.info(f"fetched {final_df.shape[0]} rows ")
    return final_df

def load_data(engine,table_name,final_df):
    with engine.begin() as conn:
        final_df.write_database(table_name=table_name, connection=conn, if_table_exists="fail")
    logging.info(f"Data written to {table_name} table")
