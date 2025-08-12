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
        return render_template("index.html", shiki_requiered=current_user.shiki_access_token is None, shiki_url=config.SHIKI_AUTH_LINK, error=error)
    else: 
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@main_bp.route("/shiki_auth_link")
@login_required
def shiki_auth_link():
    return redirect(config.SHIKI_AUTH_LINK)

@main_bp.route("/search")
@login_required
def search():
    if current_user.subed:
        query = request.args.get('query', default=None)
        return render_template("search.html", query=query)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@main_bp.route("/search/<string:query>")
@login_required
def search_with_query(query):
    if current_user.subed:
        return render_template("search.html", query=query)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@main_bp.route("/release/<int:release_id>")
@login_required
def release(release_id):
    if current_user.subed:
        return render_template("release.html", release_id=release_id)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')

@main_bp.route("/watch/<int:title_id>/<int:translation_id>")
@login_required
def watch(title_id, translation_id):
    if current_user.subed:
        return render_template("watch.html", title_id=title_id, translation_id=translation_id)
    else:
        return redirect('https://v0k1nt.su/?error=Не оформлена подписка!')


#old ways

@main_bp.route("/release")
def old_release():
    release_id = request.args.get('id', default=None)
    return redirect(f'/release/{release_id}', code=301)