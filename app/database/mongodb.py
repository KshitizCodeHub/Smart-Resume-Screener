"""
MongoDB database connection and operations.
Handles all database interactions using Motor (async MongoDB driver).
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, List, Dict, Any, ClassVar
from datetime import datetime, timezone
from bson import ObjectId
from app.config import settings

class MongoDB:
    """MongoDB database handler with async operations."""
    
    client = None  # type: AsyncIOMotorClient | None
    database = None  # type: AsyncIOMotorDatabase | None
    
    @classmethod
    async def connect_db(cls):
        """Establish connection to MongoDB Atlas."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            cls.database = cls.client[settings.mongodb_db_name]
            # Test connection
            await cls.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {settings.mongodb_db_name}")
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            raise e
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("🔌 MongoDB connection closed")
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a specific collection from the database."""
        return cls.database[collection_name]


class ResumeDB:
    """Resume collection operations."""
    
    @staticmethod
    async def create_resume(resume_data: Dict[str, Any]) -> str:
        """Insert a new resume document."""
        collection = MongoDB.get_collection("resumes")
        resume_data["upload_date"] = datetime.now(timezone.utc).isoformat()
        result = await collection.insert_one(resume_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_resume(resume_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a resume by ID."""
        collection = MongoDB.get_collection("resumes")
        resume = await collection.find_one({"_id": ObjectId(resume_id)})
        if resume:
            resume["_id"] = str(resume["_id"])
        return resume
    
    @staticmethod
    async def get_all_resumes() -> List[Dict[str, Any]]:
        """Retrieve all resumes."""
        collection = MongoDB.get_collection("resumes")
        resumes = []
        cursor = collection.find({})
        async for resume in cursor:
            resume["_id"] = str(resume["_id"])
            resumes.append(resume)
        return resumes
    
    @staticmethod
    async def delete_resume(resume_id: str) -> bool:
        """Delete a resume by ID."""
        collection = MongoDB.get_collection("resumes")
        result = await collection.delete_one({"_id": ObjectId(resume_id)})
        return result.deleted_count > 0


class JobDB:
    """Job description collection operations."""
    
    @staticmethod
    async def create_job(job_data: Dict[str, Any]) -> str:
        """Insert a new job description."""
        collection = MongoDB.get_collection("jobs")
        job_data["created_date"] = datetime.now(timezone.utc).isoformat()
        result = await collection.insert_one(job_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_job(job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a job by ID."""
        collection = MongoDB.get_collection("jobs")
        job = await collection.find_one({"_id": ObjectId(job_id)})
        if job:
            job["_id"] = str(job["_id"])
        return job
    
    @staticmethod
    async def get_all_jobs() -> List[Dict[str, Any]]:
        """Retrieve all job descriptions."""
        collection = MongoDB.get_collection("jobs")
        jobs = []
        cursor = collection.find({})
        async for job in cursor:
            job["_id"] = str(job["_id"])
            jobs.append(job)
        return jobs
    
    @staticmethod
    async def delete_job(job_id: str) -> bool:
        """Delete a job by ID."""
        collection = MongoDB.get_collection("jobs")
        result = await collection.delete_one({"_id": ObjectId(job_id)})
        return result.deleted_count > 0


class MatchDB:
    """Match results collection operations."""
    
    @staticmethod
    async def create_match(match_data: Dict[str, Any]) -> str:
        """Insert a new match result."""
        collection = MongoDB.get_collection("matches")
        match_data["timestamp"] = datetime.now(timezone.utc).isoformat()
        result = await collection.insert_one(match_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def get_matches_by_job(job_id: str) -> List[Dict[str, Any]]:
        """Retrieve all matches for a specific job."""
        collection = MongoDB.get_collection("matches")
        matches = []
        cursor = collection.find({"job_id": job_id}).sort("score", -1)
        async for match in cursor:
            match["_id"] = str(match["_id"])
            matches.append(match)
        return matches
    
    @staticmethod
    async def get_all_matches() -> List[Dict[str, Any]]:
        """Retrieve all matches."""
        collection = MongoDB.get_collection("matches")
        matches = []
        cursor = collection.find({})
        async for match in cursor:
            match["_id"] = str(match["_id"])
            matches.append(match)
        return matches
