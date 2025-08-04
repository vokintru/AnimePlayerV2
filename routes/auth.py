from flask import Blueprint, redirect, request
import config
import requests
from datetime import datetime, timedelta, timezone
from flask_login import login_user
from data import db_session
from data.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login")
def login():
    url = f"{config.GLOBAL_URL}/auth"
    return redirect(f'https://v0k1nt.su/auth/authorize?next={url}')

@auth_bp.route("/auth")
def auth():
    token = request.args.get('token')
    r = requests.get('http://v0k1nt.su/auth/verify_token', params={'token': token})
    if r.ok and r.json().get('valid'):
        user_data = r.json()['user']
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(auth_id=user_data['id']).first()
        if not user:
            user = User(
                auth_id=user_data['id'],
                modified_date=datetime.now(),
                subed=user_data['subed']
            )
            db_sess.add(user)
            db_sess.commit()
            db_sess.refresh(user)
        user.subed = user_data['subed']
        db_sess.commit()
        login_user(user)
        db_sess.close()
        return redirect("/")
    return 'Ошибка авторизации', 401