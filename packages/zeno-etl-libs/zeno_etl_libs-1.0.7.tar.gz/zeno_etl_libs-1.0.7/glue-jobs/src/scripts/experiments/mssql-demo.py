import argparse
import sys
import os
sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db_mssql import MSSql

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-d', '--data', default=None, type=str, required=False, help="batch size")
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env
logger = get_logger()

mssql = MSSql(connect_via_tunnel=True)
connection = mssql.open_connection()

logger.info(f"info message: {1}")
# query = f""" select * from PorderUPD limit 5;"""
# df = pd.read_sql_query(sql=query, con=connection)
# logger.info(f"df: {df}")

cursor = connection.cursor()
cursor.execute('SELECT TOP 10 * FROM FIFO f')
for row in cursor.fetchall():
    print(row)

mssql.close_connection()
