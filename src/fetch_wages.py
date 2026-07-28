import os
import requests
from dotenv import load_dotenv
from pyjstat import pyjstat
import polars as pl
import logging
from sqlalchemy import create_engine


logging.basicConfig(level=logging.INFO)
load_dotenv()

url='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_fte?format=JSON&lang=EN&geo=DE&geo=EL&geo=PL&sinceTimePeriod=2010'

result=pyjstat.Dataset.read(url)
df_pandas=result.write('dataframe')
final_df=pl.from_pandas(df_pandas)


logging.info(f"fetched wages data: {final_df.shape[0]} rows ")

password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
database_url = f"postgresql://postgres:{password}@localhost:5433/{db_name}"


engine = create_engine(database_url)
final_df.write_database(table_name="raw_wages", connection=engine, if_table_exists="replace")
logging.info("Data written to raw_wages table")

