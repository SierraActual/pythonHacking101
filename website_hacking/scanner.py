#!/usr/bin/env python

import requests, re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links
        self.xss_script = '<sCript>alert("Hello")</scrIpt>'

    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall(r'(?:href=")(.*?)"', response.content.decode(errors='ignore'))

    def crawl(self, url=None):
        if url == 'None':
            url = self.target_url

        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urljoin(url, link)

            if '#' in link:
                link = link.split('#')[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content, features='lxml')
        return parsed_html.findAll('form')

    def submit_forms(self, form, value, url):
        post_data = {}
        action = form.get('action')
        post_url = urljoin(self.target_url, action)
        method = form.get('method')

        inputs_list = form.findAll('input')
        for input in inputs_list:
            input_name = input.get('name')
            input_type = input.get('type')
            input_value = input.get('value')
            if input_type == 'text':
                input_value = value
            post_data[input_name] = input_value
        if method == 'post':
            return requests.post(post_url, data=post_data)
        return requests.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)

            for form in forms:
                print(f'\n\n[+] Testing form in {link}')
                is_vuln_xss_form = self.test_xss_in_form(form, link)
                if is_vuln_xss_form:
                    print(f'[***] Discovered XSS vulnerability at {link} in the following form:')
                    print(form)

            if '=' in link:
                print(f'\n\nTesting {link}')
                is_vuln_xss_link = self.test_xss_in_url(link)
                if is_vuln_xss_link:
                    print(f'[***] Discovered XSS vulnerability in {link}')

    def test_xss_in_form(self, form, url):
        response = self.submit_forms(form, self.xss_script, url)
        return self.xss_script in response.content.decode(errors='ignore')

    def test_xss_in_url(self, url):
        url = url.replace('=', f'={self.xss_script}')
        response = self.session.get(url)
        return self.xss_script in response.content.decode(errors='ignore')
