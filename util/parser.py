import requests, json
import urllib.request

def getJson(link, *header):
    if len(header) > 0:
        header = {header[0]: header[1]}
        r=requests.get(link,headers=header)
        return json.loads(r.content)
    else:
        r=requests.get(link)
        return json.loads(r.content)


def getHTML(link):
    webUrl  = urllib.request.urlopen(link)
    data = webUrl.read()
    return data