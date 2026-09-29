"""Machine pre-check of debate references.
Resolves DOI / PMID / arXiv IDs and flags: NO-ID, UNRESOLVED, PRE-2021,
YEAR-MISMATCH, TITLE-MISMATCH. Claim-vs-source checking stays with the human-style auditors.
Usage: python refcheck.py <out.md> <paper.md> [<paper.md> ...]   |   python refcheck.py --selftest
"""
import difflib, re, sys, time
import xml.etree.ElementTree as ET
import requests

REF = re.compile(r'^\W*\[([a-z_]+-\d+)\]\s*(.*)$')
DOI = re.compile(r'\b(10\.\d{4,9}/[^\s|;,<>"\]\)]+)', re.I)
PMID = re.compile(r'PMID[:\s]*(\d{5,9})', re.I)
ARX = re.compile(r'arXiv[:.\s]*(\d{4}\.\d{4,5})', re.I)
TITLE = re.compile(r'["“]([^"”]{10,})["”]')
YEAR = re.compile(r'\b(?:19|20)\d{2}\b')
S = requests.Session()
S.headers['User-Agent'] = 'debate-refcheck/1.0'


def parse(text):
    """-> {ref_id: entry_text}; an entry is its [slug-n] line plus continuation lines."""
    refs, cur = {}, None
    for line in text.splitlines():
        m = REF.match(line)
        if m:
            cur = m.group(1)
            if cur in refs and not (DOI.search(line) or PMID.search(line) or ARX.search(line)):
                cur = None  # keep the first entry that carries identifiers
                continue
            refs[cur] = m.group(2)
        elif cur and line.strip() and not line.lstrip().startswith(('#', '|')):
            refs[cur] += ' ' + line.strip()
        else:
            cur = None
    return refs


def get(url, **kw):
    time.sleep(0.35)  # ponytail: fixed pacing, fine for ~200 refs; add per-host backoff if 429s appear
    try:
        r = S.get(url, timeout=25, **kw)
        return r if r.status_code == 200 else None
    except requests.RequestException:
        return None


def crossref(doi):
    r = get(f'https://api.crossref.org/works/{doi}')
    if not r:
        h = get(f'https://doi.org/api/handles/{doi}')  # DataCite/other registrars
        return ('(exists, non-Crossref DOI)', None, '') if h and h.json().get('responseCode') == 1 else None
    m = r.json()['message']
    return ((m.get('title') or [''])[0], m.get('issued', {}).get('date-parts', [[None]])[0][0],
            (m.get('container-title') or [''])[0])


def pubmed(pmid):
    r = get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi',
            params={'db': 'pubmed', 'id': pmid, 'retmode': 'json'})
    d = r and r.json().get('result', {}).get(pmid)
    if not d or 'error' in d:
        return None
    y = YEAR.search(d.get('pubdate', ''))
    return d.get('title', ''), int(y.group()) if y else None, d.get('fulljournalname', '')


def arxiv(aid):
    r = get('https://export.arxiv.org/api/query', params={'id_list': aid})
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    e = r and ET.fromstring(r.text).find('a:entry', ns)
    if e is None or e.find('a:title', ns) is None:
        return None
    return (' '.join(e.find('a:title', ns).text.split()), int(e.find('a:published', ns).text[:4]), 'arXiv')


def check(entry):
    doi, pmid, arx = DOI.search(entry), PMID.search(entry), ARX.search(entry)
    if not (doi or pmid or arx):
        return '', None, ['NO-ID']
    doi = doi and doi.group(1).rstrip('.*_')
    if doi and doi.lower().startswith('10.48550/arxiv.'):
        arx, doi = re.search(r'(\d{4}\.\d{4,5})', doi), None
    ident, res = '', None
    for kind, val, fn in (('DOI', doi, crossref), ('PMID', pmid and pmid.group(1), pubmed),
                          ('arXiv', arx and arx.group(1), arxiv)):
        if val and not res:
            ident, res = f'{kind}:{val}', fn(val)
    if not res:
        return ident, None, ['UNRESOLVED']
    title, year, _ = res
    flags = []
    if year and year < 2021 and 'pre-2021' not in entry.lower():
        flags.append('PRE-2021')
    bare = re.sub(r'https?://\S+|10\.\d{4,9}/\S+|PMID[:\s]*\d+|arXiv[:.\s]*\S+', ' ', entry)
    cited_years = {int(y) for y in YEAR.findall(bare)}
    if year and cited_years and not any(abs(y - year) <= 1 for y in cited_years):
        flags.append(f'YEAR-MISMATCH(cited {sorted(cited_years)})')
    t = TITLE.search(entry)
    if t and title and not title.startswith('('):
        r = difflib.SequenceMatcher(None, t.group(1).lower().strip(' .'), title.lower().strip(' .')).ratio()
        if r < 0.6:
            flags.append(f'TITLE-MISMATCH(r={r:.2f})')
    return ident, res, flags or ['OK']


def main(out, papers):
    lines = ['# Machine reference pre-check', '',
             'Automated: resolves identifiers via Crossref / PubMed / arXiv. `OK` means the identifier exists, '
             'the year is ≥2021 and the title matches — it does NOT mean the claim matches the source.', '']
    for p in papers:
        refs = parse(open(p, encoding='utf-8').read())
        lines += [f'## {p.replace(chr(92), "/").split("/")[-1]} ({len(refs)} refs)', '',
                  '| Ref | Identifier | Resolved title | Year | Venue | Flags |', '|---|---|---|---|---|---|']
        for rid, entry in refs.items():
            ident, res, flags = check(entry)
            t, y, v = res or ('—', '—', '—')
            lines.append(f'| {rid} | {ident or "—"} | {str(t)[:110]} | {y} | {str(v)[:40]} | {", ".join(flags)} |')
        lines.append('')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'wrote {out}')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        demo = ('## References\n'
                '[clinician-1] Smith et al. "A study of things." Lancet, 2023. DOI: 10.1016/j.x.2023.01.001. — URL\n'
                '  continued line\n\n'
                '| C1 | claim | [clinician-1] | STRONG |\n'
                '- **[clinician-2]** Doe. "Other title here ok." arXiv:2401.01234 (2024)\n')
        refs = parse(demo)
        assert list(refs) == ['clinician-1', 'clinician-2'], refs
        assert 'continued line' in refs['clinician-1']
        assert DOI.search(refs['clinician-1']).group(1).rstrip('.*_') == '10.1016/j.x.2023.01.001'
        assert ARX.search(refs['clinician-2']).group(1) == '2401.01234'
        print('selftest ok')
    else:
        main(sys.argv[1], sys.argv[2:])
