import cx_Oracle
import os
from dotenv import load_dotenv
load_dotenv()

lib_dir = password=os.environ.get("LIB_DIR")

cx_Oracle.init_oracle_client(lib_dir=lib_dir)

con = cx_Oracle.connect(user=os.environ.get("SCHEMA_USERNAME"), password=os.environ.get("SCHEMA_PASSWORD"), dsn=os.environ.get("SCHEMA_DSN"))

cursor = con.cursor()
cursor.execute("""
        SELECT id FROM TEST

""")
for fname in cursor:
    print("Values:", fname)