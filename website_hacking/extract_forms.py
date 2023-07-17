#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def main():
    form_extractor = Form_Extractor('https://google-gruyere.appspot.com/433647619115470956373680989044218980405/login')
    form_extractor.start()

class Form_Extractor:
    def __init__(self, url):
        self.url = url

    def start(self):
        response = self.request(self.url)
        parsed_html = BeautifulSoup(response.content, features='lxml')
        forms_list = parsed_html.findAll('form')

        post_data = {}

        for form in forms_list:
            action = form.get('action')
            post_url = urljoin(self.url, action)
            method = form.get('method')
            inputs_list = form.findAll('input')
            for input in inputs_list:
                input_name = input.get('name')
                input_type = input.get('type')
                input_value = input.get('value')
                if input_type == 'text':
                    input_value = 'test'
                post_data['input_name'] = input_value
            response = requests.post(post_url, data=post_data)
            print(response.content)

    def request(self, url):
        try:
            return requests.get(f'{url}', timeout=2)
        except Exception:
            pass


if __name__ == '__main__':
    main()