from fastapi import FastAPI
from oracleDatabase import OracleDatabase
import cohere
import os
from dotenv import load_dotenv
from fastapi_utils.tasks import repeat_every
load_dotenv()

app = FastAPI()
oracle = OracleDatabase()
co = cohere.Client(os.environ.get("COHERE_APIKEY"))

@app.get('/tiktok/insertTikTok')
async def root(keyword, count=30, offset=0, sort_type=0, publish_time=30):
    try:
        oracle.insertTikTok(keyword=keyword, count=count, offset=offset, sort_type=sort_type, publish_time=publish_time)
        return {"message": "successful"}
    except Exception as e:
        return {"message": f"{e}"}
    
@app.get('/tiktok/coheregenerate')
async def cohere_generate(prompt):
    try:
        response = co.generate(
            prompt=prompt
        )
        return response[0]
    except Exception as e:
        return {"message": f"{e}"}
    
@app.on_event("startup")
@repeat_every(seconds=60)
def process_transacts():
    oracle.updateTranscript()