from motor.motor_asyncio import AsyncIOMotorClient
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

from models import AgentRegistration
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.mongo_url = os.environ['MONGO_URL']
        self.db_name = os.environ['DB_NAME']
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client[self.db_name]
        
    async def save_registration(self, registration: AgentRegistration) -> str:
        try:
            result = await self.db.agent_registrations.insert_one(registration.dict())
            logger.info(f"Registration saved with ID: {registration.id}")
            return registration.id
        except Exception as e:
            logger.error(f"Failed to save registration: {str(e)}")
            raise
            
    async def get_registration(self, registration_id: str) -> Optional[AgentRegistration]:
        try:
            doc = await self.db.agent_registrations.find_one({"id": registration_id})
            if doc:
                return AgentRegistration(**doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get registration: {str(e)}")
            return None
            
    async def get_all_registrations(self, limit: int = 100) -> List[AgentRegistration]:
        try:
            cursor = self.db.agent_registrations.find().limit(limit).sort("timestamp", -1)
            registrations = []
            async for doc in cursor:
                registrations.append(AgentRegistration(**doc))
            return registrations
        except Exception as e:
            logger.error(f"Failed to get registrations: {str(e)}")
            return []
            
    async def get_registrations_count(self) -> int:
        try:
            return await self.db.agent_registrations.count_documents({})
        except Exception as e:
            logger.error(f"Failed to count registrations: {str(e)}")
            return 0