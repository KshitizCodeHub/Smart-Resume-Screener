"""
Database Cleanup Script
Fixes schema mismatches in existing data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
MONGODB_URI = os.getenv("MONGODB_URL")  # Changed from MONGODB_URI to MONGODB_URL
if not MONGODB_URI:
    print("❌ Error: MONGODB_URL not found in .env file")
    exit(1)

DB_NAME = os.getenv("MONGODB_DB_NAME", "resume_screener_db")

async def fix_certifications(collection):
    """Fix certifications field - convert dict to string list."""
    print("\n📋 Fixing certifications field in resumes...")
    
    cursor = collection.find({})
    fixed_count = 0
    
    async for doc in cursor:
        parsed_data = doc.get("parsed_data", {})
        certifications = parsed_data.get("certifications", [])
        
        if certifications and isinstance(certifications, list):
            # Check if any certification is a dict
            needs_fix = any(isinstance(cert, dict) for cert in certifications)
            
            if needs_fix:
                # Convert dicts to strings
                fixed_certs = []
                for cert in certifications:
                    if isinstance(cert, dict):
                        # Format: "Name (Issuer, Year)"
                        name = cert.get("name", "Unknown")
                        issuer = cert.get("issuer", "")
                        year = cert.get("year", "")
                        
                        if issuer and year:
                            fixed_certs.append(f"{name} ({issuer}, {year})")
                        elif issuer:
                            fixed_certs.append(f"{name} ({issuer})")
                        else:
                            fixed_certs.append(name)
                    else:
                        fixed_certs.append(str(cert))
                
                # Update document
                parsed_data["certifications"] = fixed_certs
                await collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"parsed_data": parsed_data}}
                )
                fixed_count += 1
                print(f"   ✅ Fixed resume: {doc.get('filename', 'Unknown')}")
    
    print(f"   📊 Fixed {fixed_count} resume(s)")
    return fixed_count

async def fix_job_requirements(collection):
    """Fix job requirements field - convert dict to string list."""
    print("\n💼 Fixing requirements field in jobs...")
    
    cursor = collection.find({})
    fixed_count = 0
    
    async for doc in cursor:
        requirements = doc.get("requirements", [])
        
        # Check if requirements is a dict (old format)
        if isinstance(requirements, dict):
            # Convert dict to list of strings
            fixed_reqs = []
            
            required_skills = requirements.get("required_skills", [])
            preferred_skills = requirements.get("preferred_skills", [])
            experience = requirements.get("experience_required", "")
            education = requirements.get("education_required", "")
            responsibilities = requirements.get("responsibilities", [])
            
            if required_skills:
                fixed_reqs.append(f"Required Skills: {', '.join(required_skills)}")
            if preferred_skills:
                fixed_reqs.append(f"Preferred Skills: {', '.join(preferred_skills)}")
            if experience:
                fixed_reqs.append(f"Experience: {experience}")
            if education:
                fixed_reqs.append(f"Education: {education}")
            if responsibilities:
                fixed_reqs.extend([f"Responsibility: {r}" for r in responsibilities])
            
            # If still empty, add default
            if not fixed_reqs:
                fixed_reqs = ["See job description for requirements"]
            
            # Update document
            await collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"requirements": fixed_reqs}}
            )
            fixed_count += 1
            print(f"   ✅ Fixed job: {doc.get('title', 'Unknown')}")
    
    print(f"   📊 Fixed {fixed_count} job(s)")
    return fixed_count

async def main():
    """Run database cleanup."""
    print("\n" + "="*70)
    print("🔧 DATABASE CLEANUP UTILITY")
    print("="*70)
    print(f"\nConnecting to MongoDB: {DB_NAME}")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    try:
        # Test connection
        await db.command("ping")
        print("✅ Connected successfully")
        
        # Fix resumes collection
        resumes_collection = db["resumes"]
        resumes_fixed = await fix_certifications(resumes_collection)
        
        # Fix jobs collection
        jobs_collection = db["jobs"]
        jobs_fixed = await fix_job_requirements(jobs_collection)
        
        # Summary
        print("\n" + "="*70)
        print("📊 CLEANUP SUMMARY")
        print("="*70)
        print(f"Resumes fixed: {resumes_fixed}")
        print(f"Jobs fixed: {jobs_fixed}")
        print(f"Total fixes: {resumes_fixed + jobs_fixed}")
        
        if resumes_fixed + jobs_fixed > 0:
            print("\n✅ Database cleaned successfully!")
            print("🚀 You can now use the application without errors")
        else:
            print("\n✅ No fixes needed - database is clean!")
        
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        client.close()
        print("\n🔌 Disconnected from MongoDB")

if __name__ == "__main__":
    print("\n⚠️  This script will fix schema mismatches in your database")
    print("It will convert old data formats to match the current API schemas\n")
    
    asyncio.run(main())
