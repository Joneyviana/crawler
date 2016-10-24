import requests
import tqdm
import collections
import time
from concurrent import futures


def print_content(url):
    r = requests.get(url)


def request_many(urls,callback=print_content):
    responses_no_problems = 0
    errors = 0
    not_founds = 0
    with futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:  # <6>
        to_do_map = {}  # <7>
        for url in sorted(urls):  # <8>
            future = executor.submit(callback, url)  # <9>
            to_do_map[future] = url  # <10>
        done_iter = futures.as_completed(to_do_map)  # <11>
        done_iter = tqdm.tqdm(done_iter, total=len(urls))  # <12>
        for future in done_iter:  # <13>
            try:
                res = future.result()  # <14>
            except requests.exceptions.HTTPError as exc:  # <15>
                errors += 1
            except requests.exceptions.ConnectionError as exc:
                not_founds += 1
            else:
                responses_no_problems += 1

    print("{} successes {} errors {} not found".format(
        responses_no_problems, errors, not_founds))

def request_status(func):
    def func_wrapper(urls):
        start = time.time()
        func(urls)
        elapsed = time.time() - start
        print('Elapsed time: {:.2f}s with {}'.format(elapsed,func.__name__))
    return func_wrapper


