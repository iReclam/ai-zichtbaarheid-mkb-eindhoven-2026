#!/usr/bin/env python3
"""Deel 3: wordt het bedrijf AANBEVOLEN? Per categorie 'Welke <categorie> in Eindhoven raad je aan? Noem er 5 met website.'
aan GPT-4.1-mini (:online) en Perplexity Sonar via OpenRouter, 2 rondes. Tel welke OSM-domeinen (879) ooit genoemd/geciteerd worden.
"""
import sys, json, os, re, time, importlib.util, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as mon
S = mon.RAW
CATS = {  # OSM-categorie → vraagterm (alleen categorieën met ≥7 bedrijven in de steekproef)
 'amenity:restaurant': 'restaurant', 'amenity:cafe': 'café of koffiebar', 'shop:clothes': 'kledingwinkel', 'shop:hairdresser': 'kapper',
 'health:doctor': 'huisarts', 'shop:bicycle': 'fietsenwinkel', 'shop:bakery': 'bakker', 'shop:beauty': 'schoonheidssalon',
 'health:dentist': 'tandarts', 'shop:car_repair': 'autogarage', 'office:it': 'IT-bedrijf', 'shop:books': 'boekwinkel',
 'shop:sports': 'sportwinkel', 'shop:optician': 'opticien', 'shop:pet': 'dierenwinkel', 'shop:interior_decoration': 'woonwinkel',
 'health:physiotherapist': 'fysiotherapeut', 'shop:butcher': 'slager', 'office:engineer': 'ingenieursbureau', 'shop:shoes': 'schoenenwinkel',
 'shop:florist': 'bloemist', 'shop:jewelry': 'juwelier', 'office:lawyer': 'advocatenkantoor', 'office:estate_agent': 'makelaar',
 'office:employment_agency': 'uitzendbureau', 'office:company': 'bedrijf voor zakelijke dienstverlening', 'shop:chemist': 'drogist', 'shop:alcohol': 'slijterij',
}
sample = json.load(open(S + '/sample.json'))
doms = {r['domain'] for r in sample}
def ask(model, q):
    r, err = mon._post('https://openrouter.ai/api/v1/chat/completions', {'model': model, 'messages': [{'role': 'user', 'content': q}]},
                       {'Authorization': 'Bearer ' + os.environ.get('OPENROUTER_API_KEY', '')})
    if err: return None, [], err
    m = r['choices'][0]['message']; text = m.get('content') or ''
    urls = [a['url_citation'].get('url', '') for a in (m.get('annotations') or []) if a.get('type') == 'url_citation'] + list(r.get('citations') or [])
    return text, urls, None
def found(text, urls):
    t = (text or '').lower(); hit = set()
    for d in doms:
        if d in t or any(d in (u or '').lower() for u in urls): hit.add(d)
    return sorted(hit)
out = []
for cat, term in CATS.items():
    q = f"Welke {term} in Eindhoven raad je aan? Noem er 5 met hun website."
    for model in ['openai/gpt-4.1-mini:online', 'perplexity/sonar']:
        for ronde in (1, 2):
            text, urls, err = ask(model, q)
            out.append({'cat': cat, 'term': term, 'model': model, 'ronde': ronde, 'error': err, 'osm_domeinen': found(text, urls) if not err else [], 'n_urls': len(urls), 'snippet': (text or '')[:400]})
            json.dump(out, open(S + '/ai-aanbeveling.json', 'w'), ensure_ascii=False, indent=1)
            time.sleep(1)
named = {d for o in out for d in o['osm_domeinen']}
in_cats = [r for r in sample if r['cat'] in CATS]
print('vragen', len(out), 'fouten', sum(1 for o in out if o['error']))
print('OSM-bedrijven in deze categorieën:', len(in_cats), '| ooit aanbevolen:', sum(1 for r in in_cats if r['domain'] in named), '| alle 879: ooit genoemd', len(named & doms))
