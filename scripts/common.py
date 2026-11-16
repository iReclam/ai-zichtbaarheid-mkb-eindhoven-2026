"""Shared helpers for the research scripts (taken from iReclam's internal AI-visibility monitor)."""
import json, os, re, time, urllib.request, urllib.error

SYSTEM = "Beantwoord de vraag zoals je dat voor een Nederlandse gebruiker zou doen. Noem concrete bedrijven of bronnen als dat past."
RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'raw')  # raw output (contains business names; not published)

def _post(url, body, headers, timeout=90, tries=3):
    for i in range(tries):
        r, err = _post1(url, body, headers, timeout)
        if err and re.match(r"HTTP (429|5\d\d)", err) and i < tries - 1:
            time.sleep(8 * (i + 1)); continue
        return r, err

def _post1(url, body, headers, timeout):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        return json.load(urllib.request.urlopen(req, timeout=timeout)), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: " + re.sub(r"\s+", " ", e.read()[:160].decode(errors="ignore"))
    except Exception as e:
        return None, str(e)[:160]

def ask_gemini(q):
    r, err = _post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + os.environ.get("GOOGLE_API_KEY", ""),
                   {"systemInstruction": {"parts": [{"text": SYSTEM}]}, "contents": [{"parts": [{"text": q}]}], "tools": [{"google_search": {}}]}, {})
    if err: return None, [], err, "gemini-2.5-flash+google_search"
    c = r["candidates"][0]; text = "".join(p.get("text", "") for p in c.get("content", {}).get("parts", []))
    src = [{"title": ch.get("web", {}).get("title", ""), "url": ch.get("web", {}).get("uri", "")} for ch in c.get("groundingMetadata", {}).get("groundingChunks", [])]
    return text, src, None, "gemini-2.5-flash+google_search"
