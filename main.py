from flask import Flask, abort, send_file
from routes import register_blueprints
from flask_login import LoginManager
from data import db_session
from data.user import User
import os
import config

app = Flask(__name__)
register_blueprints(app)
app.secret_key = config.SECRET_KEY

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.remember_cookie_duration = False
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    ret = db_sess.query(User).filter(User.id == user_id).first()
    db_sess.close()
    return ret


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
