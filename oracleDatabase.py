from tikTokAPI import TikTok
import cx_Oracle
import os
from dotenv import load_dotenv
load_dotenv()


class OracleDatabase:

    def __init__(self):
        self.lib_dir = os.environ.get("LIB_DIR")
        #cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)
        self.con = cx_Oracle.connect(user=os.environ.get("SCHEMA_USERNAME"), password=os.environ.get(
            "SCHEMA_PASSWORD"), dsn=os.environ.get("SCHEMA_DSN"))
        self.tiktok = TikTok()

    def insertTikTok(self, keyword, count=30, offset=0, sort_type=0, publish_time=30):
        self.tiktok.search(keyword, count=count, offset=offset,
                           sort_type=sort_type, publish_time=publish_time)
        dictionary = self.tiktok.video_dictionary

        cursor = self.con.cursor()

        for key, value in dictionary.items():
            value = str(value).replace("'", "''")
            query = f"""
                
                DECLARE full_text CLOB;

                BEGIN
                    full_text := '{value}';

                BEGIN
                    INSERT INTO aweme_dv VALUES (full_text);
                EXCEPTION WHEN DUP_VAL_ON_INDEX
                THEN NULL;
                END;
                END;

            """

            try:
                cursor.execute(query)
            except:
                pass
            self.con.commit()
        
        cursor.close()


if __name__ == "__main__":
    oracle = OracleDatabase()
    oracle.insertTikTok(keyword='water park', count=10)
