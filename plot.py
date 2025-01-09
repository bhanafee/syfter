import matplotlib.pyplot as plt

def plot(scores, labelthreshold):
    """
    Plot the technical debt of an application based on dependency scores.

    Parameters:
        scores (list): A list of dictionaries, each containing keys:
                       'currency', 'ecosystem', and 'artifactId'.
        labelthreshold (float): A threshold above which dependencies are labeled.

    Returns:
        None: Displays a scatter plot.
    """
    # Validate inputs
    if not isinstance(scores, list):
        raise ValueError("Scores input must be a list of dictionaries.")
    if not all(('currency' in entry and 'ecosystem' in entry and 'artifactId' in entry) for entry in scores):
        raise ValueError("Each score must have 'currency', 'ecosystem', and 'artifactId'.")
    if not isinstance(labelthreshold, (int, float)):
        raise ValueError("Labelthreshold must be a numeric value.")

    try:
        # Extract data
        currency = [entry['currency'] for entry in scores]
        ecosystem = [entry['ecosystem'] for entry in scores]
        labels = [entry['artifactId'] for entry in scores]

        # Create scatter plot
        plt.scatter(ecosystem, currency)

        # Add labels for significant points
        for i in range(len(labels)):
            if currency[i] > labelthreshold or ecosystem[i] > labelthreshold:
                plt.text(ecosystem[i], currency[i] + 0.5, labels[i], fontsize=9, ha='left')

        # Label axes and add title
        plt.xlabel('Currency of components')
        plt.ylabel('Recency of ecosystem updates')
        plt.title('Technical debt of application')

        # Show the plot
        plt.show()

    except Exception as e:
        raise RuntimeError(f"An error occurred while plotting: {e}")
