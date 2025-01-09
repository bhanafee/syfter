
import numpy
import matplotlib.pyplot as plt

def plot(scores, labelthreshold):
    currency = [entry['currency'] for entry in scores]
    ecosystem = [entry['ecosystem'] for entry in scores]
    label = [entry['artifactId'] for entry in scores]
    plt.scatter(ecosystem, currency)
    for i in range(len(ecosystem)):
        if (currency[i] > labelthreshold or ecosystem[i] > labelthreshold):
            plt.text(ecosystem[i] + 1, currency[i], label[i], fontsize=9, ha='left')
    plt.xlabel('Currency of components')
    plt.ylabel('Recency of ecosystem updates')
    plt.title('Technical debt of application')
    plt.show()

