"""Build audit packets: for every reference in a debate paper, the lines that cite it plus the
source abstract (PubMed -> Crossref -> arXiv), so auditors judge claim-vs-source without browsing.
Usage: python packets.py <out_dir> <paper.md> [<paper.md> ...]   |   python packets.py --selftest
"""
import os, re, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from fetch import get, get_json          # noqa: E402
from refcheck import ARX, DOI, PMID, parse  # noqa: E402

ALIAS = {'PS': 'ppg_scientist'}
BRACKET = re.compile(r'\[([^\[\]]{1,120})\]')
TOKEN = re.compile(r'^(?:([A-Za-z_]+)?-)?(\d+)(?:\s*[–-]\s*(\d+))?$')
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'


def cited_numbers(bracket, slug):
    """'clinician-1, -4, -6' -> {1,4,6}; 'PS-3' -> {3}; '23' / '26,27' / '1–3' -> numbers (own paper)."""
    nums, prefix = set(), slug
    for tok in re.split(r'[,;]', bracket):
        m = TOKEN.match(tok.strip())
        if not m:
            return set()  # not a pure citation bracket (e.g. prose, links)
        if m.group(1):
            prefix = ALIAS.get(m.group(1), m.group(1))
        if prefix == slug:
            lo = int(m.group(2))
            nums.update(range(lo, int(m.group(3) or lo) + 1))
    return nums


def citing_lines(text, slug):
    """-> {n: [(line_no, line)]} for lines outside the reference list."""
    out = {}
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r'^\W*\[[a-z_]+-\d+\]', line):
            continue  # a reference entry, not a citation
        for b in BRACKET.findall(line):
            for n in cited_numbers(b, slug):
                out.setdefault(n, []).append((i, line.strip()))
    return out


def pubmed_abstracts(pmids):
    res = {}
    ids = sorted(set(pmids))
    for k in range(0, len(ids), 150):
        r = get(EUTILS + 'efetch.fcgi', {'db': 'pubmed', 'id': ','.join(ids[k:k + 150]), 'retmode': 'xml'})
        if not r:
            continue
        for art in ET.fromstring(r.content).iter('PubmedArticle'):
            pmid = art.findtext('.//MedlineCitation/PMID')
            parts = [((a.get('Label') + ': ') if a.get('Label') else '') + ''.join(a.itertext())
                     for a in art.iter('AbstractText')]
            res[pmid] = ' '.join(parts).strip()
    return res


def doi_to_pmid(doi):
    d = get_json(EUTILS + 'esearch.fcgi', {'db': 'pubmed', 'term': f'{doi}[doi]', 'retmode': 'json'})
    ids = d and d.get('esearchresult', {}).get('idlist')
    return ids[0] if ids and len(ids) == 1 else None


def crossref_abstract(doi):
    d = get_json(f'https://api.crossref.org/works/{doi}')
    a = d and d['message'].get('abstract')
    return ' '.join(re.sub(r'<[^>]+>', ' ', a).split()) if a else None


def arxiv_abstract(aid):
    r = get('https://export.arxiv.org/api/query', {'id_list': aid})
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    e = r and ET.fromstring(r.text).find('a:entry', ns)
    return ' '.join(e.find('a:summary', ns).text.split()) if e is not None and e.find('a:summary', ns) is not None else None


def build(out_dir, paper):
    text = open(paper, encoding='utf-8').read()
    slug = os.path.basename(paper)[:-3]
    refs, cites = parse(text), citing_lines(text, slug)
    ids = {}
    for rid, entry in refs.items():
        doi, pm, ax = DOI.search(entry), PMID.search(entry), ARX.search(entry)
        ids[rid] = (doi and doi.group(1).rstrip('.*_'), pm and pm.group(1), ax and ax.group(1))
    pmid_of = {rid: pm or (doi and doi_to_pmid(doi)) for rid, (doi, pm, _) in ids.items()}
    abstracts = pubmed_abstracts([p for p in pmid_of.values() if p])
    lines = [f'# Audit packet — {slug}', '',
             'Per reference: the entry, every line citing it (line numbers in round1 file), and the retrieved abstract.',
             'NO-ABSTRACT items (regulatory records, standards, vendor pages, some conference papers) need WebFetch.', '']
    stats = {'abstract': 0, 'none': 0, 'uncited': 0}
    for rid, entry in refs.items():
        n = int(rid.rsplit('-', 1)[1])
        doi, _, ax = ids[rid]
        pm = pmid_of[rid]
        src, abs_ = None, None
        if pm and abstracts.get(pm):
            src, abs_ = f'PubMed PMID {pm}', abstracts[pm]
        elif doi and (a := crossref_abstract(doi)):
            src, abs_ = f'Crossref {doi}', a
        elif ax and (a := arxiv_abstract(ax)):
            src, abs_ = f'arXiv {ax}', a
        stats['abstract' if abs_ else 'none'] += 1
        lines += [f'## [{rid}]', f'**Entry:** {entry[:900]}', '', '**Cited at:**']
        uses = cites.get(n, [])
        stats['uncited'] += not uses
        lines += [f'- L{i}: {l[:600]}' for i, l in uses] or ['- (not cited in text — listed only)']
        lines += ['', f'**Abstract ({src}):** {abs_}' if abs_ else '**Abstract:** NO-ABSTRACT — verify via WebFetch using the URL in the entry.', '']
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, f'{slug}.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'{slug}: {len(refs)} refs, {stats["abstract"]} with abstract, {stats["none"]} without, {stats["uncited"]} uncited')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        assert cited_numbers('clinician-1, -4, -6', 'clinician') == {1, 4, 6}
        assert cited_numbers('PS-3', 'ppg_scientist') == {3}
        assert cited_numbers('26,27', 'bayesian_ml') == {26, 27}
        assert cited_numbers('-17', 'device_engineer') == {17}
        assert cited_numbers('em_engineer-27, -28', 'em_engineer') == {27, 28}
        assert cited_numbers('1–3', 'x') == {1, 2, 3}
        assert cited_numbers('see Fig. 2', 'x') == set()
        assert cited_numbers('clinician-3', 'physiologist') == set()
        assert citing_lines('text [clinician-2] more\n[clinician-2] Ref entry', 'clinician') == {2: [(1, 'text [clinician-2] more')]}
        print('selftest ok')
    else:
        for p in sys.argv[2:]:
            build(sys.argv[1], p)
