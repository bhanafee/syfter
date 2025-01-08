import urllib.request
import json
import time
import numpy
import matplotlib.pyplot as plt

def extract_gav(entry):
    fields = entry.strip().split(':', 2)
    if len(fields) == 3:
        g, a, v = fields
        return {
            "groupId": g,
            "artifactId": a,
            "version": v
        }

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

def days(milliseconds):
    return int(milliseconds / 1000 / 60 / 60 / 24)

def health(as_of, current, latest):
    score = {"groupId": current["groupId"],
             "artifactId": current["artifactId"],
             "version": current["version"]}
    score["latestVersion"] = latest["version"] if "version" in latest else current["version"]
    if "timestamp" in latest:
        score["ecosystem"] = days(as_of * 1000 - latest["timestamp"])
        score["currency"] = max(days(latest["timestamp"] - current["timestamp"]), 0) if "timestamp" in current else 0
    else:
        score["ecosystem"] = 0
        score["currency"] = 0
    return score


if __name__ == '__main__':
    now = int(time.time())
    scores = []
    with open('dependencies.txt', 'r') as f:
        for line in f:
            gav = extract_gav(line)
            if gav is None or "groupId" not in gav or "artifactId" not in gav:
                continue
            health_score = health(now, find_date(gav), find_latest(gav))
            scores.append(health_score)
            #currency.append(0 if "currency" not in health_score else health_score["currency"])
            #ecosystem.append(0 if "ecosystem" not in health_score else health_score["ecosystem"])
            #label.append(health_score["artifactId"])
            print(health_score)
    currency = [entry['currency'] for entry in scores]
    ecosystem = [entry['ecosystem'] for entry in scores]
    label = [entry['artifactId'] for entry in scores]
    plt.scatter(ecosystem, currency)
    plt.xlabel('Latest')
    plt.ylabel('Ecosystem')
    plt.title('Generay currency of application')
    plt.show()
 