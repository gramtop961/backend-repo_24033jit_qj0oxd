import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import (
    Program,
    Story,
    Post,
    DonationIntent,
    VolunteerApplication,
    PartnerInquiry,
    ContactMessage,
)

app = FastAPI(title="Caprecon NGO API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Caprecon Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Caprecon API"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

# -------- Public content listing endpoints --------

@app.get("/api/programs", response_model=List[Program])
def list_programs(limit: Optional[int] = 20, published_only: bool = True):
    filter_q = {}
    if published_only:
        filter_q["status"] = "published"
    docs = get_documents("program", filter_q, limit)
    # Remove Mongo _id for Pydantic validation simplicity
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/stories", response_model=List[Story])
def list_stories(limit: Optional[int] = 12, published_only: bool = True):
    filter_q = {"status": "published"} if published_only else {}
    docs = get_documents("story", filter_q, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/posts", response_model=List[Post])
def list_posts(limit: Optional[int] = 12, published_only: bool = True):
    filter_q = {"status": "published"} if published_only else {}
    docs = get_documents("post", filter_q, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

# -------- Intake / Forms endpoints --------

class Created(BaseModel):
    id: str
    message: str

@app.post("/api/donations", response_model=Created)
def create_donation(intent: DonationIntent):
    try:
        inserted_id = create_document("donationintent", intent)
        return {"id": inserted_id, "message": "Donation intent recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/volunteers", response_model=Created)
def create_volunteer(apply: VolunteerApplication):
    try:
        inserted_id = create_document("volunteerapplication", apply)
        return {"id": inserted_id, "message": "Volunteer application received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/partners", response_model=Created)
def create_partner(inquiry: PartnerInquiry):
    try:
        inserted_id = create_document("partnerinquiry", inquiry)
        return {"id": inserted_id, "message": "Partner inquiry submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact", response_model=Created)
def create_contact(msg: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", msg)
        return {"id": inserted_id, "message": "Message received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
