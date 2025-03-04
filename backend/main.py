from fastapi import FastAPI
from fastapi.responses import FileResponse
import asyncio
import json
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, FollowEvent

app = FastAPI()
clients = {}

@app.get("/api/start-tracking")
async def start_tracking(unique_id: str):
    if unique_id in clients:
        return {"success": True, "message": "Tracking già avviato"}
    
    client = TikTokLiveClient(unique_id=unique_id)
    clients[unique_id] = client

    @client.on(ConnectEvent)
    async def on_connect(event: ConnectEvent):
        print(f"Connesso a {event.unique_id}")

    @client.on(FollowEvent)
    async def on_follow(event: FollowEvent):
        data = {"unique_id": event.user.unique_id, "profile_pic": event.user.profile_picture.url}
        with open(f"data_{unique_id}.json", "w") as f:
            json.dump(data, f)

    asyncio.create_task(client.start())
    return {"success": True, "message": "Tracking avviato"}

@app.get("/api/status")
async def get_status(unique_id: str):
    try:
        with open(f"data_{unique_id}.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"unique_id": unique_id, "profile_pic": "https://via.placeholder.com/100"}

@app.get("/api/download")
async def download_data(unique_id: str):
    file_path = f"data_{unique_id}.json"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"{unique_id}_data.json")
    return {"error": "File non trovato"}
