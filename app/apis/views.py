from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import api

@api.route('/autre/paiement/')
def other_payment_options():
	return render_template('apis/other_payment_options.html')


@api.route('/update/status/', methods=['POST'])
def update_status():
    try:
        phone_number = request.json.get('phone_number')
        user = Students.query.filter_by(phone_number=phone_number).first()
        if user:
            user.status = True
            db.session.commit()
            return jsonify({"message": "Status updated successfully."}), 200
        else:
            return jsonify({"message": "User not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
