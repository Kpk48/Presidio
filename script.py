from supabase import create_client
import re
from collections import Counter, defaultdict
url = "https://sskojiyeiyrsyiiwcuwn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNza29qaXllaXlyc3lpaXdjdXduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg1NTA4NjksImV4cCI6MjA3NDEyNjg2OX0.3Y-K8d7eHRcfvWVb9r3Dp6alwe36YDGD40M_irP_Ypg"
supabase = create_client(url, key)
data = supabase.table("posts").select("content").execute()
rows = [row['content'] for row in data.data]
counts = Counter()
co = defaultdict(Counter)
def extract_hashtags(text):
    return re.findall(r"#\w+", text.lower())
for text in rows:
    tags = sorted(set(extract_hashtags(text)))
    for t in tags:
        counts[t] += 1
    for i in range(len(tags)):
        for j in range(i+1, len(tags)):
            a, b = tags[i], tags[j]
            co[a][b] += 1
            co[b][a] += 1
print("Top Hashtags")
for tag, count in counts.most_common(5):
    print(f"{tag}: {count}")
def recommend(tag, threshold=0.3, top_n=3):
    if counts[tag] == 0:
        return []
    candidates = [(other, ccount / counts[tag]) for other, ccount in co[tag].items() if ccount / counts[tag] >= threshold]
    return sorted(candidates, key=lambda x: -x[1])[:top_n]
print("\nRecommendations:")
for tag, _ in counts.most_common(5):
    recs = recommend(tag)
    print(f"{tag} => {recs}")