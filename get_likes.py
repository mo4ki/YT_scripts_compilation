import yt_dlp
import os

# --- Константы ---
COOKIES_FILE = 'cookies.txt'
LIKED_PLAYLIST_ID = 'LL'
# ----------------

def main(cookie_file):
    if not os.path.exists(cookie_file):
        print(f'[*]. Ошибка: Файл cookies не найден: {cookie_file}')
        return None

    ydl_opts = {
        'cookiefile': cookie_file,
        'quiet': True,
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'force_generic_extractor': True,
    }

    playlist = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(LIKED_PLAYLIST_ID, download=False)
            if playlist_info and 'entries' in playlist_info:
                playlist = playlist_info['entries']
            else:
                print('[*]. Ошибка: Не удалось получить плейлист или он пуст.')
                return None
    except Exception as e:
        print(f'[*]. Ошибка при получении плейлиста: {e}')
        return None
    
    urls = []
    for video in playlist:
        url = video.get('url') or \
              video.get('webpage_url') or \
              (f'https://www.youtube.com/watch?v={video["id"]}' if 'id' in video else None)
        
        url_str = url or 'Не найден'
        print(url_str)
        urls.append(url_str)
    
    # Сохраняем ссылки в файл
    with open('list.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(f'{url}\n')
    
    print(f'[*] Список из {len(urls)} ссылок сохранен в file list.txt')
    return True

if __name__ == '__main__':
    if not main(COOKIES_FILE):
        exit(1)