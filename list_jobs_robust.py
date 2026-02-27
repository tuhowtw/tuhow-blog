
import json

path = 'jobs_latest.json'
try:
    with open(path, 'r', encoding='utf-16') as f:
        data = json.load(f)
except Exception:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

if 'jobs' in data:
    for j in data['jobs']:
        print(f"{j.get('id', j.get('databaseId'))} {j.get('name')} {j.get('conclusion')}")
else:
    print("No jobs found in data")
    print("Keys:", data.keys())
