def extract_gav(entry):
    """
    Extract Group, Artifact, and Version (GAV) information from a Maven dependency string formatted as:
    'groupId:artifactId:version'.

    Parameters:
        entry (str): The input string containing the dependency in 'groupId:artifactId:version' format.

    Returns:
        dict: A dictionary with 'groupId', 'artifactId', and 'version' keys, if the input is properly formatted.
        None: If the input format is invalid.

    Raises:
        ValueError: If the input is not properly formatted or if it is not a string.
    """
    # Type check
    if not isinstance(entry, str):
        raise ValueError("Input must be a valid string in the format 'groupId:artifactId:version'.")

    # Normalize and split the input string
    fields = entry.strip().split(':', 2)

    # Validate number of fields
    if len(fields) != 3:
        print(f"Warning: Invalid GAV format: {entry.strip()}")
        return None  # or raise an exception like `raise ValueError("Invalid GAV format.")`

    # Map fields into a dictionary
    g, a, v = fields
    return {
        "groupId": g,
        "artifactId": a,
        "version": v
    }
