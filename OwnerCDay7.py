from prefect import task, get_run_logger
import pandas as pd
from sqlalchemy import create_engine
from config import db_config

@task(name="Read Table From MySQL", retries=3, retry_delay_seconds=5)
def read_table(table_name: str) -> pd.DataFrame:
    logger = get_run_logger()

    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    database = db_config["database"]

    try:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")
        df = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
        logger.info(f"✅ Read {len(df)} rows from {table_name}")
        return df

    except Exception as e:
        logger.error(f"❌ READ FAILED table={table_name}. Error: {repr(e)}")
        raise
