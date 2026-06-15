import requests, json
headers = {"User-Agent": "Silverscisor/1.0"}
url = "https://en.wikipedia.org/w/api.php?action=parse&page=List_of_facial_hair_styles&format=json&prop=sections&redirects=1"
resp = requests.get(url, timeout=15, headers=headers)
data = resp.json()
for s in data.get("parse", {}).get("sections", []):
    print(f'{s["index"]}: {s["line"]}')
