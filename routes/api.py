from flask import Blueprint, request
from flask_login import login_required, current_user
import apis as api

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route("/search/<query>")
def search(query):
    res = api.kodik.search(query)
    return res, 200


@api_bp.route("/title/<int:title_id>/translations")
def title_translations(title_id):
    res = api.kodik.get_info(title_id)
    if res is None:
        return "None", 404
    return res, 200


@api_bp.route("/title/<int:title_id>/info")
@login_required
def title_info(title_id):
    res = api.shikimori.get_title_info(title_id, current_user.shiki_access_token)
    return res, 200


@api_bp.route("/title/<int:title_id>/related")
@login_required
def title_related(title_id):
    res = api.shikimori.get_title_related(title_id, current_user.shiki_access_token)
    return res, 200


@api_bp.route("/title/<int:title_id>/watch")
@login_required
def title_watch(title_id):
    translation = request.args.get('transl')
    episode = request.args.get('ep')
    if translation is None or episode is None:
        return "translation and/or episode is none", 400
    out = {}

    # kodik
    res = api.kodik.watch_link(title_id, episode, translation)
    out['kodik'] = {
        "360p": res + "360.mp4:hls:manifest.m3u8",
        "480p": res + "480.mp4:hls:manifest.m3u8",
        "720p": res + "720.mp4:hls:manifest.m3u8",
    }
    # anilibria
    if translation == "610" or translation == "3861":
        original_name = api.shikimori.get_title_info(title_id, current_user.shiki_access_token)['original_name']
        anilibria_id = api.anilibria.get_anime_id(original_name)
        if anilibria_id:
            all_episodes = api.anilibria.get_episodes(anilibria_id)
            out['anilibria'] = all_episodes[int(episode)]
    return out, 200
