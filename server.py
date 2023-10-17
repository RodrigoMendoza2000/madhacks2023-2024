from fastapi import FastAPI
from oracleDatabase import OracleDatabase

app = FastAPI()
oracle = OracleDatabase()

@app.get('/')
async def root(keyword, count=30, offset=0, sort_type=0, publish_time=30):
    try:
        oracle.insertTikTok(keyword=keyword, count=count, offset=offset, sort_type=sort_type, publish_time=publish_time)
        return {"message": "successful"}
    except:
        return {"message": "unsuccessful"}