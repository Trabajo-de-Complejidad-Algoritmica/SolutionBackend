import pandas as pd
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.settings import settings

DATABASE_URL = settings.DB_URL

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def load_data():
    with engine.connect() as conn:
        gpi_df = pd.read_sql("SELECT * FROM gpi_data", con=conn)
        cpi_df = pd.read_sql("SELECT * FROM cpi_data", con=conn)
    gpi_df['gpi_inverted'] = (5 - gpi_df['overall_score']) / 4 * 100
    merged_df = pd.merge(gpi_df,cpi_df,left_on='iso3c', right_on='country_code', how='left')
    merged_df['composite_score'] = merged_df[['gpi_inverted', 'cpi_score']].mean(axis=1, skipna=True)
    return gpi_df, cpi_df, merged_df

gpi_df, cpi_df, merged_df = load_data()