import json

with open(r'c:\Users\Jaime\Documents\GitHub\csnexus\data\seed\questions\clerical-ability\alphabetical-filing\business-and-office-filing\questions.json', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total questions: {len(data)}')
print(f'Last ID: {data[-1]["id"]}')
print(f'Difficulties: {set(q["difficulty"] for q in data)}')
print(f'Tags used: {set(t for q in data for t in q["tags"])}')
