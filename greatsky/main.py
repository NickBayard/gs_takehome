from fastapi import FastAPI, Response, status

from greatsky.routers import devices
from greatsky.routers import sessions


app = FastAPI()
app.include_router(devices.router)
app.include_router(sessions.router)