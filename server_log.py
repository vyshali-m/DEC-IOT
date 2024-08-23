from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/endpoint")
async def receive_data(request: Request):
    data = await request.json()
    print(data)
    return {"status": "success", "data": data}
#works
#ngrok http --domain=thoroughly-correct-rooster.ngrok-free.app 8000 --scheme http

#https://2d21-106-51-198-213.ngrok-free/endpoint

#ngrok http --domain=thoroughly-correct-rooster.ngrok-free.app 8000