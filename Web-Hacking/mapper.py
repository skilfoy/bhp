import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg", ".gif", ".png", ".css"] ### file extensions not fingerprinted
TARGET = sys.argv[1]
THREADS = 10

answers = queue.Queue()
web_paths = queue.QUEUE()

def gather_paths():
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory back to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2)  ### your target may have throttling/lockout
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+ f{answers.get()}\n')  ###  f{answers.get()}\n should display hits in stdout, otherwise may need modification
        else:
            sys.stdout.write('x')
        sys.stdout.flush()

def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        thread.join()

if __name__ == '__main__':
     ### make sure this is the appropriate context for your machine, this is the directory where the code will execute
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()
    input('Press return to continue')

    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')