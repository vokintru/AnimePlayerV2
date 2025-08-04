from anime_parsers_ru import KodikParser
from anime_parsers_ru.errors import NoResults

import lxml # ОБЯЗАТЕЛЬНО!!!
kodik_parser = KodikParser(use_lxml=True)  # В некоторых случаях lxml может не работать, можно перейти на стандартный парсер от bs4 прописав False


def get_info(title_id):
    try:
        res = kodik_parser.get_info(title_id, 'shikimori')
    except NoResults:
        return None
    return res


def search(query):
    result = kodik_parser.search(query, limit=50)
    out = []
    for res in result:
        if res['shikimori_id'] is not None:
            print(res)
            out.append({
                'name': res['title'],
                'type': res['material_data']['anime_kind'],
                'status': res['material_data']['all_status'],
                'episodes_released': res['material_data']['episodes_aired'],
                'episodes_total': res['material_data']['episodes_total'],
                'poster_url': res['material_data']['poster_url']
            })
            pass
    return out


def watch_link(title_id, seria_num, translation_id):
    return kodik_parser.get_link(title_id, "shikimori", seria_num, translation_id)[0]


if __name__ == '__main__':
    print(get_info(34881))
