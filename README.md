# Youtube Scripts Compilation
Просто сборник скриптов для массового скачивания музыки с ютуба.

------------

- `authroize.py`
Удобный скрипт для "авторизации". Он тащит Cookie ютуба из вашего браузера (указывается внутри скрипта) и сохраняет в файл **cookies.txt**. Этот файл будут использовать и остальные скрипты, так что обычно первым запускается именно он.

- `get_likes.py`
Получает список видео из вашего плейлиста "Понравившиеся". Автоматом сохраняет его в файл **list.txt**, что будет использован в **youtube_titles_parser.py** и **downlaoder.py**

- `youtube_titles_parser.py`
Получает названия по ссылкам на видео, что хранятся в **list.txt**. Не создаёт нового файла, а перезаписывает существующий. Лучше использовать этот скрипт после **downloader.py**

- `downloader.py`
Собственно скачивает видео с ютуба и автоматически преобразует их в mp3, запихивая в них превью и информацию о песне. По дефолту делает это в 10 процессов через multiprocessing. Настраивается внутри файла. По дефолту дёргает ссылки из **list.txt**

# requirements.txt
> eyed3==0.9.7
> grequests==0.7.0
> lxml==5.3.0
> moviepy==2.1.2
> yt_dlp==2025.3.27

в теории можно обойтись без grequests и lxml. Просто я решил что **youtube_titles_parser** в принципе может быть автономен от **yt_dlp**. Если кому-то будет не лень, то напишите свой скрипт, что будет основан на **yt_dlp**, но я сомневаюсь, что он будет быстрее. 
