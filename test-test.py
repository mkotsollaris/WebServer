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
    print(' '.join(keywords))
    outa = json.loads(requests.get("http://api.walmartlabs.com/v1/search?apiKey=frt6ajvkqm4aexwjksrukrey&query=" + keywords + "&format=json").text)
    outa['items'][0]['name'][0]
    item_id = outa['items'][0]['itemId']
    out = {}
    out['name'] = outa['items'][0]['name']
#    out['rating'] = outa['items'][0]['customerRating']
    out['price'] = outa['items'][0]['salePrice']
    print(outa)
    return json.dumps(out)

class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Got something")
        self.send_response(200)
        #self.query_string = self.path.split('image=')[1]
        #with open('/var/www/html/image.jpg', 'wb') as fh:
        #    fh.write(self.query_string.decode('base64'))
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write('1'.encode("utf-8"))

    def do_POST(self):
        print("Got something")
        self.send_response(200)
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        with open('/var/www/html/image.jpg', 'wb') as fh:
            fh.write(data)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(parse_wallmart(parse_image('http://45.33.95.66/image.jpg')).encode("utf-8"))

server = HTTPServer(('', 8081), StoreHandler)
server.serve_forever()

