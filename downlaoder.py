import os
import hashlib
from multiprocessing import Process
from moviepy.audio.io.AudioFileClip import AudioFileClip
from urllib.request import urlretrieve as download_file
import yt_dlp
import eyed3

proxy_handler = {
    # 'http': 'http://94.131.107.45:3128',
}

err_file = open('errors_logs.txt', 'a', encoding='utf-8')

# Function to generate a hash string from a given input
def generate_hash(input_str: str) -> str:

    hash_object = hashlib.sha1(input_str.encode())
    return hash_object.hexdigest()

def ensure_directory_exists(directory: str):

    if not os.path.exists(directory):
        os.makedirs(directory)

def download_song(url: str, music_path: str) -> tuple:
    try:
        # Конфигурация для yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(music_path, '%(title)s.%(ext)s'),
            'cookiefile': 'cookies.txt',
            'noplaylist': True,
        }
        
        # Получаем информацию о видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            uploader = info.get('uploader', 'Unknown Artist')
            thumbnail_url = info.get('thumbnail', None)
            
            # Загружаем видео
            out_file = ydl.prepare_filename(info)
            ydl.download([url])
            
            return out_file, title, uploader, thumbnail_url, url
            
    except Exception as e:
        err_file.write(f"Ошибка при загрузке {url}: {str(e)}\n")
        return None, None, None, None, url

def save_metadata(filepath: str, title: str, artist: str, cover_path: str, url: str):

    try:
        audio = eyed3.load(filepath)

        if audio is None:
            return

        if audio.tag is None:
            audio.initTag()

        audio.tag.title = title
        audio.tag.artist = artist
        audio.tag.album = artist  # Change in the future
        audio.tag.comments.set(url, description=u'YouTube URL')

        if os.path.exists(cover_path):
            data = open(cover_path, 'rb').read()
            audio.tag.images.set(3, data, 'image/jpeg')
            audio.tag.save(version=eyed3.id3.ID3_V2_3)
    except Exception as e:
        err_file.write(f"Ошибка при сохранении метаданных для {filepath}: {str(e)}\n")

def convert_to_mp3(filepath: str) -> str:

    try:
        base, ext = os.path.splitext(filepath)
        out = base + '.mp3'
        
        # Если файл уже в формате mp3, просто возвращаем путь
        if ext.lower() == '.mp3':
            return filepath
            
        FILETOCONVERT = AudioFileClip(filepath)
        FILETOCONVERT.write_audiofile(out)
        FILETOCONVERT.close()

        return out
    except Exception as e:
        err_file.write(f"Ошибка при конвертации в MP3 для {filepath}: {str(e)}\n")
        return filepath

def get_links(filename: str) -> list:

    with open(filename, encoding='utf-8') as file:

        links_raw = file.read()
        links_prepared = links_raw.strip().split('\n')
        links = []
        for line in links_prepared:
            parts = line.split(' ', 1)
            if parts and len(parts) > 0:
                links.append(parts[0])

    return links   

def split_list(lst: list, n: int) -> list:

    avg = len(lst) / float(n)
    out = []
    last = 0.0

    while last < len(lst):

        out.append(lst[int(last):int(last + avg)])
        last += avg

    if len(out) != n:
        out[-1].extend([None] * (n - len(out)))

    return out

def main(links, music_path):

    for link in links:
        try:
            if not link:
                continue
                
            # Загружаем видео и получаем информацию
            out_file, title, artist, thumbnail_url, url = download_song(link, music_path)
            
            if not out_file:
                continue
                
            # Загружаем миниатюру
            cover_path = music_path + generate_hash(thumbnail_url) + '.jpg' if thumbnail_url else None
            if thumbnail_url:
                try:
                    download_file(thumbnail_url, cover_path)
                except Exception as e:
                    err_file.write(f"Ошибка при загрузке обложки для {link}: {str(e)}\n")
                    cover_path = None

            # Конвертируем в MP3 если нужно
            mp3_file = convert_to_mp3(out_file)
            
            # Сохраняем метаданные
            if cover_path:
                save_metadata(mp3_file, title, artist, cover_path, url)
            
            # Удаляем временные файлы
            if out_file != mp3_file and os.path.exists(out_file):
                os.remove(out_file)
                
            if cover_path and os.path.exists(cover_path):
                os.remove(cover_path)
                
            print(f"Успешно загружено: {title}")
            
        except Exception as e:
            err_file.write(f"Общая ошибка для {link}: {str(e)}\n")
            continue

def start_workers(links: list, music_path: str, workers: int) -> list:

    lists = split_list(links, workers)
    processes = [Process(target=main, args=(lst, music_path)) for lst in lists]

    [p.start() for p in processes]
    [p.join() for p in processes]

    return processes

if __name__ == '__main__':

    music_path = './music/'
    filename = 'list.txt'
    links = get_links(filename)
    workers = 4  # Увеличено количество параллельных процессов
    
    ensure_directory_exists(music_path)
    processes = start_workers(links, music_path, workers)
