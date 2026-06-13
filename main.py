#__IMPORTS__# ------------------------------------------------------
import uvicorn
import os
import json
import time
import random
from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

#__GLOBAL_VARIABLES__# ------------------------------------------------------
contentFile = "data.json"
rateLimitIps = {}
rateLimit = 3
API_KEY = "Hi; hello; how are you?; im great, you?; yeah me too; thats good to hear; so what have you been doing all day?; nothin much;"

#__JSON__# ------------------------------------------------------
if not os.path.exists(contentFile):
    with open(contentFile, "w") as file:
        json.dump({}, file, indent=2)

#__APP_STUFF__# ------------------------------------------------------

app = FastAPI(
    title="Introductions API",
    description=f'''An API where anyone and everyone can introduce themselves to other users around the world!\n\n
    KEY: {API_KEY}
    '''
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # customize this to only allow certain domains!
    allow_methods=["*"],
    allow_headers=["*"],
)

#__FUNCTIONS__# ------------------------------------------------------

def dumpJson(content):
    with open(contentFile, "w") as file:
        json.dump(content, file, indent=2)

def checkKey(key):
    if key != API_KEY: #Make sure the api key is valid
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
def getAllProfiles():
    allProfiles = None
    with open(contentFile, "r") as profiles: #Read what is in the profiles file
        allProfiles = json.load(profiles)

    return allProfiles

def lookForProfile(user):
    allProfiles = getAllProfiles()
    
    if user in allProfiles:
        return True, allProfiles[user]
    else:
        return False, {}
    
def getPublicProfiles():
    allProfiles = getAllProfiles()
    publicProfiles = {}
    
    for i, v in allProfiles.items():
        publicProfiles[i] = {
            "User" : i,
            "Nickname" : v["Nickname"],
            "Pronouns" : v["Pronouns"],
            "Bio" : v["Bio"]
        }
    
    return publicProfiles
    
#__RATELIMIT__# ------------------------------------------------------

def getIp(request: Request):
    forwarded = request.headers.get("X-Forwarded-For")

    if forwarded:
        return forwarded.split(",")[0].strip() #cleans string to good ip
    
    return request.client.host
    

def checkRateLimit(ip: str):
    limit = False
    oldIps = []
    currentTime = time.time()

    if ip in rateLimitIps: #check if the ip should be rate limited
        lastTime = rateLimitIps[ip]

        if currentTime - lastTime < rateLimit:
            limit = True
    else:
        rateLimitIps[ip] = time.time()

    for i, v in rateLimitIps.items(): #find any old rate limit data that isnt needed
        if currentTime - v > rateLimit:
            oldIps.append(i)

    for v in oldIps: #clean any old rate limit data that isnt needed
        del rateLimitIps[v]

    if limit:
        raise HTTPException(status_code=429, detail="Too many requests!")
    
    return

#__POST__# ------------------------------------------------------
@app.post("/profiles")
def create_or_update_profile(
    user: str = Query(..., example="Nicholas"),
    password: str = Query(..., example="password1234"),
    KEY: str = Query(..., example="Hi; hello; how are you?; im great, you?; yeah me too; thats good to hear; so what have you been doing all day?; nothin much;"),
    nickname: str = Query("", example="Nick"),
    pronouns: str = Query("", example="they/them"),
    bio: str = Query("", example="Hello, i like painting!"),
    newPassword: str = Query("", example="If you want to reset your password and you already have a profile, put your new password you want here!"),
    Ip: str = Depends(getIp)
    ):

    checkKey(KEY)
    checkRateLimit(Ip)

    allProfiles = getAllProfiles()
    
    if user in allProfiles and password != allProfiles[user]["password"]: #Check if the user is already in the system
        raise HTTPException(status_code=403, detail="Invalid password for profile")
    elif user in allProfiles and password == allProfiles[user]["password"]: #if the user has a profile already and wants to update it, check if the password is correct and update it if it is
        profile = allProfiles[user]

        if nickname != profile["Nickname"] and nickname != None and nickname != "":
            profile["Nickname"] = nickname
        if pronouns != profile["Pronouns"] and pronouns != None and pronouns != "":
            profile["Pronouns"] = pronouns
        if bio != profile["Bio"] and bio != None and bio != "":
            profile["Bio"] = bio
        if newPassword != profile["password"] and newPassword != None and newPassword != "":
            profile["password"] = newPassword
    elif not user in allProfiles: #If the user isnt in the system, we make a profile for them
        newProfile = { #make this new profile
            "Nickname" : nickname,
            "Pronouns" : pronouns,
            "Bio" : bio,
            "password" : password
        }
        
        allProfiles[user] = newProfile #add this new profile we just made into the main file
    
    dumpJson(allProfiles)

    return {
        "Status" : True,
        "Details" : "Profile created/updated"
    }


#__GET__# ------------------------------------------------------
@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/allProfiles")
def get_all_profiles(KEY: str, Ip: str = Depends(getIp)):
    checkKey(KEY)
    checkRateLimit(Ip)

    publicProfiles = getPublicProfiles()

    return publicProfiles

@app.get("/randomProfile")
def get_random_profile(Ip: str = Depends(getIp)):
    checkRateLimit(Ip)

    allProfiles = getAllProfiles()

    if len(allProfiles) > 0:
        randProfile = random.choice(list(allProfiles.keys()))
        publicProfiles = getPublicProfiles()

        if randProfile in publicProfiles.keys():
            return publicProfiles[randProfile]
    
        raise HTTPException(status_code=404, detail="Profile not found")
    
    raise HTTPException(status_code=404, detail="No profiles yet")

@app.get("/profiles/{user}")
def get_specific_profile(user: str, KEY: str, Ip: str = Depends(getIp)):
    checkKey(KEY)
    checkRateLimit(Ip)

    hasProfile, profile = lookForProfile(user)

    if hasProfile:
        publicProfile = {
            "User" : user,
            "Nickname" : profile["Nickname"],
            "Pronouns" : profile["Pronouns"],
            "Bio" : profile["Bio"]
        }

        return publicProfile
    else:
        raise HTTPException(status_code=404, detail="User does not exist")


@app.get("/ping")
def ping(Ip: str = Depends(getIp)):
    checkRateLimit(Ip)

    return {"message": "Success"}


#__PROGRAM__# ------------------------------------------------------

uvicorn.run(app, host="0.0.0.0")