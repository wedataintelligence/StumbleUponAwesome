import urllib.request
import urllib.error
import os
import threading
"""
This file is for removing URLs which are invalid, lead to 404, timeout or other errors.
"""
all_urls = []
valid_urls = []
http_errors = []
other_errors = []
chunks = []

def clean_chunk(idx, chunk):
    for url in chunk:
        try:
            all_urls.append(url)
            conn = urllib.request.urlopen(url, timeout=5)
        except urllib.error.HTTPError as e:
            http_errors.append(url)
        except urllib.error.URLError as e:
            other_errors.append(url)
        else:
            valid_urls.append(url)
        print("\rTotal urls: {}  Valid urls: {} Invalid urls: {}  HTTP errors: {}  Other errors: {}" \
              .format(len(all_urls), len(valid_urls), len(all_urls) - len(valid_urls), len(http_errors), len(other_errors)), end="")

def merge_chunks():
    with open ('../extension/urls_cleaned.txt', 'a') as f:
        for url in valid_urls:
            f.write(url)
    
if __name__ == "__main__":
    with open("../extension/urls.txt", 'r') as f:

        if os.path.exists("../extension/urls_cleaned.txt"):
            os.remove("../extension/urls_cleaned.txt")

        urls = f.readlines()
        chunks = [urls[x:x+100] for x in range(0, len(urls), 100)]
        threads = [threading.Thread(target=clean_chunk,args=(idx, chunk)) for idx, chunk in enumerate(chunks)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        merge_chunks()
