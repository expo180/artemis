from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Students
from werkzeug.security import generate_password_hash
from .forms import CourseWorkRegistrationForm
from datetime import datetime
import urllib.parse
import uuid

def generate_unique_token_for_student(student_id):
    # Generate a unique token using the student_id and a UUID
    unique_id = uuid.uuid4().hex
    token = f"{student_id}-{unique_id}"
    return token

@auth.route("/inscription/", methods=['POST'])
def enroll():
    form_data = request.get_json()

    if not form_data or not isinstance(form_data, dict):
        return jsonify({'success': False, 'message': 'Invalid data format'})

    # Check for duplicate email
    existing_student = Students.query.filter_by(email=form_data.get('email', '')).first()
    if existing_student:
        flash('An account with this email address already exists.', 'danger')
        return jsonify({'success': False, 'message': 'Duplicate email address'})

    # Create a new instance of the Students model and populate it with form data
    student = Students(
        first_name=form_data.get('first_name', ''),
        last_name=form_data.get('last_name', ''),
        email=form_data.get('email', ''),
        phone_number=form_data.get('phone_number', ''),
        motivation=form_data.get('motivation', ''),
        program_title=form_data.get('areas_of_interest', ''),
        member_since=datetime.utcnow()
    )

    try:
        # Save the new student to the database
        db.session.add(student)
        db.session.commit()
        token = generate_unique_token_for_student(student.id)
        email = form_data.get('email', '')
        redirect_url = f"https:https://ekki.onrender.com?email={urllib.parse.quote(email)}&token={token}"
        return redirect(redirect_url)
    
    except IntegrityError:
        # Handle unique constraint violation (duplicate email)
        db.session.rollback()
        flash('An account with this email address already exists.', 'danger')
        return jsonify({'success': False, 'message': 'Duplicate email address'})


@auth.route("/s'incrire/formation/", methods=['GET', 'POST'])
def register():
    form = CourseWorkRegistrationForm()
    return render_template('auth/register.html', form=form)

