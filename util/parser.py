import requests, json
import urllib.request

def getJson(link):
    r=requests.get(link)
    return json.loads(r.content)


def getHTML(link):
    webUrl  = urllib.request.urlopen(link)
    data = webUrl.read()
    return data