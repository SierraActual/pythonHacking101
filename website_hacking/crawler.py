#!/usr/bin/python
import requests

def main():
    crawler = Crawler('google.com')
    crawler.start()

class Crawler:
    def __init__(self, url):
        self.url = url

    def start(self):
        with open('sample_wordlist.list', 'r') as wordlist_file:
            for line in wordlist_file:
                word = word.strip
                full_url = f'{word}.{self.url}'
                print(f'{full_url} status: {self.request(full_url)}')

    def request(self, url):
        try:
            return get_response = requests.get(f'http://{url}')
        except requests.exceptions.ConnectionError:
            pass

if __name__ == '__main__':
    main()