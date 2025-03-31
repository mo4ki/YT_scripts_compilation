import grequests
from lxml.html import fromstring

def normalize_links(links: str):

    links = links.replace('music.', 'www.').strip().split('\n')
    return [link[:43] for link in links]

def make_requests(urls: list) -> list:

    rs = (grequests.get(u) for u in urls)
    _requests = grequests.map(rs)
    [_requests.remove(r) for r in _requests if not r]

    return _requests,  _requests.count(None)

def parse_titles(requests: list) -> str:

    titles = []

    for request in requests:
    
        tree = fromstring(request.text)
        title = tree.findtext('.//title')[:-10]
        titles.append(title)
        
    return titles

def generate_text(music_links: list, titles: list, none_amount: int) -> str:

    text = ''
    for link, title in zip(music_links, titles):

        link = link.replace('www.', 'music.')
        text += f'{link} - {title}\n'
    
    return text.strip()

def open_file(filename, mode='r', encoding='utf-8'):

    try:
        return open(filename, mode, encoding=encoding)
    
    except Exception as e:

        print(f"Error: {e}")
        print("Input file couldn't be opened.")
        exit()

def main(in_filename, out_filename):
    
    # try:

    with open_file(in_filename) as f:
        music_links = f.read()
        
    music_links = normalize_links(music_links)
    requests, none_amount = make_requests(music_links)
    titles = parse_titles(requests)
    text = generate_text(music_links, titles, none_amount)

    with open_file(out_filename, 'w') as f:
        f.write(text)

    print(text)
    print(f"{none_amount} - none's amount")


if __name__ == '__main__':

    in_filename = 'list.txt'
    out_filename = 'list.txt'

    main(in_filename, out_filename)