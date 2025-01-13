import matplotlib.pyplot as plt

def plot(scores):
    """
    Plot the technical debt of an application based on dependency scores.

    Parameters:
        scores (list): A list of dictionaries, each containing keys:
                       'currency', 'ecosystem', and 'artifactId'.

    Returns:
        None: Displays a scatter plot.
    """
    # Validate inputs
    if not isinstance(scores, list):
        raise ValueError("Scores input must be a list of dictionaries.")
    if not all(('currency' in entry and 'ecosystem' in entry and 'artifactId' in entry) for entry in scores):
        raise ValueError("Each score must have 'currency', 'ecosystem', and 'artifactId'.")

    days_limit = (365 * 4) + 1    # ceiling on ages to show (one leap year every 4 years)
    currency_threshold = 365      # label artifacts where the version in use is much older than the latest
    ecosystem_threshold = 180     # label artifacts the ecosystem hasn't updated recently
    label_rotation = 30           # rotate labels to reduce overlap

    try:
        # Extract data
        currency = [entry['currency'] for entry in scores]
        ecosystem = [entry['ecosystem'] for entry in scores]
        labels = [entry['artifactId'] for entry in scores]

        # Label axes and add title
        plt.xlabel('Currency of components in use')
        plt.ylabel('Recency of ecosystem updates')
        plt.title('Technical debt of application')


        # Visualize on a log scale with a fixed limit so that graphs are visually comparable
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(0, days_limit)
        plt.ylim(0, days_limit)
        currency = [min(value, days_limit) for value in currency]
        ecosystem = [min(value, days_limit) for value in ecosystem]

        # Create scatter plot
        plt.scatter(currency, ecosystem)

        # Add labels for significant points
        for i in range(len(labels)):
            if currency[i] > currency_threshold or ecosystem[i] > ecosystem_threshold:
                plt.text(currency[i], ecosystem[i], labels[i], fontsize=9, ha='left', rotation=label_rotation)

        # Show the plot
        plt.show()

    except Exception as e:
        raise RuntimeError(f"An error occurred while plotting: {e}")
