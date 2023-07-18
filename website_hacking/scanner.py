#!/usr/bin/env python

import requests, re
from urllib.parse import urljoin

class Scanner:
    def __init__(self, url):
        self.target_url = url
        self.target_links = []

    def extract_links_from(self, url):
        response = requests.get(url)
        return re.findAll(r'(?:href=")(.*?)"', response.content.decode(errors='ignore'))

    def crawl(self, url=None):
        if url == 'None':
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urljoin.(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                self.crawl(link)