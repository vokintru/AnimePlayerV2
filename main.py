from flask import Flask, render_template, request, redirect, abort, send_file, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.user import User
import os
import requests
import datetime
import urllib.parse

app = Flask(__name__)
app.secret_key = "oPWUQyDMY8QX-ToLzwQ2LEUeqoGz4CY6"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.remember_cookie_duration = False
login_manager.login_view = 'login'
global_url = 'http://192.168.1.107:8086'

SHIKI_APP_ID = 'VgAjVlsH2AKHN9gfc_PLeKffViL6oc7yT4tR3nX5aXI'
SHIKI_APP_SECRET = 'DQeLPzgpNrSMoNILk-7q8dP_5SLGW-8n7yGcrzWUXtM'

@app.route("/")
@login_required
def home():
    if current_user.subed:
        error = request.args.get('error', default=None)
        if current_user.shiki_access_token is None:
            callback_url = f'{global_url}/shiki_callback'
            url = f"https://shikimori.one/oauth/authorize?client_id=VgAjVlsH2AKHN9gfc_PLeKffViL6oc7yT4tR3nX5aXI&redirect_uri={urllib.parse.quote(callback_url, safe='')}&response_type=code&scope=user_rates"
            return render_template("index.html", shiki_requiered=True, shiki_url=url, error=error)
        else:
            return render_template("index.html", error=error)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@app.route("/login")
def login():
    url = f"{global_url}/auth"
    return redirect(f'https://v0k1nt.su/auth/authorize?next={url}')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    ret = db_sess.query(User).filter(User.id == user_id).first()
    db_sess.close()
    return ret

@app.route("/auth")
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
                modified_date=datetime.datetime.now(),
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

@app.route("/shiki_callback")
@login_required
def shiki_callback():
    code = request.args.get('code')
    r = requests.post('https://shikimori.one/oauth/token',
                      headers={'User-Agent': 'v0k1nt.su search'},
                      params={'grant_type': 'authorization_code',
                              'client_id': SHIKI_APP_ID,
                              'client_secret': SHIKI_APP_SECRET,
                              'code': code,
                              'redirect_uri': f'{global_url}/shiki_callback'})
    if r.ok and r.json():

        if r.json()['scope'] != 'user_rates':
            return redirect('/?error=Вы не приняли Scopes!')
        else:
            resp = r.json()
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.shiki_access_token = resp['access_token']
            user.shiki_refresh_token = resp['refresh_token']
            db_sess.commit()
            db_sess.close()
            return redirect('/')
    return 'Ошибка авторизации', 401

@app.route('/resources/<string:path>')
def resources(path: str):
    if os.path.exists(f'resources\\{path}'):  # Windows-like
        return send_file(f'resources\\{path}')
    elif os.path.exists(f'resources/{path}'):  # Unix
        return send_file(f'resources/{path}')
    else:
        return abort(404)


if __name__ == "__main__":
    db_session.global_init("database.db")
    app.run(host='0.0.0.0', port='8086')
