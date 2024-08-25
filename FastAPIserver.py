from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncpg
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

#DATABASE_URL = "postgresql://postgres.ljkyfydochapfwaqgghg:Supabase2024$@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
# "postgresql://postgres.gxvqfyitftgzusocnxvo:Supabase2024$@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_MIN_CONNECTIONS = os.getenv("DATABASE_MIN_CONNECTIONS")
DATABASE_MAX_CONNECTIONS = os.getenv("DATABASE_MAX_CONNECTIONS")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_db_pool():
    return await asyncpg.create_pool(
        DATABASE_URL,
        min_size=DATABASE_MIN_CONNECTIONS,
        max_size=DATABASE_MAX_CONNECTIONS,
        statement_cache_size=0
    )

@app.on_event("startup")
async def startup_event():
    app.state.db_pool = await get_db_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.db_pool.close()

@app.post("/endpoint")
async def insert_data(request: Request):
    batch_data = await request.json()
    #print(batch_data)
    # data_to_insert = [
    #     (
    #         row['timestamp'],
    #         row['freeHeapMemory'],
    #         row['networkTrafficVolume'],
    #         row['packetSize'],
    #         row['responseTime'],
    #         row['errorRate'],
    #         row['powerConsumption']
    #     )
    #     for row in batch_data["batch data"]
    # ]

    data_to_insert = [
        (
            datetime.now(),
            row['timestamp'],
            row['freeHeapMemory'],
            row['networkTrafficVolume'],
            row['packetSize'],
            row['responseTime'],
            row['errorRate'],
            row['powerConsumption']
        )
        for row in batch_data["batch data"]
    ]

    query = """
        INSERT INTO iot_data (timestamp, device_timestamp, freeHeapMemory, networkTrafficVolume, packetSize, responseTime, errorRate, powerConsumption)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """

    async with app.state.db_pool.acquire() as connection:
        async with connection.transaction():
            try:
                await connection.executemany(query, data_to_insert)
                logger.info("Successfully inserted data")
                return {"server: successfully inserted your records "}
            except Exception as e:
                logger.error(f"Error inserting data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

#ngrok http --domain=thoroughly-correct-rooster.ngrok-free.app 8000 --scheme http
#uvicorn FastAPIserverForArduino:app --reload


# New ngrok
#ngrok http --domain=grand-grown-swine.ngrok-free.app 8000 --scheme http