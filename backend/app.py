from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models.user import User
from schemas import UserCreate, LoginUser, SkillInput
import bcrypt
from schemas import ProfileUpdate
from fastapi import UploadFile, File,Form
from schemas import PreferencesRequest 
import pdfplumber
from schemas import RoadmapRequest
from jobs import JOBS
from schemas import (
    UserCreate,
    LoginUser,
    ProfileUpdate,
    PreferencesRequest,
    CareerMentorRequest,
    ReminderCreate

)

from jobs_api import get_jobs
from groq import Groq
from models.application import Application
import smtplib
from email.message import EmailMessage
from schemas import ApplyJobRequest
from agent.career_mentor_agent import CareerMentorAgent
from models.remainder import Reminder
from schemas import CareerMentorRequest
import re
import os
from agent.roadmap_agent import RoadmapAgent


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
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

career_agent = CareerMentorAgent(client)
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

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau"
    ],

    "Backend Developer": [
        "python",
        "fastapi",
        "sql",
        "docker"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "nodejs",
        "mongodb"
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
@app.get("/profile/{email}")
def get_profile(email: str):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}

    return {
        "email": user.email,
        "degree": user.degree,
        "college": user.college,
        "graduation_year": user.graduation_year
    }
@app.put("/profile/{email}")
def update_profile(email: str, profile: ProfileUpdate):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        db.close()
        return {"error": "User not found"}

    user.degree = profile.degree
    user.college = profile.college
    user.graduation_year = profile.graduation_year

    db.commit()
    db.close()

    return {
        "message": "Profile Updated Successfully"
    }
@app.post("/upload_resume")
def upload_resume(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    db = SessionLocal()

    text = ""

    try:
        # Read uploaded PDF directly
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text.lower()

        # Extract Skills
        found_skills = []

        for skill in SKILLS:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)

        # ATS Score
        ats_score = 0

        education_keywords = [
            "education",
            "bachelor",
            "master",
            "degree"
        ]

        experience_keywords = [
            "experience",
            "internship",
            "work experience"
        ]

        project_keywords = [
            "project",
            "projects"
        ]

        skill_keywords = [
            "skills",
            "technical skills"
        ]

        if any(word in text for word in education_keywords):
            ats_score += 20

        if any(word in text for word in experience_keywords):
            ats_score += 20

        if any(word in text for word in project_keywords):
            ats_score += 20

        if any(word in text for word in skill_keywords):
            ats_score += 20

        if len(found_skills) >= 5:
            ats_score += 20

        # Resume Score
        resume_score = 0

        resume_score += min(len(found_skills) * 5, 50)

        if any(word in text for word in education_keywords):
            resume_score += 15

        if any(word in text for word in experience_keywords):
            resume_score += 15

        if any(word in text for word in project_keywords):
            resume_score += 10

        if "certification" in text:
            resume_score += 10

        resume_score = min(resume_score, 100)

        # Save to Database
        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {"error": "User not found"}

        user.skills = ",".join(found_skills)
        user.resume_score = resume_score
        user.ats_score = ats_score
        user.resume_text = text

        db.commit()

        return {
    "skills": found_skills,
    "resume_score": resume_score,
    "ats_score": ats_score,
    "resume_text_saved": len(text) > 0
}
    except Exception as e:
        return {
            "error": str(e)
        }

    finally:
        file.file.close()
        db.close()
@app.post("/preferences")
def save_preferences(data: PreferencesRequest):
    print(data)

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        return {"error": "User not found"}

    user.preferred_company = data.preferred_company
    user.preferred_domain = data.preferred_domain
    user.preferred_location = data.preferred_location
    user.job_type = data.job_type

    db.commit()

    return {
        "message": "Preferences saved successfully"
    }
@app.get("/preferences/{email}")
def get_preferences(email: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return {"error": "User not found"}

    return {
        "email": user.email,
        "preferred_company": user.preferred_company,
        "preferred_domain": user.preferred_domain,
        "preferred_location": user.preferred_location,
        "job_type": user.job_type
    }

from agent.roadmap_agent import RoadmapAgent
roadmap_agent = RoadmapAgent()
@app.post("/roadmap")
def roadmap(data: RoadmapRequest):

    result = roadmap_agent.run(data.target_role)

    return {
        "target_role": data.target_role,
        "roadmap": result
    }
@app.post("/apply_job")
def apply_job(data: ApplyJobRequest):

    db = SessionLocal()

    existing = db.query(Application).filter(
        Application.email == data.email,
        Application.company == data.company,
        Application.role == data.role
    ).first()

    if existing:
        return {
            "message": "Application already tracked"
        }

    application = Application(
        email=data.email,
        company=data.company,
        role=data.role,
        apply_link=data.apply_link,
        status="Pending"
    )

    db.add(application)
    db.commit()

    return {
        "message": "Application tracked successfully"
    }
@app.post("/auto_apply")
def auto_apply(email: str, role: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        db.close()
        return {"error": "User not found"}

    jobs = get_jobs(role)

    count = 0

    for job in jobs[:5]:

        existing = db.query(Application).filter(
            Application.email == email,
            Application.company == job["company"],
            Application.role == job["title"]
        ).first()

        if existing:
            continue

        application = Application(
            email=email,
            company=job["company"],
            role=job["title"],
            apply_link=job["apply_link"],
            status="Pending"
        )

        db.add(application)
        count += 1

    db.commit()
    db.close()

    return {
        "message": f"{count} jobs tracked successfully"
    }
@app.get("/live_jobs/{role}")
def live_jobs(role: str):

    try:
        jobs = get_jobs(role)
        return jobs

    except Exception as e:
        return {
            "error": "Unable to fetch jobs",
            "details": str(e)
        }
@app.post("/send_job_alert")
def send_job_alert(email: str):

    return {
        "message":
        f"Job alert sent to {email}"
    }
@app.get("/recommended_jobs/{email}")
def recommended_jobs(email: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return {"error": "User not found"}

    role = user.preferred_domain
    try:
        jobs = get_jobs(role)
        return jobs[:10]

    except Exception as e:
        return {
            "error": "Unable to fetch recommended jobs",
            "details": str(e)
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
@app.delete("/applications/{application_id}")
def delete_application(application_id: int):

    db = SessionLocal()

    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        return {"message": "Application not found"}

    db.delete(application)
    db.commit()

    return {"message": "Application deleted"}
@app.get("/user_applications/{email}")
def get_applications(email: str):

    db = SessionLocal()

    applications = db.query(Application).filter(
        Application.email == email
    ).all()

    return applications
from pydantic import BaseModel

# ✅ ADD THIS CLASS HERE (TOP SECTION of your file)
class ChatRequest(BaseModel):
    message: str



# 👇 CHAT API
@app.post("/chat")
def chat(data: ChatRequest):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
@app.get("/users")
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    return users
@app.post("/career_mentor")
def career_mentor(data: CareerMentorRequest):
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:
            return {"error": "User not found"}

        jobs = get_jobs(
            user.preferred_domain
            if user.preferred_domain
            else data.target_role
        )

        current_skills = []

        if user.skills:
            current_skills = [
                s.strip().lower()
                for s in user.skills.split(",")
            ]

        required_skills = ROLE_SKILLS.get(
            data.target_role,
            []
        )

        missing_skills = []

        for skill in required_skills:
            if skill.lower() not in current_skills:
                missing_skills.append(skill)

        user_info = {
            "name": user.name,
            "skills": user.skills or "",
            "resume_text": user.resume_text or "",
            "missing_skills": missing_skills,
            "target_role": data.target_role,
            "preferred_company": user.preferred_company,
            "preferred_domain": user.preferred_domain,
            "preferred_location": user.preferred_location,
            "job_type": user.job_type,
            "live_jobs": jobs[:5]
        }

        result = career_agent.process(user_info)

        result["missing_skills"] = missing_skills

        db.commit()

        return result

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }

    finally:
        db.close()
@app.post("/add_reminder")
def add_reminder(data: ReminderCreate):

    db = SessionLocal()

    reminder = Reminder(
        email=data.email,
        task=data.task,
        due_date=data.due_date
    )

    db.add(reminder)
    db.commit()

    return {
        "message": "Reminder added"
    }
@app.get("/reminders/{email}")
def get_reminders(email: str):

    db = SessionLocal()

    reminders = db.query(Reminder).filter(
        Reminder.email == email
    ).all()

    return reminders
@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int):

    db = SessionLocal()

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if not reminder:
        db.close()
        return {
            "error": "Reminder not found"
        }

    db.delete(reminder)
    db.commit()
    db.close()

    return {
        "message": "Reminder deleted successfully"
    }
@app.put("/reminders/{reminder_id}")
def complete_reminder(reminder_id: int):

    db = SessionLocal()

    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if reminder is None:
        db.close()
        return {"error": "Reminder not found"}

    reminder.status = "Completed"

    db.commit()
    db.refresh(reminder)
    db.close()

    return {
        "message": "Reminder marked as completed"
    }
