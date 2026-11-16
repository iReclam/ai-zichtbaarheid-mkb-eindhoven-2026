#!/usr/bin/env python3
"""Deel 2 onderzoek: kent een AI-assistent het bedrijf? Vraag per bedrijf 'Wat weet je over <naam> in Eindhoven?'
aan Gemini (google_search), OpenAI (web_search) en Perplexity (sonar). 'Herkend' = eigen domein in de bronnen of de tekst.
Gebruik: python3 ai-mention.py [--limit N] [--platforms gemini,openai,perplexity]
"""
import json, random, re, sys, os, concurrent.futures as cf
import importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as mon
S = mon.RAW
args = sys.argv[1:]
limit = int(args[args.index('--limit') + 1]) if '--limit' in args else 100
plats = (args[args.index('--platforms') + 1] if '--platforms' in args else 'gemini,openai,perplexity').split(',')
def _or(model):
    def f(q):
        r, err = mon._post('https://openrouter.ai/api/v1/chat/completions', {'model': model, 'messages': [{'role': 'system', 'content': mon.SYSTEM}, {'role': 'user', 'content': q}]},
                           {'Authorization': 'Bearer ' + os.environ.get('OPENROUTER_API_KEY', '')})
        if err: return None, [], err, model
        m = r['choices'][0]['message']; text = m.get('content') or ''
        src = [{'title': a['url_citation'].get('title', ''), 'url': a['url_citation'].get('url', '')} for a in (m.get('annotations') or []) if a.get('type') == 'url_citation']
        src += [{'title': '', 'url': u} for u in (r.get('citations') or [])]
        return text, src, None, model
    return f
# OpenAI- en Perplexity-sleutels zonder tegoed (10-11) → via OpenRouter, zelfde modellen met webzoeken
FN = {'gemini': mon.ask_gemini, 'openai': _or('openai/gpt-4.1-mini:online'), 'perplexity': _or('perplexity/sonar')}

scan = {r['url']: r for r in json.load(open(S + '/scan.json')) if 'error' not in r}
sample = [r for r in json.load(open(S + '/sample.json')) if 'https://' + r['domain'] + '/' in scan and r['name']]
random.seed(20261110)
# gestratificeerd: 20 per hoofdcategorie, aangevuld tot limit
by = {}
for r in sample: by.setdefault(r['cat'].split(':')[0], []).append(r)
pick = []
for c, L in by.items():
    random.shuffle(L); pick += L[:20]
rest = [r for r in sample if r not in pick]; random.shuffle(rest)
pick = (pick + rest)[:limit]

def one(r):
    out = {'name': r['name'], 'domain': r['domain'], 'cat': r['cat'], 'score': scan['https://' + r['domain'] + '/']['score'], 'platforms': {}}
    q = f"Wat weet je over {r['name']} in Eindhoven? Wat doen ze en wat is hun website?"
    dom = r['domain'].lower()
    for p in plats:
        text, src, err, model = FN[p](q)
        if err:
            out['platforms'][p] = {'error': err}; continue
        t = (text or '').lower()
        in_src = any(dom in (s.get('url') or '').lower() for s in src)
        in_text = dom in t
        out['platforms'][p] = {'recognised': in_src or in_text, 'in_sources': in_src, 'in_text': in_text,
                               'unknown_phrase': bool(re.search(r"geen (specifieke )?informatie|kan ik niet vinden|niet bekend|ken ik niet|kon geen", t)),
                               'n_sources': len(src), 'model': model, 'snippet': (text or '')[:300]}
    return out

with cf.ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, pick))
json.dump(res, open(S + '/ai-mention.json', 'w'), ensure_ascii=False, indent=1)
for p in plats:
    ok = [x['platforms'][p] for x in res if 'error' not in x['platforms'].get(p, {'error': 1})]
    print(p, 'n=%d herkend=%d (%.0f%%) fouten=%d' % (len(ok), sum(o['recognised'] for o in ok), 100 * sum(o['recognised'] for o in ok) / max(1, len(ok)), len(res) - len(ok)))
