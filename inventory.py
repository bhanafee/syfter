
def extract_gav(entry):
    fields = entry.strip().split(':', 2)
    if len(fields) == 3:
        g, a, v = fields
        return {
            "groupId": g,
            "artifactId": a,
            "version": v
        }
