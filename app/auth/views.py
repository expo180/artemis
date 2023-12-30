# auth/views.py
from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Students
from werkzeug.security import generate_password_hash
from .forms import CourseWorkRegistrationForm
from .. import rapi 
from datetime import datetime

@auth.route('/set_locale', methods=['GET', 'POST'])
def set_locale():
    if request.method == 'POST':
        selected_language = request.form.get('locale')
        if selected_language and selected_language in current_app.config['LANGUAGES']:
            session['locale'] = selected_language
            print(session['locale'])
    else:
        user_languages = request.headers.get('Accept-Language')
        preferred_language = determine_language(user_languages)
        session['locale'] = preferred_language

    return redirect(request.referrer or url_for('auth.register'))

def determine_language(user_languages):
    user_languages = [lang.strip() for lang in user_languages.split(',')]
    print(user_languages)
    
    supported_languages = ['en', 'fr', 'ja', 'ar', 'it', 'es', 'pt', 'ru', 'pl']
    
    for lang in user_languages:
        primary_language = lang.split('-')[0]
        if primary_language in supported_languages:
            return primary_language
    
    return 'en'

    
@auth.route("/s'incrire/formation/", methods=['GET', 'POST'])
def register():
    form = CourseWorkRegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user:
            # Display a flash message for existing email
            flash('Account already exists. Please log in.', 'error')
            return redirect(url_for('auth.register'))

        current_datetime = datetime.utcnow()

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data.lower(),
            country=form.country.data
        )

        db.session.add(user)
        db.session.commit()

        # Save user data in the session for template usage
        session['user_data'] = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data.lower(),
            'country': form.country.data,
            'age': form.age.data,
            'areas_of_interest': form.areas_of_interest.data,
            'gender': form.gender.data,
            'member_since': current_datetime
        }

        # Display a flash message for successful registration
        return redirect(url_for('main.register_success'))

    return render_template('auth/register.html', form=form)