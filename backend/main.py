from fastapi import FastAPI
from adapters.routers.faceit import router as faceit_router
from adapters.routers.players import router as stat_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Faceit-Insight")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(faceit_router)
app.include_router(stat_router)
