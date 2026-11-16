# Prompts

All questions were asked in Dutch, exactly as below, on 10 November 2026.

## System prompt (part 2)
> Beantwoord de vraag zoals je dat voor een Nederlandse gebruiker zou doen. Noem concrete bedrijven of bronnen als dat past.

(English: "Answer the question as you would for a Dutch user. Name specific companies or sources where appropriate.")

## Part 2 — recognition (per business, 100 businesses)
> Wat weet je over {naam} in Eindhoven? Wat doen ze en wat is hun website?

("What do you know about {name} in Eindhoven? What do they do and what is their website?")

Models: Gemini 2.5 Flash with Google Search grounding (Google API), GPT-4.1-mini with web search (`openai/gpt-4.1-mini:online` via OpenRouter), Perplexity Sonar (`perplexity/sonar` via OpenRouter).
"Recognised" = the business's own domain appears in the cited sources or in the answer text.

## Part 3 — recommendation (per category, 28 categories × 2 models × 2 rounds = 112 answers)
> Welke {categorie} in Eindhoven raad je aan? Noem er 5 met hun website.

("Which {category} in Eindhoven do you recommend? Name 5 with their website.")

No system prompt. Models: `openai/gpt-4.1-mini:online` and `perplexity/sonar` via OpenRouter. Category terms (Dutch) are listed in `scripts/4-ai-aanbeveling.py` (`CATS`).
