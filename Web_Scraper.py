#!/usr/bin/env python3

import requests
import concurrent.futures
import re

def scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>',
                              response.text, re.DOTALL)

        return list(map(lambda x: re.sub(r'<[^>]+>', '', x).strip(), headings))

    except requests.RequestException as error:
        print(error)
        return []

import time

def main():
    base = "https://30124.williamtheisen.com"
    urls = [f"{base}/reading_{i:02}.html" for i in range(1, 6)]

    for workers in [1, 5]:
        start = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(scrape, urls))

        elapsed = time.perf_counter() - start

        print(f"{workers} worker(s): {elapsed:.3f} seconds")

        for url, headings in zip(urls, results):
            print(f"\n{url}")
            for heading in headings:
                print(heading)


if __name__ == "__main__":
    main()
