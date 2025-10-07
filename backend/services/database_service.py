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
        # Use os.environ.get() with fallbacks to prevent KeyError crashes
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.db_name = os.environ.get('DB_NAME', 'pymetra_registration')
        
        logger.info(f"DatabaseService initialized with DB: {self.db_name}")
        logger.info(f"MongoDB URL configured: {self.mongo_url[:20]}...")
        
        try:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.db_name]
            logger.info("DatabaseService successfully connected")
        except Exception as e:
            logger.error(f"DatabaseService connection failed: {str(e)}")
            raise e
        
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
    
    async def update_registration_drive_info(self, registration_id: str, drive_id: str, drive_link: str):
        """Update registration with Google Drive information"""
        try:
            result = await self.db.agent_registrations.update_one(
                {"id": registration_id},
                {"$set": {
                    "cv_drive_id": drive_id,
                    "cv_drive_link": drive_link
                }}
            )
            
            if result.modified_count > 0:
                logger.info(f"Updated registration {registration_id} with Drive info")
                return True
            else:
                logger.warning(f"No registration found to update: {registration_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update registration drive info: {str(e)}")
            return False