# AI visibility of SMEs in Eindhoven 2026 — open data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24281712.svg)](https://doi.org/10.5281/zenodo.24281712)

**AI knows you, but doesn't recommend you.** Research by [iReclam](https://ireclam.nl) (online marketing agency, Eindhoven, the Netherlands), 10 November 2026.

- Publication (Dutch): https://ireclam.nl/ai-zichtbaarheid-mkb-eindhoven-2026/
- Publication (English): https://ireclam.nl/en/blog/ai-visibility-study-eindhoven-2026/
- Method: [METHODOLOGY.md](METHODOLOGY.md) (Dutch) · prompts: [prompts/prompts.md](prompts/prompts.md) · codebook: [data/README.md](data/README.md)

## Key findings
| Measure | Value |
|---|---|
| Business websites scanned (OpenStreetMap, municipality of Eindhoven) | 879 (773 measurable) |
| Average technical AI-readiness score | 66.7 / 100 (median 66) |
| "Ready for AI search" (score ≥ 80) | 24.8 % |
| No structured data (JSON-LD) on the homepage | 40.4 % |
| Business schema with address and telephone | 13.6 % |
| Recognised by name — GPT-4.1-mini (web) / Perplexity Sonar | 84 % / 82 % (n = 100) |
| Businesses ever recommended in 112 recommendation answers | 45 of 641 (7.0 %) — 93 % never named |

## Contents
- `data/` — anonymised data (no business names, websites or domains): technical scan, recognition, recommendations, summaries.
- `scripts/` — the scripts used (OpenStreetMap query, recognition, recommendation). The technical scan uses [geo-readiness-check](https://github.com/iReclam/geo-readiness-check).
- `prompts/` — the exact questions asked.

API keys are read from environment variables (`GOOGLE_API_KEY`, `OPENROUTER_API_KEY`). Raw output with business names is written to `raw/` and is not part of this repository.

## Licence
- Data and documentation: [CC BY 4.0](LICENSE-DATA) — please cite "iReclam (2026), AI visibility of SMEs in Eindhoven 2026".
- Code: [MIT](LICENSE).

## Cite
iReclam (2026). *AI visibility of SMEs in Eindhoven 2026 (open data)* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24281712 — version 1.0.0: https://doi.org/10.5281/zenodo.24281713. See also [CITATION.cff](CITATION.cff).

---

**Nederlands:** open data bij het onderzoek *AI-zichtbaarheid MKB Eindhoven 2026* van iReclam. Methode in [METHODOLOGY.md](METHODOLOGY.md). Data geanonimiseerd (geen bedrijfsnamen of websites). Data CC BY 4.0, code MIT.
