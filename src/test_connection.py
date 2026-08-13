import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

load_dotenv()
password=os.getenv("POSTGRES_PASSWORD")
db_name=os.getenv("POSTGRES_DB")
database_url=f"postgresql://postgres:{password}@localhost:5433/{db_name}"
engine=create_engine(database_url)

with engine.connect() as conn:
    result=conn.execute(text('select 1; '))
    print(result.fetchone())