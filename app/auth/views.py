from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Students, Ambassadors
from werkzeug.security import generate_password_hash
from .forms import CourseWorkRegistrationForm, AdminSignin, AdminRegistrationForm
from datetime import datetime


@auth.route("/inscription/", methods=['POST'])
def enroll():
    form_data = request.get_json()
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
        program_title=form_data.get('areas_of_interest', ''),
        confirm_email=form_data.get('confirmEmail', ''),
        payment_method=form_data.get('payment_method', ''),
        member_since=datetime.utcnow(),
        participation_code=form_data.get('six_digit_code', '')
    )

    # Save the new student to the database
    db.session.add(student)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Form submitted successfully'}) 


@auth.route("/s'incrire/formation/", methods=['GET', 'POST'])
def register():
    form = CourseWorkRegistrationForm()
    return render_template('auth/register.html', form=form)

@auth.route("/paiement/succès/", methods=['GET', 'POST'])
def success_pay():
    return render_template('apis/payment_success.html')


@auth.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    form = AdminSignin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                print(current_user.is_instructor())
                next = url_for('main.admin_dashboard')
            return redirect(next)
        flash('Incorrect password or email address!', 'error')
    return render_template('auth/admin/login.html', form=form)

@auth.route("/admin/signup/", methods=['GET', 'POST'])
def admin_signup():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            # Display a flash message for existing email
            flash('Account already exists. Please log in.', 'error')
            return redirect(url_for('auth.admin_signup'))

        current_datetime = datetime.utcnow()

        user = User(
            email=form.email.data.lower(),
            password_hash=generate_password_hash(form.password2.data),
            member_since=current_datetime
        )

        db.session.add(user)
        db.session.commit()
        flash('Your account have been created successfully!', 'success')
        return redirect(url_for('auth.admin_login'))

    return render_template('auth/admin/register.html', form=form)

@auth.route('/become_an_ambassador/', methods=['GET', 'POST'])
def register_ambassador_interest():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            full_name = data.get('full_name')
            email = data.get('email')
            esperance = data.get('earning_range')
            institution = data.get('college_name')
            impact = data.get('bring_people_count')
            hidden_country_code = data.get('hiddenCountryCode')
            phone_code = data.get('phoneCode')

            phone_number = hidden_country_code + phone_code if hidden_country_code and phone_code else None

            six_digit_code = data.get('six_digit_code')

            if six_digit_code:
                ambassador = Ambassadors(
                    full_name=full_name,
                    email=email,
                    esperance=esperance,
                    institution=institution,
                    impact=impact,
                    phone_number=phone_number,
                    code=six_digit_code,
                    member_since=datetime.utcnow()
                )
                print(full_name, email, esperance, institution, impact, phone_number, six_digit_code, hidden_country_code)
                db.session.add(ambassador)
                db.session.commit()

                return jsonify({'success': True, 'message': 'Ambassador registration successful'})
            else:
                return jsonify({'success': False, 'message': 'Six-digit code is required'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})

    return render_template('employees/publishers.html')