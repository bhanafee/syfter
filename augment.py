import urllib.request
import json

def find_date(current):
    query = "g:" + current["groupId"] + "+AND+a:" + current["artifactId"] + "+AND+v:" + current["version"]
    queried = query_maven(query)
    result = {
        "groupId": current["groupId"],
        "artifactId": current["artifactId"],
        "version": current["version"]
    }
    if queried is not None and "timestamp" in queried:
        result["timestamp"] = queried["timestamp"]
    return result

def find_latest(current):
    query = "g:" + current["groupId"] + "+AND+a:" + current["artifactId"]
    queried = query_maven(query)
    result = {
        "groupId": current["groupId"],
        "artifactId": current["artifactId"]
    }
    if queried is not None:
        result["version"] = queried["latestVersion"]
        result["timestamp"] = queried["timestamp"]
    return result

def query_maven(query):
    url = "https://search.maven.org/solrsearch/select?q=" + query
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        entry = json.loads(data)
        if entry["response"]["numFound"] == 0:
            return None
        else:
            return entry["response"]["docs"][0]
