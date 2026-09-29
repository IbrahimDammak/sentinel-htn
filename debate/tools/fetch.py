"""Failure-tolerant HTTP helper for the debate agents.

    import sys; sys.path.insert(0, r'E:\\bureau\\cardiacAttackDetectionHakathon\\debate\\tools')
    from fetch import get, get_json

Retries timeouts, 429/5xx and non-JSON bodies (overload/rate-limit HTML pages) with
exponential backoff, and returns None instead of raising, so one bad query never kills a batch.
"""
import time

import requests

S = requests.Session()
S.headers['User-Agent'] = 'Mozilla/5.0 (debate-research)'
RETRY = {429, 500, 502, 503, 504}


def get(url, params=None, tries=4, timeout=30):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code not in RETRY:
                return None
        except requests.RequestException:
            pass
        if i < tries - 1:
            time.sleep(2 ** i)
    return None


def get_json(url, params=None, tries=4, timeout=30):
    for i in range(tries):
        r = get(url, params, 1, timeout)
        if r is not None:
            try:
                return r.json()
            except ValueError:
                pass
        if i < tries - 1:
            time.sleep(2 ** i)
    return None


if __name__ == '__main__':
    d = get_json('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
                 {'db': 'pubmed', 'term': 'cuffless blood pressure', 'mindate': 2023, 'maxdate': 2026,
                  'datetype': 'pdat', 'retmode': 'json'})
    assert d and int(d['esearchresult']['count']) > 0, d
    assert get('https://api.crossref.org/works/10.9999/does-not-exist', tries=1) is None
    print('fetch ok, hits:', d['esearchresult']['count'])
