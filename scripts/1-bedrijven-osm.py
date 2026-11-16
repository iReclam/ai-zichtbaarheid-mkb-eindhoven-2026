import json,urllib.request,urllib.parse
q='''[out:json][timeout:120];
area["name"="Eindhoven"]["admin_level"="8"]->.a;
( nwr(area.a)["website"]["shop"];
  nwr(area.a)["website"]["craft"];
  nwr(area.a)["website"]["office"];
  nwr(area.a)["website"]["healthcare"];
  nwr(area.a)["website"]["amenity"~"^(dentist|doctors|veterinary|restaurant|cafe|driving_school|clinic|pharmacy)$"];
);
out tags;'''
d=json.load(urllib.request.urlopen(urllib.request.Request('https://overpass-api.de/api/interpreter',data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'ireclam-research/0.1'}),timeout=180))
rows=[]
for e in d['elements']:
    t=e['tags']; cat=t.get('shop') and 'shop:'+t['shop'] or t.get('craft') and 'craft:'+t['craft'] or t.get('office') and 'office:'+t['office'] or t.get('healthcare') and 'health:'+t['healthcare'] or 'amenity:'+t.get('amenity','')
    rows.append(dict(name=t.get('name',''),cat=cat,website=t['website'],brand=t.get('brand','')))
json.dump(rows,open('osm-eindhoven.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(len(rows)); print(Counter(r['cat'] for r in rows).most_common(40))
