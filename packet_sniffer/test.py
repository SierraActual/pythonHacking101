import time

try:
    while True:
        print('1')
        time.sleep(2)
except KeyboardInterrupt:
    print('stop')