from sqlalchemy import create_engine,text
engine=create_engine("postgresql://postgres:devpass@localhost:5433/eurostat")

with engine.connect() as conn:
    result=conn.execute(text('select 1; '))
    print(result.fetchone())