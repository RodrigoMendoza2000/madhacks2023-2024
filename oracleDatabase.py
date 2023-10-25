from tikTokAPI import TikTok
import cx_Oracle
import os
from dotenv import load_dotenv
load_dotenv()
from io import BytesIO
import requests
from oracleCloud import OracleCloud

class OracleDatabase:

    def __init__(self):
        self.lib_dir = os.environ.get("LIB_DIR")
        #cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)
        self.con = cx_Oracle.connect(user=os.environ.get("SCHEMA_USERNAME"), password=os.environ.get(
            "SCHEMA_PASSWORD"), dsn=os.environ.get("SCHEMA_DSN"))
        self.tiktok = TikTok()
        self.oracle_cloud = OracleCloud()

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

            query = f"""
                DECLARE
                BEGIN
                INSERT INTO VIDEO_BLOB VALUES ('{key}', empty_blob(), 'video/mp4', '{key}.mp4');
                EXCEPTION WHEN DUP_VAL_ON_INDEX
                THEN NULL;
                END;
            """

            try:
                cursor.execute(query)
            except:
                pass
            self.con.commit()

            select_query = f"""
                SELECT (SELECT URL FROM VIDEO_URL WHERE AWEME_ID = '{key}' AND URL LIKE '%api16%' FETCH FIRST 1 ROWS ONLY) AS video_ur, DOWNLOADED_VIDEO FROM VIDEO_BLOB WHERE aweme_id = '{key}'
                FOR UPDATE

            """
            cursor.execute(select_query)

            cursor_fetch = cursor.fetchall()

            for row in cursor_fetch:
                (url, blob,) = row

                request = requests.get(url=url)
                
                if request.status_code == 200:
                    video_mp4 = request.content
                    
                    print('adding to OCI')
                    self.oracle_cloud.insert_into_bucket(file_stream=video_mp4, name=key)
                    print('added to OCI')
                else:
                    pass

                video_mp4_stream = BytesIO(video_mp4)
                print(len(video_mp4))
                offset = 1
                num_bytes_in_chunk = 65536
                print('adding to blob')
                while True:
                    data = video_mp4_stream.read(num_bytes_in_chunk)
                    if data:
                        blob.write(data, offset)
                    if len(data) < num_bytes_in_chunk:
                        break
                    offset += len(data)
                print('added to blob')

            self.con.commit()
            

        
        cursor.close()


if __name__ == "__main__":
    oracle = OracleDatabase()
    oracle.insertTikTok(keyword='oracle apex', count=1)
