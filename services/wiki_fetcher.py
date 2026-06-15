import json
import os
import re
import requests
from html.parser import HTMLParser
from datetime import datetime, timedelta

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp", "wiki_cache.json")
BEARD_CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp", "wiki_beard_cache.json")
CACHE_DURATION = timedelta(hours=24)


class WikiTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.in_a = False
        self.current_field = ""
        self.td_fields = []
        self.rows = []
        self.col_index = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table" and "wikitable" in attrs_dict.get("class", ""):
            self.in_table = True
            self.rows = []
        if not self.in_table:
            return
        if tag == "td":
            self.in_td = True
            self.current_field = ""
            self.col_index += 1
        if tag == "a" and self.in_td:
            self.in_a = True

    def handle_data(self, data):
        if self.in_td:
            text = data.strip()
            if text:
                if self.in_a or len(self.td_fields) < self.col_index:
                    self.current_field += text

    def handle_endtag(self, tag):
        if tag == "table" and self.in_table:
            self.in_table = False
        if tag == "td" and self.in_table:
            field = self.current_field.strip()
            if field:
                self.td_fields.append(field)
            self.in_td = False
            self.in_a = False
        if tag == "tr" and self.in_table:
            if self.td_fields:
                self.rows.append(self.td_fields[0])
            self.td_fields = []
            self.col_index = 0
            self.current_field = ""


def fetch_wiki_section(page: str, section: int) -> list:
    url = (
        "https://en.wikipedia.org/w/api.php"
        f"?action=parse&page={page}&format=json"
        f"&prop=text&section={section}&redirects=1"
    )
    headers = {"User-Agent": "Silverscisor/1.0 (hairstyle-recommendation-bot; educational project)"}
    resp = requests.get(url, timeout=15, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    html = data.get("parse", {}).get("text", {}).get("*", "")
    parser = WikiTableParser()
    parser.feed(html)
    return parser.rows


def generate_hairstyle_data(styles: list[str]) -> list[dict]:
    style_tags = {
        "fade": ["Modern", "Trending"],
        "cut": ["Classic"],
        "bob": ["Classic", "Popular"],
        "crop": ["Modern", "Popular"],
        "pompadour": ["Trending", "Bold"],
        "quiff": ["Modern", "Trending"],
        "braid": ["Trending", "Bold"],
        "bun": ["Classic", "Popular"],
        "ponytail": ["Classic"],
        "dread": ["Bold", "Natural"],
        "curl": ["Natural", "Popular"],
        "wave": ["Natural", "Trending"],
        "fringe": ["Modern", "Popular"],
        "buzz": ["Minimal", "Classic"],
        "shag": ["Trending", "Modern"],
        "mullet": ["Bold", "Trending"],
        "mohawk": ["Bold", "Trending"],
        "undercut": ["Modern", "Trending"],
        "part": ["Classic"],
        "slick": ["Classic", "Bold"],
        "flat": ["Classic"],
        "spike": ["Bold", "Modern"],
        "afro": ["Natural", "Bold"],
    }
    prices = [150, 180, 200, 220, 250, 280, 300, 350, 400]
    durations = ["15 min", "20 min", "25 min", "30 min", "35 min", "40 min"]

    result = []
    seen = set()
    for i, s in enumerate(styles):
        sl = s.lower().strip()
        if not sl or sl in seen or len(sl) < 3:
            continue
        seen.add(sl)

        tags = ["Popular"]
        for kw, t in style_tags.items():
            if kw in sl:
                tags = list(dict.fromkeys(t + tags))
                break

        price = prices[i % len(prices)]
        dur = durations[i % len(durations)]
        conf = max(65, 90 - (i % 15))

        result.append({
            "id": i + 1,
            "name": s.strip(),
            "confidence": conf,
            "description": f"{s.strip()} hairstyle",
            "price": price,
            "duration": dur,
            "tags": tags[:3],
            "image": None,
        })
    return result


def load_or_fetch_cache(cache_file: str, page: str, sections: list[int]) -> list[dict]:
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at < CACHE_DURATION and data.get("styles"):
            print(f"[WikiFetcher] Using cached {len(data['styles'])} styles from {cache_file}")
            return data["styles"]
    except (FileNotFoundError, KeyError, ValueError):
        pass

    print(f"[WikiFetcher] Fetching {page} sections {sections}...")
    all_raw = []
    seen = set()
    for sec in sections:
        try:
            raw = fetch_wiki_section(page, sec)
            for name in raw:
                n = name.strip()
                if n and len(n) > 2 and n.lower() not in seen:
                    seen.add(n.lower())
                    all_raw.append(n)
        except Exception as e:
            print(f"[WikiFetcher] Section {sec} failed: {e}")

    styles = generate_hairstyle_data(all_raw)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({
            "cached_at": datetime.now().isoformat(),
            "styles": styles,
        }, f, indent=2, ensure_ascii=False)
    print(f"[WikiFetcher] Cached {len(styles)} styles")
    return styles


def get_wiki_hairstyles(force_refresh: bool = False) -> list[dict]:
    if force_refresh:
        try:
            os.remove(CACHE_FILE)
        except FileNotFoundError:
            pass
    return load_or_fetch_cache(CACHE_FILE, "List_of_hairstyles", [1, 2, 3])


def get_wiki_beards(force_refresh: bool = False) -> list[dict]:
    if force_refresh:
        try:
            os.remove(BEARD_CACHE_FILE)
        except FileNotFoundError:
            pass
    return load_or_fetch_cache(BEARD_CACHE_FILE, "List_of_facial_hair_styles", [1, 2, 3, 4, 5])


if __name__ == "__main__":
    styles = get_wiki_hairstyles(force_refresh=True)
    print(f"\n--- Hairstyles ({len(styles)}) ---")
    for s in styles[:15]:
        print(f"  {s['id']}. {s['name']} — ${s['price']} — tags: {s['tags']}")

    beards = get_wiki_beards(force_refresh=True)
    print(f"\n--- Beard styles ({len(beards)}) ---")
    for s in beards[:15]:
        print(f"  {s['id']}. {s['name']} — ${s['price']} — tags: {s['tags']}")
