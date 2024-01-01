from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Students
from werkzeug.security import generate_password_hash
from .forms import CourseWorkRegistrationForm
from datetime import datetime

@auth.route("/inscription/", methods=['POST'])
def enroll():
    form_data = request.get_json()
    print(form_data)
    # Validate the incoming data
    if not form_data or not isinstance(form_data, dict):
        return jsonify({'success': False, 'message': 'Invalid data format'})

    # Create a new instance of the Students model and populate it with form data
    student = Students(
        first_name=form_data.get('first_name', ''),
        last_name=form_data.get('last_name', ''),
        email=form_data.get('email', ''),
        phone_number=form_data.get('phone_number', ''),
        motivation=form_data.get('motivation', ''),
        program_title=form_data.get('areas_of_interest', '') 
    )
    # Save the new student to the database
    db.session.add(student)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Form submitted successfully'})

@auth.route("/s'incrire/formation/", methods=['GET', 'POST'])
def register():
    form = CourseWorkRegistrationForm()
    return render_template('auth/register.html', form=form)

