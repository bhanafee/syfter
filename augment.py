import urllib.error
import urllib.request

def find_date(current):
    """
    Constructs a Maven query based on the given artifact metadata and retrieves
    the artifact's timestamp, if available.

    Parameters:
        current (dict): A dictionary representing the current artifact metadata.
                        Expected structure:
                          {
                              "groupId": str,
                              "artifactId": str,
                              "version": str
                          }

    Returns:
        dict: A dictionary containing the artifact's metadata, with the keys:
              - groupId: The group ID of the artifact.
              - artifactId: The artifact ID.
              - version: The artifact's version.
              - timestamp (optional): The artifact's timestamp, if available.

    Raises:
        TypeError: If the `current` parameter is not a dictionary.
        KeyError: If required keys (`groupId`, `artifactId`, `version`) are missing.
        ValueError: If the query to Maven fails.
    """
    # Validate input
    if not isinstance(current, dict):
        raise TypeError("Input parameter `current` must be a dictionary.")
    required_keys = ["groupId", "artifactId", "version"]
    for key in required_keys:
        if key not in current:
            raise KeyError(f"Missing required key '{key}' in `current` dictionary.")

    # Construct the query string
    query = (
        f"g:{current['groupId']}+AND+"
        f"a:{current['artifactId']}+AND+"
        f"v:{current['version']}"
    )

    # Perform the Maven query
    query_result = query_maven(query)

    # Build the result dictionary
    result = {
        "groupId": current["groupId"],
        "artifactId": current["artifactId"],
        "version": current["version"]
    }

    if query_result is not None and "timestamp" in query_result:
        result["timestamp"] = query_result["timestamp"]

    return result


def find_latest(current):
    """
    Finds the latest version and timestamp of an artifact based on its groupId and artifactId.

    Parameters:
        current (dict): A dictionary representing the current artifact metadata.
                        Expected structure:
                          {
                              "groupId": str,
                              "artifactId": str
                          }

    Returns:
        dict: A dictionary containing the latest artifact metadata, with the fields:
              - groupId: The group ID of the artifact.
              - artifactId: The artifact ID.
              - version (optional): The latest version of the artifact, if available.
              - timestamp (optional): The timestamp of the latest version, if available.

    Raises:
        TypeError: If `current` is not a dictionary.
        KeyError: If required keys (`groupId`, `artifactId`) are missing in `current`.
        ValueError: If the query to Maven fails or returns an invalid response.
    """
    # Validate input
    if not isinstance(current, dict):
        raise TypeError("Input parameter `current` must be a dictionary.")
    required_keys = ["groupId", "artifactId"]
    for key in required_keys:
        if key not in current:
            raise KeyError(f"Missing required key '{key}' in `current` dictionary.")

    # Construct the query
    query = f"g:{current['groupId']}+AND+a:{current['artifactId']}"

    # Perform the Maven query
    query_result = query_maven(query)

    # Build the result dictionary
    result = {
        "groupId": current["groupId"],
        "artifactId": current["artifactId"],
    }

    if query_result is not None:
        # Add the latest version and timestamp if available
        if "latestVersion" in query_result:
            result["version"] = query_result["latestVersion"]
        if "timestamp" in query_result:
            result["timestamp"] = query_result["timestamp"]

    return result

import urllib.request
import json


def query_maven(query, base_url="https://search.maven.org/solrsearch/select?q="):
    """
    Queries the Maven Central Repository using the provided query string and retrieves the first result, if available.

    Parameters:
        query (str): The search query to be sent to the Maven Central Repository.
                     Example: "g:com.example+AND+a:example-artifact".
        base_url (str): The base URL for Maven Central search API (default: "https://search.maven.org/solrsearch/select?q=").

    Returns:
        dict: The first document in the search response, if results are found.
        None: If no results are found or the query fails.

    Raises:
        ValueError: If the query is not a valid string or empty.
        ConnectionError: If there is a problem connecting to the Maven Central API.
        JSONDecodeError: If the response data is not valid JSON.
        KeyError: If the expected keys are not present in the API response.
    """
    # Validate input
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    # Construct the full URL
    url = base_url + query

    try:
        # Perform the HTTP GET request
        with urllib.request.urlopen(url) as response:
            # Decode the response data
            data = response.read().decode("utf-8")
            # Parse the JSON response
            entry = json.loads(data)
            # Check for results in the response
            if entry.get("response", {}).get("numFound", 0) == 0:
                return None
            # Return the first document
            return entry["response"]["docs"][0]

    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to connect to Maven API: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON response: {e}")
    except KeyError as e:
        raise KeyError(f"Unexpected response structure from Maven API: {e}")

