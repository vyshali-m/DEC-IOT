from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
import pandas as pd
import json

app = FastAPI()

# Initialize an empty DataFrame
df = pd.DataFrame(columns=["timestamp", "freeHeapMemory", "networkTrafficVolume", 
                           "packetSize", "responseTime", "errorRate", "powerConsumption"])

# Keep track of WebSocket connections
clients = []

@app.get("/")
async def get():
    # Serve the HTML page
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/endpoint")
async def receive_data(request: Request):
    global df
    data = await request.json()
    
    # Convert the batch data to a DataFrame
    batch_df = pd.DataFrame(data['batch data'])
    
    # Append the new data to the existing DataFrame
    df = pd.concat([df, batch_df], ignore_index=True)
    
    # Send the updated data to all connected WebSocket clients
    for client in clients:
        await client.send_text(df.to_json(orient="records"))
    
    return {"status": "success", "data": data}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except:
        clients.remove(websocket)


#ngrok http --domain=thoroughly-correct-rooster.ngrok-free.app 8000 --scheme http