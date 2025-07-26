from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(140), nullable=False)

    resumes = db.relationship('Resume', backref='user', cascade="all, delete", lazy=True)


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable=False)
    style = db.Column(db.String(20), nullable=False, default='modern')

    personal_info = db.relationship('PersonalInfo', backref='resume', uselist=False, cascade="all, delete")

    education = db.relationship('Education', backref='resume', cascade="all, delete", lazy=True)
    experience = db.relationship('Experience', backref='resume', cascade="all, delete", lazy=True)
    projects = db.relationship('Project', backref='resume', cascade="all, delete", lazy=True)
    skills = db.relationship('Skill', backref='resume', cascade="all, delete", lazy=True)
    certifications = db.relationship('Certification', backref='resume', cascade="all, delete", lazy=True)

# --------------------------
# 👤 Personal Info (One per Resume)
# --------------------------
class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), unique=True)
    profile_pic = db.Column(db.String(150), default='default.jpg')
    full_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    resume_email = db.Column(db.String(60), nullable=False)
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    address = db.Column(db.String(200))
    summary = db.Column(db.String(300), nullable=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(100))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    description = db.Column(db.String(300))

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    description = db.Column(db.String(300))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    tech_stack = db.Column(db.String(200))
    link = db.Column(db.String(200))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    name = db.Column(db.String(50))
    level = db.Column(db.String(20)) 

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    name = db.Column(db.String(100))
    issuer = db.Column(db.String(100))
    issue_date = db.Column(db.String(20))
    credential_link = db.Column(db.String(200))
