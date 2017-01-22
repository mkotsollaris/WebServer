import json
import sys
import requests
from collections import Counter

image = sys.argv[1]
threshold = 2

def removes(yes):
    no = ["Walmart.com", ".", ","]
    for x in no:
        yes = yes.replace(x, '')
    return yes

def post_some_dict(dict):
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:5000/search", data=json.dumps(dict), headers=headers)
    return r.text

out = json.loads(post_some_dict({"image_url": image}))['titles']
#print(out)
#out = [x for x in out if 'walmart' in x]
threshold = len(out)-1
#out = [x[27:-9] for x in out]
#print(out)
large = []
for line in out:
    line = line.replace('-', '')
    line = removes(line)
    line = line.split(' ')
    for word in line:
        large.append(word)
#print(large)
c = Counter(large).most_common()

keywords = []

for x in c:
    if x[1] > threshold:
        keywords.append(x[0])

print(' '.join(keywords))
