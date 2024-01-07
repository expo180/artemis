from flask import render_template, redirect, request, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from . import api
from ..models import Students, UserSignature, OtherPaymentMehtodSubscribers
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, user_id, data):
    data_to_sign = f"{user_id}-{data}"

    message_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    message_hash.update(data_to_sign.encode('utf-8'))
    digest = message_hash.finalize()

    signature = private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.urlsafe_b64encode(signature).decode('utf-8')

@api.route('/autre/paiement/')
def other_payment_options():
    return render_template('apis/other_payment_options.html')


@api.route('/api/other_payment_submission', methods=['POST'])
def other_payment_submission():
    full_name = request.form.get('fullName')
    phone = request.form.get('phoneCode')
    subscriber = OtherPaymentMehtodSubscribers(
        full_name=full_name,
        phone=phone
    )

    db.session.add(subscriber)
    db.session.commit()

    return jsonify({'success': True})

@api.route('/api/change_status/<int:student_id>', methods=['POST'])
@login_required
def change_status(student_id):

    student = Students.query.get_or_404(student_id)

    user_id = student.id
    private_key, _ = generate_key_pair()
    signature = sign_data(private_key, user_id, 'status_change')

    user_signature = UserSignature.query.filter_by(user_id=user_id).first()

    if not user_signature:
        user_signature = UserSignature(user_id=user_id, signature=signature)
        print(user_signature)
        db.session.add(user_signature)

    else:
        user_signature.signature = signature

    student.status = True
    db.session.commit()

    return jsonify({'success': True})

@api.route('/submit_payment_form/', methods=['POST'])
def submit_payment_form():
    try:
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')

        subscriber = OtherPaymentMehtodSubscribers(full_name=full_name, phone=phone)
        db.session.add(subscriber)
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

