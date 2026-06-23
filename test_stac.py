import urllib.request
import json

url = "http://127.0.0.1:8000/api/v1/farms/api/stac-ndvi/"
data = json.dumps({
    "polygon": [
        [75.8340, 30.9010],
        [75.8350, 30.9010],
        [75.8350, 30.9020],
        [75.8340, 30.9020],
        [75.8340, 30.9010]
    ]
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Error code:", e.code)
    print("Error body:", e.read().decode('utf-8')[:500])
except Exception as e:
    print("Other Exception:", e)
