from fastapi import FastAPI

from greatsky.routers import (
    biases,
    devices,
    sessions,
    waveforms,
    weights,
)

app = FastAPI()
app.include_router(devices.router)
app.include_router(sessions.router)
app.include_router(waveforms.router)
app.include_router(biases.router)
app.include_router(weights.router)
