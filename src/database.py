from motor.motor_asyncio import AsyncIOMotorClient

from beanie import init_beanie

from .config import database_settings
from .models import Team

# Call this from within your event loop to get beanie setup.
async def init():
    # Create Motor client
    client = AsyncIOMotorClient(database_settings.url)

    # Init beanie with the document class
    await init_beanie(database=client[database_settings.db_name], document_models=[Team])
