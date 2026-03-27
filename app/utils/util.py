import os

from jose import jwt
from datetime import datetime, timedelta, timezone
import jose
from functools import wraps
from flask import request, jsonify
 

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-before-production')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Bearer <token>
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_customer_id = payload['sub']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_customer_id, *args, **kwargs)
    return decorated

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id),
        'role': 'customer'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def encode_token_mechanic(mechanic_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(mechanic_id),
        'role': 'mechanic'  # distinguishes mechanic tokens from customer tokens
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]  # Bearer <token>
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload.get('role') != 'mechanic':
                return jsonify({'message': 'Mechanic access required!'}), 403
            current_mechanic_id = payload['sub']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_mechanic_id, *args, **kwargs)
    return decorated