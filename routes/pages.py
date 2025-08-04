from flask import Blueprint, request, render_template, redirect
from flask_login import login_required, current_user
import config
import urllib

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
@login_required
def home():
    if current_user.subed:
        error = request.args.get('error', default=None)
        return render_template("index.html", shiki_requiered=current_user.shiki_access_token is None, url=config.SHIKI_AUTH_LINK, error=error)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@main_bp.route("/search")
@login_required
def search():
    if current_user.subed:
        title = request.args.get('title', default=None)
        return render_template("index.html", shiki_requiered=current_user.shiki_access_token is None, url=config.SHIKI_AUTH_LINK, error=error)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')
