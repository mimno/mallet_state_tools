import numpy as np

# -p \log p
# -k/n \log k/n
# -k/n log k + k/n log n

def counter_entropy(counts, total):
    entropy = 0.0
    for pair, c in counts.most_common():
        entropy -= c * np.log(c)
    entropy /= total
    entropy += np.log(total)
    return entropy
