#!/usr/bin/python
import requests, re
from urllib.parse import urljoin

#TODO needs to stop searching with sub or dir search if crawler already found url

def main():
    crawler = Crawler('google-gruyere.appspot.com/433647619115470956373680989044218980405')
    crawler.start()

class Crawler:
    def __init__(self, url):
        self.url = url
        self.target_links = set()

    def start(self):
        self.spider(f'https://{self.url}')
        self.full_search()
        print(f'[+] Search Complete.\n[+] Full site listing as follows:\n' + '\n'.join(self.target_links))

    def full_search(self):
        previous_string = ''
        try:
            print('[+] Starting directory search with default URL...')
            self.dir_search(f'https://{self.url}')
            print(' '.ljust(len(previous_string)) + '\r')
            
            print('[+] Starting subdomain search...')
            with open('short_sample_wordlist.txt', 'r') as wordlist_file:
                for line in wordlist_file:
                    word = line.strip()
                    full_url = f'https://{word}.{self.url}'

                    # Dynamic updating:
                    print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                    previous_string = f'Current search: {full_url}'

                    response = self.request(full_url)
                    if response:
                        print(f'[+] Subdomain found at {full_url}')
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
                try:
                    if flag == 'Failed':
                        return
                except Exception:
                    pass

                word = line.strip()
                full_url = f'{url}/{word}'

                split_url = full_url.split('/')
                if split_url[-1] == split_url[-2]:
                    print(f'    [!] Potential limitless redirect at {full_url}')
                    return 'Failed'

                # Dynamic updating:
                print(f'Current search: {full_url.ljust(len(previous_string))}\r', end='')
                previous_string = f'Current search: {full_url}'

                response = self.request(full_url)

                if response:
                    print(f'    [+] Directory found: {full_url}')
                    self.spider(full_url)
                    self.target_links.add(full_url)
                    flag = self.dir_search(full_url)

    def request(self, url):
        try:
            return requests.get(f'{url}', timeout=2)
        except Exception:
            pass

    def spider(self, url):
        response = self.request(url)
        href_links = re.findall(r'(?:href=")(.*?)"', response.content.decode(errors='ignore')) + re.findall(r"(?:href=')(.*?)'", response.content.decode(errors='ignore'))
        for link in href_links:
            link = urljoin(url, link)
            link = link.split('?')[0]
            if '#' in link:
                link = link.split('#')[0]
            if self.url in link:
                if link not in self.target_links:
                    self.target_links.add(link)
                    print(f'        [+] Added {link} from spider function.')
                    self.spider(link)

if __name__ == '__main__':
    main()