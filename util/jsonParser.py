import requests, json

def getJson(link):
    r=requests.get(link)
    return json.loads(r.content)