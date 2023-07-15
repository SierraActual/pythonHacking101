#!/usr/bin/python
import requests, re
from urllib.parse import urljoin

#TODO needs work on detection

def main():
    crawler = Crawler('google.com')
    crawler.start()

class Crawler:
    def __init__(self, url):
        self.url = url
        self.target_links = set()

    def start(self):
        self.full_search()
        print(f'[+] Search Complete.\n[+] Full site listing as follows:\n' + '\n'.join(self.target_links))

    def full_search(self):
        try:
            print('[+] Starting directory search with default URL...')
            self.dir_search(f'https://{self.url}')
            
            print('[+] Starting subdomain search...')
            with open('short_sample_wordlist.txt', 'r') as wordlist_file:
                previous_string = ''
                for line in wordlist_file:
                    word = line.strip()
                    full_url = f'https://{word}.{self.url}'

                    # Dynamic updating:
                    print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                    previous_string = f'Current search: {full_url}'

                    response = self.request(full_url)
                    if response:
                        print(f'[+] {full_url} status: {response}\n    [+] Searching for additional directories...')
                        self.target_links.add(full_url)
                        self.spider(full_url)
                        self.dir_search(full_url)
        except KeyboardInterrupt:
            print('\n[+] Interrupt detected. Exiting...')
            exit()

    def dir_search(self, url):
        with open('short_sample_dirlist.txt', 'r') as dir_list:
            previous_string = ''
            for line in dir_list:
                word = line.strip()
                full_url = f'{url}/{word}'

                # Dynamic updating:
                print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                previous_string = f'Current search: {full_url}'

                response = self.request(full_url)
                print(f'history: \n{response.history}')


                if response.status_code == 404:
                    continue

                if response:
                    print(f'    [+] Directory found: {full_url}')
                    self.spider(full_url)
                    self.target_links.add(full_url)
                    self.dir_search(full_url)

    def request(self, url):
        try:
            return requests.get(f'{url}', timeout=2)
        except Exception:
            pass

    def spider(self, url):
        response = requests.get(url)
        href_links = re.findall(r'(?:href=")(.*?):"', response.content.decode())
        for link in href_links:
            link = urljoin(url, link)
            if url in link:
                self.target_links.add(link)

if __name__ == '__main__':
    main()