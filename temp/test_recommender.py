import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.recommender import recommender

hair = recommender.get_haircut_recommendations("oval", 85)
beard = recommender.get_beard_recommendations("square", 80)
colors = recommender.get_color_recommendations("medium", 85, "Warm")

print(f"Haircuts: {len(hair)} (first: {hair[0]['name']})")
print(f"Beards: {len(beard)} (first: {beard[0]['name']})")
print(f"Colors: {len(colors)} (first: {colors[0]['name']})")
print()

print("Top 10 haircuts:")
for h in hair[:10]:
    print(f"  {h['id']}. {h['name']} — {h['confidence']}%")
print()

print("Top 10 beards:")
for b in beard[:10]:
    print(f"  {b['id']}. {b['name']} — {b['confidence']}%")
print()

print("All colors:")
for c in colors:
    print(f"  {c['id']}. {c['name']} — {c['confidence']}%")
