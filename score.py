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
