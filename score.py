def convert_milliseconds_to_days(milliseconds):
    """
    Converts a duration in milliseconds to the equivalent number of whole days.

    Parameters:
        milliseconds (int or float): The duration in milliseconds.

    Returns:
        int: The number of whole days.

    Raises:
        ValueError: If the input is not a positive number.
        TypeError: If the input is not a number.
    """
    if not isinstance(milliseconds, (int, float)):
        raise TypeError("Input must be an integer or a float.")

    seconds_in_a_day = 86400  # 24 hours * 60 minutes * 60 seconds
    return int(milliseconds / 1000 / seconds_in_a_day)


def health(as_of, current, latest):
    """
    Calculates and returns the health score of a software artifact.

    Parameters:
        as_of (int): The current timestamp in seconds (e.g., UNIX epoch time).
        current (dict): A dictionary representing the current artifact version.
                        Expected structure:
                          {
                              "groupId": str,
                              "artifactId": str,
                              "version": str,
                              "timestamp": int (optional)
                          }
        latest (dict): A dictionary representing the latest known artifact version.
                       Expected structure:
                         {
                             "version": str (optional),
                             "timestamp": int (optional)
                         }

    Returns:
        dict: A dictionary containing the health score, with the keys:
              - groupId, artifactId, version
              - latestVersion
              - ecosystem: Days since the latest artifact was updated compared to `as_of`
              - currency: Age in days of the current version since the latest version's release
    """
    # Validate inputs
    if not isinstance(as_of, (int, float)):
        raise TypeError("The `as_of` parameter must be a number (seconds since epoch).")
    if not isinstance(current, dict) or not isinstance(latest, dict):
        raise TypeError("Both `current` and `latest` must be dictionaries.")
    required_keys = ["groupId", "artifactId", "version"]
    for key in required_keys:
        if key not in current:
            raise KeyError(f"Missing required key '{key}' in `current` dictionary.")

    # Default score structure
    score = dict(groupId=current["groupId"], artifactId=current["artifactId"], version=current["version"])

    # Latest version
    score["latestVersion"] = latest.get("version", current["version"])

    # Calculate ecosystem and currency
    if "timestamp" in latest:
        # Convert `as_of` to milliseconds (if `days` function works in ms units)
        time_diff = as_of * 1000 - latest["timestamp"]
        score["ecosystem"] = convert_milliseconds_to_days(time_diff)
        # Calculate currency
        if "timestamp" in current:
            currency_days = convert_milliseconds_to_days(latest["timestamp"] - current["timestamp"])
            score["currency"] = max(currency_days, 0)
        else:
            score["currency"] = 0
    else:
        score["ecosystem"] = 0
        score["currency"] = 0

    return score
