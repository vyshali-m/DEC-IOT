from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()


# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model to validate incoming data
class MemoryLog(BaseModel):
    device_id: str
    free_memory: int

@app.post("/log_memory")
async def log_memory(data: MemoryLog):
    try:
        # Insert memory log into the Supabase table
        response = supabase.table('device_memory_logs').insert({
            'device_id': data.device_id,
            'free_memory': data.free_memory
        }).execute()

        if response.get("status_code") == 200:
            return {"message": "Memory log added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add memory log")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))