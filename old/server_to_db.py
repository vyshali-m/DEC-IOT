from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncpg
import asyncio

app = FastAPI()
DATABASE_URL = "postgresql://postgres.ljkyfydochapfwaqgghg:Supabase2024$@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
DATABASE_MIN_CONNECTIONS = 3
DATABASE_MAX_CONNECTIONS = 10
async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL, 
                                     min_size = DATABASE_MIN_CONNECTIONS,
                                     max_size = DATABASE_MAX_CONNECTIONS,
                                     statement_cache_size=0)

@app.on_event("startup")
async def startup_event():
    app.state.db_pool = await get_db_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.db_pool.close()

async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    return conn

conn = get_db_connection()


@app.post("/endpoint")
async def insert_data(request: Request):
    batch_data = await request.json()
    #print(batch_data["batch data"])
    async with app.state.db_pool.acquire() as connection:
        async with connection.transaction(): # Start a transaction
            try:
                for row in batch_data["batch data"]:
                    query = "INSERT INTO iot_data (timestamp, freeHeapMemory, networkTrafficVolume, packetSize, responseTime, errorRate, powerConsumption) VALUES ($1, $2, $3, $4, $5, $6, $7);"
                    result = await connection.execute(query,
                                                    row['timestamp'],
                                                    row['freeHeapMemory'],
                                                    row['networkTrafficVolume'],
                                                    row['packetSize'],
                                                    row['responseTime'],
                                                    row['errorRate'],
                                                    row['powerConsumption'])
                    print(result)
                    print("success : row updated successfully")
            
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail=str(e))
                # Rollback is handled automatically if the transaction fails

    return {"message": "Data inserted successfully"}

#ngrok http --domain=thoroughly-correct-rooster.ngrok-free.app 8000 --scheme http
# @app.post("/endpoint")
# async def insert_data(request: Request):
#     batch_data = await request.json()
#     #print(batch_data["batch data"])
    
#     try:
#         for row in batch_data["batch data"]:
#             await conn.execute("""INSERT INTO iot_data (timestamp, freeHeapMemory, networkTrafficVolume, packetSize, responseTime, errorRate, powerConsumption) 
#                             VALUES ($1, $2, $3, $4, $5, $6, $7)""",row['timestamp'], row['freeHeapMemory'], row['networkTrafficVolume'],row['packetSize'],row['responseTime'], row['errorRate'], row['powerConsumption'],)
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         await conn.close()
    
#     return {"message": "Data inserted successfully"}
