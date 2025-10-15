"""
Fix database data by converting None values to empty strings in education and experience fields
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_database():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["resume_screener_db"]
    resumes_collection = db["resumes"]
    
    print("Fixing resume data...")
    
    # Get all resumes
    resumes = await resumes_collection.find({}).to_list(length=None)
    
    fixed_count = 0
    for resume in resumes:
        needs_fix = False
        parsed_data = resume.get("parsed_data", {})
        
        # Fix education field
        if "education" in parsed_data:
            for edu in parsed_data["education"]:
                if isinstance(edu, dict):
                    for key, value in edu.items():
                        if value is None:
                            edu[key] = ""
                            needs_fix = True
        
        # Fix experience field
        if "experience" in parsed_data:
            for exp in parsed_data["experience"]:
                if isinstance(exp, dict):
                    for key, value in exp.items():
                        if value is None:
                            exp[key] = ""
                            needs_fix = True
        
        # Update the resume if it needs fixing
        if needs_fix:
            await resumes_collection.update_one(
                {"_id": resume["_id"]},
                {"$set": {"parsed_data": parsed_data}}
            )
            fixed_count += 1
            print(f"✓ Fixed resume: {resume.get('filename', 'Unknown')}")
    
    print(f"\n✅ Fixed {fixed_count} resumes")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_database())
