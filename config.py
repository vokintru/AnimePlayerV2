import urllib

# Flask App
GLOBAL_URL = 'http:///192.168.1.107:8086'
SECRET_KEY = "oPWUQyDMY8QX-ToLzwQ2LEUeqoGz4CY6"

# Shikimori App
SHIKI_APP_ID = 'VgAjVlsH2AKHN9gfc_PLeKffViL6oc7yT4tR3nX5aXI'
SHIKI_APP_SECRET = 'DQeLPzgpNrSMoNILk-7q8dP_5SLGW-8n7yGcrzWUXtM'
SHIKI_AUTH_LINK = f"https://shikimori.one/oauth/authorize?client_id=VgAjVlsH2AKHN9gfc_PLeKffViL6oc7yT4tR3nX5aXI&redirect_uri={urllib.parse.quote(f'{GLOBAL_URL}/shiki_callback', safe='')}&response_type=code&scope=user_rates"

# Shikimori API
SHIKI_USERAGENT = 'v0k1nt.su search'

# Kodik
KODIK_TOKEN = "447d179e875efe44217f20d1ee2146be"
