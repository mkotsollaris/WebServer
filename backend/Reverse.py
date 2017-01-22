import json
import sys
import requests

image = sys.argv[1]

def post_some_dict(dict):
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:5000/search", data=json.dumps(dict), headers=headers)
    return r.text
total = json.loads(post_some_dict({"image_url": image}));
#print(total);
links = json.loads(post_some_dict({"image_url": image}))['links'];
titles = json.loads(post_some_dict({"image_url": image}))['titles'];

list = [];
parselist = [];
for x in links:
    if "walmart" in x:
        list.append(x);
        x = x[27:-9];
        parselist.append(x);
        #print(x);
#print(list[0]);
l = parselist[0].split('-');
g = [x.split('-') for x in parselist];

test = g[0][0];
#print(test);
for r in g[0]:
    if r in g[1]:
        print(r);
print(g);