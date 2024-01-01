from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import api

@api.route('/paiement/formation/')
def payment():
	return render_template('apis/payment.html')

@api.route('/autre/paiement/')
def other_payment_options():
	return render_template('apis/other_payment_options.html')