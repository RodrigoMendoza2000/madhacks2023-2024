from tikTokAPI import TikTok
import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()
from io import BytesIO
import requests
from oracleCloud import OracleCloud
from cohereAPI import CohereAPI


class OracleDatabase:
    def __init__(self):
        self.lib_dir = os.environ.get("LIB_DIR")
        # cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)
        self.con = cx_Oracle.connect(
            user=os.environ.get("SCHEMA_USERNAME"),
            password=os.environ.get("SCHEMA_PASSWORD"),
            dsn=os.environ.get("SCHEMA_DSN"),
        )
        self.tiktok = TikTok()
        self.oracle_cloud = OracleCloud()
        self.cohere_api = CohereAPI()


    def insert_topics_summary(self):
        to_insert = self.cohere_api.to_process
        to_be_eliminated = []
        for key, value in to_insert.items():
            print(f"insert topics summary key: {key}, value: {value}")
            if value["topics"] == 0:
                try:
                    print("")
                    self.insert_topics(key, value["transcript"])
                except Exception as e:
                    print(e)
                    break
                else:
                    value["topics"] = 1
            if value["summary"] == 0:
                if len(value["transcript"]) >= 250:
                    try:
                        self.insert_summary(key, value["transcript"])
                    except Exception as e:
                        print(e)
                        break
                    else:
                        value["summary"] = 1
                else:
                    value["summary"] = 1
            if value["topics"] == 1 and value["summary"] == 1:
                to_be_eliminated.append(key)

        for i in to_be_eliminated:
            to_insert.pop(i)


    def insert_topics(self, aweme_id, prompt):
        cursor = self.con.cursor()
        print(f"insert topics prompt: {prompt}")
        try:
            topic_list = self.cohere_api.get_topics(prompt)
            print(f"insert topic topic list: {topic_list}")
        except:
            cursor.close()
            raise Exception("Couldnt get API")


        try:
            for topic in topic_list:
                query = f"""
                    INSERT INTO AWEME_TOPICS VALUES (:aweme_id, :topic)
                """
                try:
                    cursor.execute(query, aweme_id = aweme_id, topic=topic)
                except Exception as e:
                    print(e)
                self.con.commit()
                print("commited topic")
        except Exception as e:
            print(e)
            cursor.close()
            raise Exception("Couldnt insert into database")

        

    def insert_summary(self, aweme_id, transcript):
        cursor = self.con.cursor()
        try:
            #print(f"insert summary prompt: {transcript}")
            summary = self.cohere_api.get_summary(transcript)
            #print(f"insert summary summary: {summary}")
        except:
            cursor.close()
            raise Exception("Couldnt get API")
        
        query = f"""
            UPDATE video SET summary = :summary WHERE aweme_id = :aweme_id
        """
        try:
            cursor.execute(query, summary = summary, aweme_id=aweme_id)
            print("commited video summary")
        except Exception as e:
            cursor.close()
            print(e)
            raise Exception("Couldnt insert into database")
        else:
            
            self.con.commit()
        cursor.close()

    # get the dictionary of transcripts from OracleCloud class and update the table in the DB
    def updateTranscript(self):
        cursor = self.con.cursor()
        
        transcript_dictionary = self.oracle_cloud.process_transcribed_jobs()

        

        for key, value in transcript_dictionary.items():
            query = f"""
            declare
            l_transcript CLOB;
            BEGIN
            l_transcript := :transcript;
            update video SET transcript = l_transcript WHERE aweme_id = {key};
            
            END;
            """
            try:
                cursor.execute(query, transcript=value)
                print(f"len of transcript: {len(value)}")
                # If the transcript is greater than 30 characters
                if len(value) > 30:
                    self.cohere_api.to_process[key] = {"transcript": value, "topics": 0, "summary": 0}
            except Exception as e:
                print(e)
            self.con.commit()
            print("commited  transcript")

        cursor.close()

    def insert_duality_view(self, value):
        cursor = self.con.cursor()
        #value = str(value).replace("'", "''")
        # Insert the data in the duality view
        query = f"""
            
            DECLARE full_text CLOB;

            BEGIN
                full_text := :value;

            BEGIN
                INSERT INTO aweme_dv VALUES (full_text);
            EXCEPTION WHEN DUP_VAL_ON_INDEX
            THEN NULL;
            END;
            END;

        """

        try:
            cursor.execute(query, value=value)
            print('commited DV')
        except Exception as e:
            print(e)
        self.con.commit()
        cursor.close()

    def insert_empty_blob(self, key):
        cursor = self.con.cursor()
        # Add empty blob to video_blob to be able to update it later
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
        cursor.close()

    def insert_video_blob(self, key):
        cursor = self.con.cursor()

        select_query = f"""
                        SELECT (SELECT URL FROM VIDEO_URL WHERE AWEME_ID = '{key}' AND URL LIKE '%api16%' FETCH FIRST 1 ROWS ONLY) AS video_ur, DOWNLOADED_VIDEO FROM VIDEO_BLOB WHERE aweme_id = '{key}'
                        FOR UPDATE

                    """
        cursor.execute(select_query)

        cursor_fetch = cursor.fetchall()

        for row in cursor_fetch:
            (
                url,
                blob,
            ) = row

            request = requests.get(url=url)

            if request.status_code == 200:
                video_mp4 = request.content

                print("adding to OCI")
                self.oracle_cloud.insert_into_bucket(file_stream=video_mp4, name=key)
                print("added to OCI")
            else:
                pass

            video_mp4_stream = BytesIO(video_mp4)
            print(len(video_mp4))
            offset = 1
            num_bytes_in_chunk = 65536
            print("adding to blob")
            while True:
                data = video_mp4_stream.read(num_bytes_in_chunk)
                if data:
                    blob.write(data, offset)
                if len(data) < num_bytes_in_chunk:
                    break
                offset += len(data)
            print("added to blob")

        self.con.commit()
        cursor.close()

    # Create the transcription jobs from the videos extracted
    def add_transcriptions(self, list_videos):
        self.oracle_cloud.create_transcribe_job(
            "pythonoracleapex", "pythonoracleapex", "", list_videos
        )


    def insertTikTok(self, keyword, count=30, offset=0, sort_type=0, publish_time=30):
        self.tiktok.search(
            keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
        )
        dictionary = self.tiktok.video_dictionary

        # list of videos to create the transcription job
        list_videos = [str(key) + ".mp4" for key, value in dictionary.items()]

        for key, value in dictionary.items():
            self.insert_duality_view(value=value)

            self.insert_empty_blob(key=key)

            self.insert_video_blob(key=key)

        self.add_transcriptions(list_videos=list_videos)


if __name__ == "__main__":
    oracle = OracleDatabase()
    oracle.insertTikTok(keyword="oracle apex", count=2)
    print(oracle.oracle_cloud.transcriptions_to_be_processed)
    oracle.insertTikTok(keyword="oracle apex", count=2)
