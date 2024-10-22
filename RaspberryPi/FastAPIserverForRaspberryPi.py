from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncpg
import logging
from datetime import datetime
import json

app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://postgres.gxvqfyitftgzusocnxvo:Supabase2024$@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
DATABASE_MIN_CONNECTIONS = 3
DATABASE_MAX_CONNECTIONS = 10

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
    
    data_to_insert = [
        (
            datetime.now(),
            datetime.strptime(row["device_time"], "%Y-%m-%d %H:%M:%S"),
            row["cpu_usage"],
            row["free_memory"],
            row["packets_recv"],
            row["err_in"],
            row["drop_in"],
            row["cpu_temperature"]
        )
        for row in batch_data["batch data"]
    ]

    query = """
        INSERT INTO rpi_iot_data (timestamp, devicetimestamp, cpusage, freememory, packetsrecv, errin, dropin, cputemperature)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """

    async with app.state.db_pool.acquire() as connection:
        async with connection.transaction():
            try:
                await connection.executemany(query, data_to_insert)
                logger.info("Successfully inserted data")
                return {"message": "Successfully inserted your records"}
            except Exception as e:
                logger.error(f"Error inserting data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

# Commands to run the server
# uvicorn FastAPIserverForRaspberryPi:app --reload

# ngrok http --domain=grand-grown-swine.ngrok-free.app 8000 --scheme http

