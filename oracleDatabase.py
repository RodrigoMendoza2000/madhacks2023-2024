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
    
    def updateTranscript(self, transcript_dictionary):
        cursor = self.con.cursor()
        print(transcript_dictionary)
        
        for key, value in transcript_dictionary.items():
            
            query = f"""
            declare
            l_transcript CLOB;
            BEGIN
            l_transcript := {value};
            update video SET transcript = l_transcript WHERE aweme_id = {key};
            
            END;
            """
            print(query)
            try:
                cursor.execute(query)
            except Exception as e:
                print(e)
            self.con.commit()
            print("commited")
            
        cursor.close()

    def insertTikTok(self, keyword, count=30, offset=0, sort_type=0, publish_time=30):
        self.tiktok.search(keyword, count=count, offset=offset,
                           sort_type=sort_type, publish_time=publish_time)
        dictionary = self.tiktok.video_dictionary

        cursor = self.con.cursor()

        list_videos = [str(key)+'.mp4' for key, value in dictionary.items()]
        
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
            
        self.oracle_cloud.create_transcribe_job('pythonoracleapex', 'pythonoracleapex', '', list_videos)
        
        cursor.close()
        
        transcript_dictionary = self.oracle_cloud.process_transcribed_jobs()
        self.updateTranscript(transcript_dictionary=transcript_dictionary)


if __name__ == "__main__":
    oracle = OracleDatabase()
    oracle.insertTikTok(keyword='oracle apex', count=2)
    print(oracle.oracle_cloud.transcriptions_to_be_processed)
    oracle.insertTikTok(keyword='oracle apex', count=2)
