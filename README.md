# Introductions API
This is an open API, anyone across the world can share some cool things about themselves! If you don't want to share anything, you can also learn more about others. This was built with **Python** and **FastAPI**. This API allows anyone to create "profiles" with some information they would like to share about themsleves, update that information, and fetch other users profiles. All profiles are password protected and you can change your password in the future after creating a password.

## Cool features
### 1. Password protected profiles
You can create your own profiles and other people wont be able to change it since a password is needed to modify any profile that has already been made.

### 2. Rate limiting with IP
Using FastAPI, rate limiting was built in and only one request is allowed every 3 seconds per IP address.

### 3. JSON storage system
A single JSON file is used to store all profiles after every new profile is created so that the data isn't stored in ram and cleared.

If you want to try this API and maybe learn something new about a random stranger, click [here](https://rp-pi-zero-project.hackclub.app/docs) to see the docs.