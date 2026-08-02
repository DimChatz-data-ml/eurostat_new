import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine
from common import table_has_data, extract_data, load_data


logging.basicConfig(level=logging.INFO)
load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
database_url = f"postgresql://postgres:{password}@localhost:5433/{db_name}"
engine = create_engine(database_url)


url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_ainr?format=JSON&lang=EN&geo=DE&geo=EL&geo=PL&sinceTimePeriod=2010&coicop18=TOTAL&unit=RCH_A_AVG'

already_exists=table_has_data(engine,table_name='raw_inflation')
if already_exists:
    logging.info('we have data,skip that part')
else:
    final_df=extract_data(url)
    load_data(engine, table_name='raw_inflation', df=final_df)
