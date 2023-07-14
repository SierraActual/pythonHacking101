#!/usr/bin/python
import requests

def main():
    crawler = Crawler('google.com')
    crawler.start()

class Crawler:
    def __init__(self, url):
        self.url = url

    def start(self):
        print('[+] Starting directory search with default URL...')
        self.dir_search(f'http://{self.url}')
        
        print('[+] Starting subdomain search...')
        with open('sample_wordlist.txt', 'r') as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                full_url = f'{word}.{self.url}'
                response = self.request(full_url)
                if response:
                    print(f'[+] {full_url} status: {response}\n[+] Searching for additional directories...')
                    self.dir_search(full_url)

    def dir_search(self, url):
        with open('sample_dirlist.txt', 'r') as dir_list:
            for line in dir_list:
                word = line.strip()
                full_url = f'{url}/{word}'
                response = self.request(full_url)
                if response:
                    print([+] Directory found: {full_url})
                    self.dir_search(full_url)

    def request(self, url):
        try:
            return requests.get(f'http://{url}', timeout=5)
        except Exception:
            pass

if __name__ == '__main__':
    main()