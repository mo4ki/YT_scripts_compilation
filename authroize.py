from yt_dlp.cookies import extract_cookies_from_browser
from http.cookiejar import MozillaCookieJar
import os

# --- Константы ---
SAVED_COOKIES_FILE = 'cookies.txt'

# --- Настройки ---
BROWSER_FOR_COOKIES = 'firefox, chrome, edge' # Браузер(ы) для поиска cookies (через запятую)
BROWSER_PROFILE = None         # Профиль браузера (если не стандартный)
BROWSER_CONTAINER = None       # Контейнер Firefox (если используется)
# ---------------


def save_cookies(cookiejar, filename):
    '''Сохраняет cookies в файл Netscape формата. Возвращает True/False.'''
    
    saver = MozillaCookieJar(filename)
    youtube_cookies_count = 0
    for cookie in cookiejar:
        if cookie.domain.endswith('.youtube.com'):
            saver.set_cookie(cookie)
            youtube_cookies_count += 1
    try:
        saver.save(ignore_discard=True, ignore_expires=True)
        print(f'[*]. Сохранено {youtube_cookies_count} YouTube cookies.')
        return True
    except Exception:
        return False
    
def main():
    # 1. Извлечение Cookies
    cookies = None
    browser_info = 'не найден'
    browsers = [b.strip().lower() for b in BROWSER_FOR_COOKIES.split(',')]
    for browser in browsers:
        # try:
            _cookies = extract_cookies_from_browser(browser, profile=BROWSER_PROFILE, container=BROWSER_CONTAINER)
            if _cookies:
                cookies = _cookies
                browser_info = f'{browser} (Профиль: {BROWSER_PROFILE or "стандартный"})'
                break
        # except:
        #     pass

    if not cookies:
        print(f'[*]. Не удалось извлечь cookies из указанных браузеров ({BROWSER_FOR_COOKIES}).')
        print(f'[*]. Убедитесь, что вы вошли в YouTube.')
        return False
    
    if save_cookies(cookies, SAVED_COOKIES_FILE): # 2. Сохранение Cookies
        print(f'[*]. Cookie из "{browser_info}", сохранены в "{SAVED_COOKIES_FILE}"')
        return True
    return False

if __name__ == '__main__':
    if not main():
        exit(1)
