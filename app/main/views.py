from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import main

@main.route('/details/formation/cours/')
def course_details():
	return render_template('main/photoshop.html')
