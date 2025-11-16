"""
Database Schemas for Caprecon NGO MVP

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name.

Content-oriented collections support publishing workflows via optional status fields.
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr

# Core content types
class Program(BaseModel):
    title: str = Field(..., description="Program title")
    summary: str = Field(..., description="Short description for cards and previews")
    problem_context: Optional[str] = Field(None, description="Context of the issue this program addresses")
    approach: Optional[str] = Field(None, description="How Caprecon addresses the problem")
    activities: Optional[List[str]] = Field(default_factory=list, description="Key activities")
    beneficiaries: Optional[List[str]] = Field(default_factory=list, description="Target groups")
    expected_impact: Optional[str] = Field(None, description="Expected outcomes and indicators")
    locations: Optional[List[str]] = Field(default_factory=list, description="Operational locations")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for filtering")
    status: Optional[Literal['draft','published']] = Field('published', description="Publishing status")

class Story(BaseModel):
    title: str
    excerpt: Optional[str] = None
    body: Optional[str] = None
    program_tags: Optional[List[str]] = Field(default_factory=list)
    author: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Literal['draft','published']] = 'published'

class Post(BaseModel):
    title: str
    excerpt: Optional[str] = None
    body: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    author: Optional[str] = None
    status: Optional[Literal['draft','published']] = 'published'

class Report(BaseModel):
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    file_url: Optional[str] = None
    status: Optional[Literal['draft','published']] = 'published'

# Intake forms
class DonationIntent(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field('USD', description='ISO currency code')
    frequency: Literal['one_time','monthly'] = 'one_time'
    fund: Optional[str] = Field(None, description='Restricted fund name')
    first_name: str
    last_name: str
    email: EmailStr
    country: Optional[str] = None
    message: Optional[str] = None
    consent: bool = Field(..., description='User consent for communications')

class VolunteerApplication(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    role_interest: Optional[str] = None
    availability: Optional[str] = None
    experience: Optional[str] = None
    references: Optional[str] = None
    consent: bool
    status: Optional[Literal['received','screening','accepted','declined']] = 'received'

class PartnerInquiry(BaseModel):
    organization: str
    partner_type: Optional[str] = Field(None, description='NGO, agency, corporate, academic')
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None
    country: Optional[str] = None
    collaboration_areas: Optional[str] = None
    message: Optional[str] = None
    compliance_ack: bool = Field(..., description='Acknowledgement of compliance statements')
    status: Optional[Literal['received','in_discussion','mou_draft','closed']] = 'received'

class ContactMessage(BaseModel):
    topic: Optional[str] = None
    name: str
    email: EmailStr
    message: str
    consent: bool

# Optional: KPI metric definition for future impact dashboard
class Metric(BaseModel):
    key: str
    label: str
    value: float
    unit: Optional[str] = None
    period: Optional[str] = None

# Note:
# - The database helper functions in database.py (create_document, get_documents)
#   can be used with these models. Insert using collection name equal to class name lowercased.
#   Example: create_document('donationintent', DonationIntent(...))
