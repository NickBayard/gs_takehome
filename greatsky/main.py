from fastapi import FastAPI, Response, status

from greatsky.routers import devices


app = FastAPI()
app.include_router(devices.router)