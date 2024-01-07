from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import main
from ..models import Students
from ..decorators import admin_required

@main.route('/details/formation/cours/')
def course_details():
	return render_template('main/photoshop.html')

@main.route('/admin/dashboard/')
@login_required
@admin_required
def admin_dashboard():
    students = Students.query.all()
    return render_template('main/admin.html', students=students)
