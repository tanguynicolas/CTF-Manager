# root of the project, which inits the FastAPI app

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="CTF Manager")

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/livez")
def alive():
    return("I'm alive!")

@app.get("/info")
def info():
    return {"Info": "No info"}
