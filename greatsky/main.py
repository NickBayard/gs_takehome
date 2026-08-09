from fastapi import FastAPI, Response, status

from greatsky.routers import (
    currents,
    devices,
    sessions, 
    waveforms,
    weights,
)

app = FastAPI()
app.include_router(devices.router)
app.include_router(sessions.router)
app.include_router(waveforms.router)
app.include_router(currents.router)
app.include_router(weights.router)