from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import *
from weasyprint import HTML
import os , tempfile

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/uploads/'

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        resume_email = request.form.get('resume_email')
        phone = request.form.get('phone')
        github = request.form.get('github')
        linkedin = request.form.get('linkedin')
        summary = request.form.get('summary')
        style = request.form.get('template')
        profile_pic = request.files.get('profile_pic')

        if not full_name or not resume_email:
            flash("Full Name and Resume Email are required.", "danger")
            return redirect(url_for('views.home'))

        filename = 'default.jpg'
        if profile_pic and profile_pic.filename != '':
            filename = secure_filename(profile_pic.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            profile_pic.save(filepath)

        resume = Resume(user_id=current_user.id, title=f"{full_name}'s Resume", style=style)
        db.session.add(resume)
        db.session.commit()

        info = PersonalInfo(
            resume_id=resume.id,
            full_name=full_name,
            resume_email=resume_email,
            phone=phone,
            github=github,
            linkedin=linkedin,
            summary=summary,
            profile_pic=filename
        )
        db.session.add(info)
        db.session.commit()

        flash("Basic resume info saved! Now complete your resume.", "success")
        return redirect(url_for('views.create_resume', resume_id=resume.id))

    return render_template("home.html")

@views.route('/Resume/<int:resume_id>', methods=['GET', 'POST'])
@login_required
def create_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.home'))

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    education = Education.query.filter_by(resume_id=resume.id).first()
    experience = Experience.query.filter_by(resume_id=resume.id).first()
    project = Project.query.filter_by(resume_id=resume.id).first()
    skill = Skill.query.filter_by(resume_id=resume.id).first()
    certification = Certification.query.filter_by(resume_id=resume.id).first()

    if request.method == 'POST':
        info.full_name = request.form.get('full_name')
        info.resume_email = request.form.get('resume_email')
        info.phone = request.form.get('phone')
        info.github = request.form.get('github')
        info.linkedin = request.form.get('linkedin')
        info.summary = request.form.get('summary')

        profile_pic = request.files.get('profile_pic')
        if profile_pic and profile_pic.filename != '':
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(profile_pic.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            profile_pic.save(filepath)


        if not education:
            education = Education(resume_id=resume.id)
        education.degree = request.form.get('degree')
        education.institution = request.form.get('institution')
        education.start_year = request.form.get('start_year')
        education.end_year = request.form.get('end_year')
        education.description = request.form.get('edu_description')

        if not experience:
            experience = Experience(resume_id=resume.id)
        experience.job_title = request.form.get('job_title')
        experience.company = request.form.get('company')
        experience.start_date = request.form.get('start_date')
        experience.end_date = request.form.get('end_date')
        experience.description = request.form.get('exp_description')

        if not project:
            project = Project(resume_id=resume.id)
        project.title = request.form.get('project_title')
        project.description = request.form.get('project_description')
        project.tech_stack = request.form.get('tech_stack')
        project.link = request.form.get('project_link')

        if not skill:
            skill = Skill(resume_id=resume.id)
        skill.name = request.form.get('skill_name')
        skill.level = request.form.get('skill_level')

        if not certification:
            certification = Certification(resume_id=resume.id)
        certification.name = request.form.get('cert_name')
        certification.issuer = request.form.get('issuer')
        certification.issue_date = request.form.get('issue_date')
        certification.credential_link = request.form.get('credential_link')

        db.session.add_all([info, education, experience, project, skill, certification])
        db.session.commit()

        flash("Resume updated successfully!", "success")
        return redirect(url_for('views.view_resume', resume_id=resume.id))

    return render_template("resumetemplate.html", Resume=resume, PersonalInfo=info, Education=education,
                           Experience=experience, Project=project, Skill=skill, Certification=certification)

@views.route('/resume/view/<int:resume_id>')
@login_required
def view_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("You are not authorized to view this resume.", "danger")
        return redirect(url_for('views.home'))

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    education = Education.query.filter_by(resume_id=resume.id).first()
    experience = Experience.query.filter_by(resume_id=resume.id).first()
    project = Project.query.filter_by(resume_id=resume.id).first()
    skill = Skill.query.filter_by(resume_id=resume.id).first()
    certification = Certification.query.filter_by(resume_id=resume.id).first()

    return render_template("resume_base.html", resume=resume, info=info, education=education,
                           experience=experience, project=project, skill=skill,
                           certification=certification)

@views.route('/resume/manage')
@login_required
def manage_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template("manage.html", resumes=resumes)

@views.route('/resume/delete/<int:resume_id>')
@login_required
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))

    PersonalInfo.query.filter_by(resume_id=resume.id).delete()
    Education.query.filter_by(resume_id=resume.id).delete()
    Experience.query.filter_by(resume_id=resume.id).delete()
    Project.query.filter_by(resume_id=resume.id).delete()
    Skill.query.filter_by(resume_id=resume.id).delete()
    Certification.query.filter_by(resume_id=resume.id).delete()
    db.session.delete(resume)
    db.session.commit()

    flash("Resume deleted.", "success")
    return redirect(url_for('views.manage_resumes'))
@views.route('/resume/download/<int:resume_id>')
@login_required
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('views.manage_resumes'))

    info = PersonalInfo.query.filter_by(resume_id=resume.id).first()
    education = Education.query.filter_by(resume_id=resume.id).first()
    experience = Experience.query.filter_by(resume_id=resume.id).first()
    project = Project.query.filter_by(resume_id=resume.id).first()
    skill = Skill.query.filter_by(resume_id=resume.id).first()
    certification = Certification.query.filter_by(resume_id=resume.id).first()

    rendered_html = render_template("resume_base.html", resume=resume, info=info,
                                    education=education, experience=experience,
                                    project=project, skill=skill,
                                    certification=certification)

    # 🛠️ Important: static folder as base_url so WeasyPrint can find css/images
    base_path = os.path.abspath("static")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=rendered_html, base_url=base_path).write_pdf(tmp.name)
        return send_file(tmp.name, as_attachment=True, download_name=f"{resume.title}.pdf")
