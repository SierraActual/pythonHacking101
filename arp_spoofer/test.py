import time

timed = 0
try:
    while True:
        timed += 1
        print(f'\r[+] Sent two spoofed packets to {timed}', end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[+] Exiting...')

