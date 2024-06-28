from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .database import init as init_db
from .config import database_settings, kafka_settings
from .organization.router import router as organization_router
from .players.router import router as players_router

app = FastAPI(
    title="CTF Manager",
    summary="A manager for your CTFs. Manage teams and flags."
)

app.add_event_handler("startup", init_db)

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/livez")
def alive():
    return("I'm alive!")

@app.get("/info")
def info():
    return{
        "Database DB name": database_settings.db_name,
        "Kafka enablement": kafka_settings.enable,
        "Kafka topic name": kafka_settings.topic
    }

app.include_router(organization_router, prefix="/team", tags=["organization"])
app.include_router(players_router, prefix="/team/{code_name}", tags=["players"])
