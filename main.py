#__IMPORTS__# ------------------------------------------------------
import uvicorn
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

#__GLOBAL_VARIABLES__# ------------------------------------------------------
contentFile = "data.json"
API_KEY = "Hi; hello; how are you?; im great, you?; yeah me too; thats good to hear; so what have you been doing all day?; nothin much;"

#__JSON__# ------------------------------------------------------
if not os.path.exists(contentFile):
    with open(contentFile, "w") as file:
        json.dump({}, file, indent=2,)

#__APP_STUFF__# ------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # customize this to only allow certain domains!
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    title="Introductions API",
    description="An API where anyone and everyone can introduce themselves to other users around the world!"
)

#__POST__# ------------------------------------------------------
@app.post("/profiles")
def create_or_update_profile(user: str, nickname: str, pronouns: str, bio: str, password: str, KEY: str):
    if KEY != API_KEY: #Make sure the api key is valid
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    allProfiles = None
    with open(contentFile, "r") as profiles: #Read what is currently in the profiles file
        allProfiles = json.load(profiles)
    
    if user in allProfiles and password != allProfiles[user]["password"]: #Check if the user is already in the system
        raise HTTPException(status_code=403, detail="Invalid password for profile")
    elif not user in allProfiles: #If the user isnt in the system, we make a profile for them
        newProfile = {
            "Nickname" : nickname,
            "Pronouns" : pronouns,
            "Bio" : bio,
            "password" : password
        }


#__GET__# ------------------------------------------------------
@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/hello")
def hello():
    return {"message": "Hello, RaspAPI!"}


#__PROGRAM__# ------------------------------------------------------
uvicorn.run(app)