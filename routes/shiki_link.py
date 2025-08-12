from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
import requests
import config
from data import db_session
from data.user import User

shiki_auth_bp = Blueprint('shiki_auth', __name__)

@shiki_auth_bp.route("/shiki_callback")
@login_required
def shiki_callback():
    code = request.args.get('code')
    r = requests.post('https://shikimori.one/oauth/token',
                      headers={'User-Agent': 'v0k1nt.su search'},
                      params={'grant_type': 'authorization_code',
                              'client_id': config.SHIKI_APP_ID,
                              'client_secret': config.SHIKI_APP_SECRET,
                              'code': code,
                              'redirect_uri': f'{config.GLOBAL_URL}/shiki_callback'})
    if r.ok and r.json():

        if r.json()['scope'] != 'user_rates':
            return redirect('/?error=Вы не приняли Scopes!')
        else:
            resp = r.json()
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.shiki_access_token = resp['access_token']
            user.shiki_refresh_token = resp['refresh_token']
            r = requests.get('https://shikimori.one/api/users/whoami',
                      headers={'User-Agent': 'v0k1nt.su search',
                               'Authorization': f'Bearer {user.shiki_access_token}'})
            user.shiki_user_id = r.json()['id']
            db_sess.commit()
            db_sess.close()
            return redirect('/')
    return 'Ошибка авторизации', 401