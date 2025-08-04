import requests

def get_anime_id(name):
    res = requests.get(f'https://aniliberty.top/api/v1/anime/catalog/releases?f%5Bsearch%5D={name}&limit=1')
    if res.json()['data'][0]['name']['english'] == name:
        return res.json()['data'][0]['id']
    else:
        return None

def get_episodes(title_id):
    res = requests.get(f'https://aniliberty.top/api/v1/anime/releases/{title_id}')
    episodes = {}
    for episode in res.json()["episodes"]:
        data = {
            '480p': episode["hls_480"],
            '720p': episode["hls_720"],
            '1080p': episode["hls_1080"],
        }
        episodes[episode["ordinal"]] = {
            key: value.replace("countryIso=RU", "countryIso=DE")
            for key, value in data.items()
            if value is not None
        }
    return episodes
