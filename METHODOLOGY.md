# Methode — Onderzoek AI-zichtbaarheid MKB Eindhoven 2026

Uitgevoerd door iReclam (online marketingbureau, Eindhoven) op 10 november 2026. Publicatie: https://ireclam.nl/ai-zichtbaarheid-mkb-eindhoven-2026/

## Onderzoeksvragen
1. Hoeveel Eindhovense bedrijfswebsites zijn technisch klaar om door AI-assistenten gelezen en geciteerd te worden?
2. Kent een AI-assistent met webzoeken een bedrijf als je het bij naam noemt?
3. Beveelt een AI-assistent het bedrijf aan als je om een aanbeveling in de categorie vraagt?

## Populatie en steekproef
- **Bron:** OpenStreetMap (Overpass API), gemeente Eindhoven (admin_level 8), alle objecten met een website-tag en een tag `shop`, `craft`, `office`, `healthcare` of een relevante `amenity` (o.a. restaurant, café, tandarts, huisarts, dierenarts, rijschool, kliniek, apotheek) → 1.395 objecten (`scripts/1-bedrijven-osm.py`).
- **Opschoning:** ketens (brand-tag / gedeelde ketendomeinen), overheid, onderwijs, verenigingen, dubbele domeinen en social-media-profielen als 'website' verwijderd → **879 unieke bedrijfswebsites**.
- **Deel 2:** gestratificeerde steekproef van **100 bedrijven** (20 per hoofdcategorie: horeca, winkels, zorg, kantoren/dienstverlening, aangevuld).
- **Deel 3:** **28 categorieën** met ≥7 bedrijven in de dataset (samen **641 bedrijven**).

KvK-gegevens zijn niet gebruikt (geen open data). De dataset is daardoor niet representatief voor 'alle MKB in Eindhoven', wel voor bedrijven die in OpenStreetMap met een website staan.

## Deel 1 — technische gereedheid
- Tool: [geo-readiness-check](https://github.com/iReclam/geo-readiness-check) (open source, MIT), alleen de **homepage**, 8 parallelle verzoeken, 10-11-2026.
- **Meetbaar:** 773 van 879 (106 onbereikbaar, botbescherming 403/429 of serverfout).
- **Score 0–100** op basis van: AI-zoekbots niet geblokkeerd in robots.txt, tekst leesbaar zonder JavaScript (≥150 woorden in ruwe HTML), Organization/LocalBusiness-JSON-LD (met adres, telefoon, sameAs), FAQPage-schema, title, meta description, precies één H1, Open Graph, XML-sitemap, HTTPS, geen noindex. Weging: zie README van de tool.
- **'Klaar voor AI-zoeken'** = score ≥ 80.

## Deel 2 — herkenning
- Vraag per bedrijf: *"Wat weet je over {naam} in Eindhoven? Wat doen ze en wat is hun website?"* (systeemprompt en modellen: `prompts/prompts.md`).
- Modellen met webzoeken: GPT-4.1-mini (`:online`, OpenRouter), Perplexity Sonar (OpenRouter), Gemini 2.5 Flash met Google Search grounding.
- **Herkend** = het eigen domein van het bedrijf staat in de geciteerde bronnen of in de antwoordtekst.
- Eén run per bedrijf per model. Gemini: daglimiet bereikt na 18 bedrijven.

## Deel 3 — aanbeveling
- Vraag per categorie: *"Welke {categorie} in Eindhoven raad je aan? Noem er 5 met hun website."*
- GPT-4.1-mini (`:online`) en Perplexity Sonar, elk **2 rondes** → 28 × 2 × 2 = **112 antwoorden**.
- **Aanbevolen** = domein of bedrijfsnaam (OSM-naam, ≥5 tekens) van een bedrijf uit de dataset komt voor in antwoord of bronnen.

## Resultaten (kern)
| Maat | Waarde |
|---|---|
| Gemiddelde score (n=773) | 66,7 (mediaan 66) |
| Score ≥ 80 | 24,8 % |
| Geen JSON-LD op homepage | 40,4 % |
| Business-schema met adres én telefoon | 13,6 % |
| Nauwelijks leesbaar zonder JavaScript | 14,0 % |
| Blokkeert minstens één AI-bot | 5,3 % (AI-zoekbot: 2,1 %) |
| Herkend bij naam — GPT-4.1-mini / Perplexity Sonar | 84 % / 82 % (n=100) |
| Herkend bij naam — Gemini 2.5 Flash | 15 van 18 gemeten |
| Bedrijven ooit aanbevolen (deel 3) | 45 van 641 (7,0 %) → 93 % nooit |
| Gem. technische score aanbevolen vs. niet | 70,7 vs. 66,3 |

## Beperkingen
- Alleen de homepage is gescand; schema op diepere pagina's telt niet mee.
- OSM-dekking is onvolledig; ketens en bedrijven zonder OSM-website vallen buiten de dataset.
- Sites met botbescherming zijn niet gemeten (en zijn voor AI-crawlers waarschijnlijk ook slecht bereikbaar).
- API-antwoorden kunnen afwijken van de consumentenapps (model, locatie, tijdstip, personalisatie).
- Deel 2: één run per model; Gemini slechts 18 metingen.
- Deel 3: elk antwoord noemt ±5 namen, dus per categorie zijn hooguit ±20 bedrijven zichtbaar; naam-matching kan namen missen of (bij korte namen) onterecht matchen; ketens en niet-OSM-bedrijven zijn niet geteld.
- De score meet technische gereedheid, geen voorspelling van daadwerkelijke vermelding. Het verschil 70,7 vs. 66,3 is een correlatie, geen bewijs van oorzaak.

## Privacy
Gepubliceerde data bevat geen bedrijfsnamen, websites of domeinen; rijen zijn geschud voor het toekennen van ID's. De ruwe data (met namen, uit openbare bronnen) wordt niet gepubliceerd.

## Herhaling
Gepland: januari 2027 (zelfde methode), daarna breder (Nederland en Vlaanderen).
