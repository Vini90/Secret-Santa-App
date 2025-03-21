import asyncio
import random

from typing import Dict, List

from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


# Initialize FastAPI
app = FastAPI()

# MongoDB Connection
config = dotenv_values(".mongo.env")
MONGO_URI = config["MONGO_URI"]
DB_NAME = config["DB_NAME"]

client = AsyncIOMotorClient(MONGO_URI)
client.get_io_loop = asyncio.get_running_loop
db = client[DB_NAME]
participants_collection = db["participants"]
exchange_collection = db["exchanges"]

# Models
class ParticipantCreate(BaseModel):
    name: str
    email: str
    exclusions: List[str] = []


class ExchangeCreate(BaseModel):
    assignments: Dict[str, str]


# CRUD Operations for Participants
@app.post("/participants/")
async def create_participant(participant: ParticipantCreate):
    existing = await participants_collection.find_one(
        {"email": participant.email}
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Participant already exists"
        )

    participant_dict = participant.model_dump()
    await participants_collection.insert_one(participant_dict)
    return {"message": "Participant added successfully"}


@app.get("/participants/")
async def get_participants():
    participants = await participants_collection.find().to_list(None)
    for p in participants:
        p["_id"] = str(p["_id"])
    return participants


@app.delete("/participants/{email}")
async def delete_participant(email: str):
    result = await participants_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Participant not found"
        )
    return {"message": "Participant deleted successfully"}


# Secret Santa Gift Exchange
@app.post("/exchange/")
async def create_exchange():
    participants = await participants_collection.find().to_list(None)

    if len(participants) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least 2 participants"
        )

    assignments = {}
    available_receivers = participants.copy()

    for giver in participants:
        possible_receivers = [
            r for r in available_receivers
            if r["name"] != giver["name"]
            and r["name"] not in giver["exclusions"]
        ]
        if not possible_receivers:
            raise HTTPException(
                status_code=400,
                detail="No valid gift exchange possible"
            )

        receiver = random.choice(possible_receivers)
        assignments[giver["name"]] = receiver["name"]
        available_receivers.remove(receiver)

    await exchange_collection.insert_one({"assignments": assignments})

    return {"exchange": assignments}


@app.get("/exchange/history")
async def get_exchange_history():
    history = (
        await exchange_collection.find()
        .sort("_id", -1)
        .limit(5)
        .to_list(None)
    )
    for exchange in history:
        exchange["_id"] = str(exchange["_id"])
    return history