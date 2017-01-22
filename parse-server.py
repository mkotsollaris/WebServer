import json
import sys
import requests
from collections import Counter
from wapy.api import Wapy
from http.server import BaseHTTPRequestHandler, HTTPServer
wapy = Wapy('frt6ajvkqm4aexwjksrukrey')


def removes(yes):
    no = ["Walmart.com", ".", ","]
    for x in no:
        yes = yes.replace(x, '')
    return yes

def post_some_dict(dict):
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://127.0.0.1:5000/search", data=json.dumps(dict), headers=headers)
    return r.text

def parse_image(image):
    out = json.loads(post_some_dict({"image_url": image}))['titles']
    print(out)
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
    print(keywords)
    return ' '.join(keywords)

def parse_wallmart(keywords):
    products = wapy.search(' '.join(keywords))
    out = {}
    out['name'] = products[0].name
    out['rating'] = products[0].customer_rating
    out['price'] = products[0].sale_price
    return json.dumps(out)

class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(fh.read().encode())

    def do_POST(self):
        self.send_response(200)
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        with open('/var/www/html/image.jpg', 'wb') as fh:
            fh.write(data)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(parse_wallmart(parse_image('http://45.33.95.66/image.jpg')).encode())

server = HTTPServer(('', 8081), StoreHandler)
server.serve_forever()

