from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models.user import User
from schemas import UserCreate, LoginUser, SkillInput
import bcrypt
from schemas import ProfileUpdate
from fastapi import UploadFile, File
from schemas import PreferenceUpdate
from schemas import SkillGapRequest
import pdfplumber
from schemas import RoadmapRequest
from jobs import JOBS
from schemas import (
    UserCreate,
    LoginUser,
    ProfileUpdate,
    PreferenceUpdate
)
from schemas import ResumeScoreRequest
from jobs_api import get_jobs
import google.generativeai as genai
from agent.coordinator_agent import CoordinatorAgent
from models.application import Application
import smtplib
from email.message import EmailMessage
from schemas import ApplyJobRequest
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(
    api_key="AQ.Ab8RN6LnQ8A6_FYAheRLFry3xD70XIVIzdLKcw77WFKb-YkI2A"
)
SENDER_EMAIL = "yourgmail@gmail.com"
SENDER_PASSWORD = "your_app_password"
def send_email(receiver_email, company, role, status):

    msg = EmailMessage()

    msg["Subject"] = "Interview Update"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Hello,

Your application for {role} at {company}
has been updated.

Current Status:
{status}

Best wishes,
Career Advisor Agent
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )
        server.send_message(msg)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "react",
    "nodejs",
    "flask",
    "fastapi",
    "aws",
    "docker",
    "kubernetes",
    "mongodb"
]
JOB_MAP = {
    "python": ["Python Developer", "Backend Developer"],
    "sql": ["Data Analyst", "Database Administrator"],
    "machine learning": ["ML Engineer", "AI Engineer"],
    "deep learning": ["Deep Learning Engineer"],
    "tensorflow": ["AI Engineer"],
    "aws": ["Cloud Engineer", "DevOps Engineer"],
    "react": ["Frontend Developer"],
    "nodejs": ["Full Stack Developer"]
}
ROLE_SKILLS = {
    "AI Engineer": [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "aws"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "power bi"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react"
    ]
}
ROADMAPS = {
    "machine learning": [
        "Python Basics",
        "NumPy",
        "Pandas",
        "Matplotlib",
        "Machine Learning",
        "Scikit-Learn",
        "Deep Learning",
        "TensorFlow/PyTorch",
        "Projects"
    ],

    "data science": [
        "Python",
        "Statistics",
        "NumPy",
        "Pandas",
        "Data Visualization",
        "Machine Learning",
        "Projects"
    ],

    "web development": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "Projects"
    ],

    "ai engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "LLMs",
        "LangChain",
        "RAG",
        "Agentic AI",
        "Projects"
    ]
}
ROLE_SKILLS = {
    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "docker"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react"
    ]
}


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Career Agent API Running"}
@app.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        skills=user.skills
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }
@app.post("/login")
def login(user: LoginUser):

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if db_user is None:
        return {"message": "User Not Found"}

    if db_user.password is None:
        return {"message": "Password not set for this user"}

    if bcrypt.checkpw(
        user.password.encode("utf-8"),
        db_user.password.encode("utf-8")
    ):
        return {"message": "Login Success"}

    return {"message": "Invalid Password"}
@app.post("/profile")
def update_profile(profile: ProfileUpdate):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == profile.email
    ).first()

    if not user:
        return {"message": "User not found"}

    user.degree = profile.degree
    user.college = profile.college
    user.graduation_year = profile.graduation_year

    db.commit()

    return {"message": "Profile Updated"}
@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...)):

    text = ""

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    with pdfplumber.open(file.filename) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return {
        "skills": found_skills
    }
@app.post("/recommend_jobs_skill")
def recommend_jobs_skill(data: SkillInput):

    jobs = set()

    for skill in data.skills:
        skill = skill.lower()

        if skill in JOB_MAP:
            for job in JOB_MAP[skill]:
                jobs.add(job)

    return {
        "recommended_jobs": list(jobs)
    }
@app.post("/preferences")
def update_preferences(data: PreferenceUpdate):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        return {"message": "User not found"}

    user.preferred_company = data.preferred_company
    user.preferred_domain = data.preferred_domain
    user.preferred_location = data.preferred_location
    user.job_type = data.job_type

    db.commit()

    return {"message": "Preferences Saved"}
@app.post("/skill_gap")
def skill_gap(data: SkillGapRequest):

    role_skills = ROLE_SKILLS.get(
        data.target_role,
        []
    )

    current = [
        skill.lower()
        for skill in data.current_skills
    ]

    missing = []

    for skill in role_skills:
        if skill not in current:
            missing.append(skill)

    return {
        "target_role": data.target_role,
        "missing_skills": missing
    }
@app.post("/roadmap")
def roadmap(data: RoadmapRequest):

    roadmap_list = ROADMAPS.get(
        data.target_role.lower(),
        ["Role not found"]
    )

    return {
        "target_role": data.target_role,
        "roadmap": roadmap_list
    }
@app.post("/recommend_jobs")
def recommend_jobs(preference: PreferenceUpdate):

    recommendations = []

    for job in JOBS:

        if (
            job["domain"].lower()
            == preference.preferred_domain.lower()
        ):

            recommendations.append(job)

    return {
        "recommended_jobs": recommendations
    }
@app.post("/apply_job")
def apply_job(data: ApplyJobRequest):
    db = SessionLocal()

    application = Application(
        email=data.email,
        company=data.company,
        role=data.role,
        apply_link=data.apply_link
    )

    db.add(application)
    db.commit()

    return {
        "message": "Application tracked successfully"
    }
@app.post("/auto_apply")
def auto_apply(email: str, role: str):
    jobs = get_jobs(role)

    db = SessionLocal()

    for job in jobs[:5]:
        application = Application(
            email=email,
            company=job["company"],
            role=job["title"],
            apply_link=job["redirect_url"],
            status="Pending"
        )

        db.add(application)

    db.commit()

    return {
        "message": "Top jobs added to tracker"
    }
@app.get("/applications/{email}")
def get_applications(email: str):

    db = SessionLocal()

    applications = db.query(Application).filter(
        Application.email == email
    ).all()

    return [
        {
            "id": a.id,
            "email": a.email,
            "company": a.company,
            "role": a.role,
            "status": a.status,
            "apply_link": a.apply_link
        }
        for a in applications
    ]
@app.put("/update_status/{application_id}")
def update_status(application_id: int, status: str):

    db = SessionLocal()

    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        return {"message": "Application not found"}

    application.status = status
    db.commit()

    send_email(
        application.email,
        application.company,
        application.role,
        status
    )

    return {"message": "Status updated and email sent"}

from resources import LEARNING_RESOURCES

@app.post("/learning_resources")
def learning_resources(data: SkillGapRequest):

    missing = ROLE_SKILLS.get(
        data.target_role,
        []
    )

    resources = {}

    for skill in missing:
        if skill in LEARNING_RESOURCES:
            resources[skill] = LEARNING_RESOURCES[skill]

    return resources
@app.post("/resume_optimize")
def resume_optimize(data: ResumeScoreRequest):

    suggestions = []

    if "docker" not in data.skills:
        suggestions.append(
            "Add Docker skill for deployment jobs"
        )

    if "aws" not in data.skills:
        suggestions.append(
            "Learn AWS Cloud Fundamentals"
        )

    if "github" not in data.skills:
        suggestions.append(
            "Create and showcase GitHub projects"
        )

    return {
        "suggestions": suggestions
    }
@app.get("/live_jobs/{role}")
def live_jobs(role: str):

    jobs = get_jobs(role)

    return jobs
@app.post("/send_job_alert")
def send_job_alert(email: str):

    return {
        "message":
        f"Job alert sent to {email}"
    }
@app.put("/update_status/{application_id}")
def update_status(
    application_id: int,
    status: str
):

    db = SessionLocal()

    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        return {
            "message": "Application not found"
        }

    application.status = status

    db.commit()

    send_email(
        application.email,
        application.company,
        application.role,
        status
    )

    return {
        "message":
        "Status updated and email sent"
    }
from pydantic import BaseModel

# ✅ ADD THIS CLASS HERE (TOP SECTION of your file)
class ChatRequest(BaseModel):
    message: str


# 👇 your existing model
model = genai.GenerativeModel("gemini-2.5-flash")


# 👇 CHAT API
@app.post("/chat")
def chat(data: ChatRequest):
    response = model.generate_content(data.message)

    return {
        "response": response.text
    }
@app.post("/career_advisor")
def career_advisor(email: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return {
            "error": "User not found"
        }

    data = {
        "skills": user.skills.split(",")
    }

    return data
@app.get("/users")
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    return users