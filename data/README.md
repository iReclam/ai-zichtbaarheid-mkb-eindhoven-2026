# Codebook

All business names, websites and domains have been removed. Rows were shuffled with a fixed seed before IDs were assigned, so IDs cannot be traced back to the alphabetical source list.

## part1-technical-scan.csv / .json (879 rows, 773 measurable)
One row per business website (OpenStreetMap, municipality of Eindhoven), homepage only, scanned 10-11-2026 with [geo-readiness-check](https://github.com/iReclam/geo-readiness-check).

| Column | Meaning |
|---|---|
| id | Anonymous ID (S0001…) |
| category | OpenStreetMap category, e.g. `shop:bakery`, `amenity:restaurant`, `office:it` |
| measurable | false = unreachable, bot protection or server error (excluded from statistics) |
| status | HTTP status of the homepage |
| score | Technical AI-readiness score 0–100 (see geo-readiness-check README) |
| https, robots_txt, sitemap, indexable, llms_txt | Basic checks (true/false) |
| key_ai_bots_allowed | No AI *search/retrieval* bot is blocked in robots.txt |
| ai_bots_blocked | AI bots blocked in robots.txt (`;`-separated) |
| title, title_len, meta_description, open_graph, lang | Head elements |
| h1_count, h1_ok | Number of H1s; ok = exactly one |
| words_without_js, readable_without_js | Words in raw HTML; readable = ≥150 words |
| jsonld, jsonld_errors, schema_types | JSON-LD present, parse errors, schema.org types |
| business_schema, business_types | Organization/LocalBusiness (sub)type present |
| schema_address, schema_phone, schema_sameas | Address / telephone / sameAs in that business schema |
| faq_schema | FAQPage schema present |
| phone_visible | Telephone number visible in the HTML |

`part1-summary.json` = the aggregate figures used in the publication.

## part2-recognition.csv (100 rows)
Stratified sample from part 1. Per platform (`gemini_`, `openai_`, `perplexity_`): `measured` (false = API error / daily limit), `recognised`, `in_sources`, `in_text`, `unknown_phrase` (answer said it did not know the business), `n_sources`, `model`. `technical_score` = part 1 score. Gemini: only 18 of 100 measured (daily API limit).

## part3-recommendations.csv (112 rows)
One row per answer: `category`, `question_term` (Dutch term used in the question), `model`, `round` (1 or 2), `error`, `n_urls_in_answer`, `n_dataset_businesses_named` (how many businesses from the OSM dataset were named; names not published).
`part3-summary.json`: `n_in_cats` (641 businesses in these 28 categories), `ever_recommended` (45; matched on domain **or** OSM business name ≥5 characters — domain-only matching gives 25), `per_cat` [category, dataset businesses in that category, distinct dataset businesses (from all 879, any category) named in that category's answers — so this column does not add up to 45], `score_hit` / `score_miss` (mean technical score of named vs. never-named businesses).

Note: `n_dataset_businesses_named` in part3-recommendations.csv uses domain matching only (script 4). The 28 categories were selected on ≥7 occurrences in the raw OSM list (1,395), before cleaning.
