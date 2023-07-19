#!/usr/bin/env python

import scanner, requests

target_url = 'https://www.sample.com'
login_url = 'https://www.sample.com/login.php'
links_to_ignore = 'https://www.sample.com/logout.php'
data_dict = {
    'username': 'test',
    'password': 'test',
    'login': 'submit'
}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post(login_url, data=data_dict)
vuln_scanner.crawl()
vuln_scanner.run_scanner()