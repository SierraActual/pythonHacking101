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
                previous_string = ''
                word = line.strip()
                full_url = f'{word}.{self.url}'

                # Dynamic updating:
                print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                previous_string = f'Current search: {full_url}\r'

                response = self.request(full_url)
                if response:
                    print(f'[+] {full_url} status: {response}\n    [+] Searching for additional directories...')
                    self.dir_search(full_url)

    def dir_search(self, url, visited_domains=set()):
        try:
            domain = url.split('/')[2]  # Extract the domain from the URL
            if domain in visited_domains:
                print(f'   [!] Infinite recursion detected at: {domain}')
                return

            visited_domains.add(domain)
        except Exception:
            pass

        with open('short_sample_dirlist.txt', 'r') as dir_list:
            previous_string = ''
            counter = 0
            for line in dir_list:
                if counter > 10:
                    print(f'      [!] Potential limitless domains at: {url}.')
                    return
                word = line.strip()
                full_url = f'{url}/{word}'

                # Dynamic updating:
                print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                previous_string = f'Current search: {full_url}\r'

                response = self.request(full_url)
                if response:
                    print(f'    [+] Directory found: {full_url}')
                    self.dir_search(full_url, visited_domains)
                    counter += 1
        try:
            visited_domains.remove(domain)  # Remove the domain from visited set after the recursion
        except Exception:
            pass

    def request(self, url):
        try:
            return requests.get(f'http://{url}', timeout=2)
        except Exception:
            pass

if __name__ == '__main__':
    main()