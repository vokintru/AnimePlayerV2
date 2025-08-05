import requests
import config
from data import db_session
from data.user import User


def request(protocol, url, headers: dict=None, data: dict=None):
    if protocol == "GET":
        try:
            resp = requests.get(url, headers=headers, data=data)
        except Exception as e:
            raise EOFError(f"Ошибка запроса: {e}")
    elif protocol == "POST":
        try:
            resp = requests.post(url, headers=headers, data=data)
        except Exception as e:
            raise EOFError(f"Ошибка запроса: {e}")
    else:
        raise EOFError("Протокол не поддерживается")
    if resp.status_code == 401 and resp.json() == {"error": "invalid_token",
                                                     "error_description": "The access token is invalid",
                                                     "state": "unauthorized"}:
        new_token = refresh_token(headers['Authorization'])
        if new_token['status'] == 'failure' and new_token['do'] == 'reauth':
            return 'reauth'
        elif new_token['status'] == 'success':
            headers['Authorization'] = f'Bearer {new_token["token"]}'
            return request(url, protocol, headers, data)
    elif resp.status_code == 200:
        return resp.json()
    else:
        raise EOFError(resp)


def refresh_token(token):
    try:
        resp = requests.post('https://shikimori.one/oauth/token',
                             headers={
                                 'User-Agent': config.SHIKI_USERAGENT
                             },
                             data={
                                 "grant_type": "refresh_token",
                                 "client_id": config.SHIKI_APP_ID,
                                 "client_secret": config.SHIKI_APP_SECRET,
                                 "refresh_token": token
                             })
    except Exception as e:
        return {'status': 'failure',
                'do': e}
    if resp.status_code == 400 and resp.json() == {'error': 'invalid_grant', 'error_description': 'The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.'}:
        return {'status': 'failure',
                'do': 'reauth'}
    rest_json = resp.json()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.shiki_refresh_token == token).first()
    user.shiki_access_token = rest_json['access_token']
    user.shiki_refresh_token = rest_json['refresh_token']
    db_sess.commit()
    db_sess.close()
    return {'status': 'success',
            'token': rest_json['access_token']}


def get_title_info(title_id, token):
    resp = request("GET", f"https://shikimori.one/api/animes/{title_id}",
                   headers={
                       'User-Agent': config.SHIKI_USERAGENT,
                       'Authorization': f'Bearer {token}'
                   })
    if resp == 'reauth':
        return {'error': 'reauth'}
    return {
        'name': resp['russian'],
        'original_name': resp['name'],
        'poster': 'https://shikimori.one' + resp['image']['original'],
        'type': resp['kind'],
        'score': resp['score'],
        'status': resp['status'],
        'total_episodes': resp['episodes'],
        'released_episodes': resp['episodes_aired'],
        'started': resp['aired_on'],
        'released': resp['released_on'],
        'rating': resp['rating'],
        'is_anons': resp['anons'],
        'is_ongoing': resp['ongoing'],
        'next_episode_at': resp['next_episode_at'],
        'user_rate': resp['user_rate']
    }

def get_title_related(title_id, token):
    resp = request("GET", f"https://shikimori.one/api/animes/{title_id}/related",
                   headers={
                       'User-Agent': config.SHIKI_USERAGENT,
                       'Authorization': f'Bearer {token}'
                   })
    if resp == 'reauth':
        return {'error': 'reauth'}
    related = []
    for relation in resp:
        related.append({
            'type': relation['relation_russian'],
            'anime': relation['anime'],
            'manga': relation['manga'],
        })
    return related

if __name__ == '__main__':
    #db_session.global_init("../database.db")
    print(get_title_related(34881, "RVgHiR_U9eAkUk_6BFw9U9G75tG9tGjOP6wkyhTxqc0"))
