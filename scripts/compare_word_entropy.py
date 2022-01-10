import gzip, sys, regex
from collections import Counter
import numpy as np

whitespace_pattern = regex.compile("\s+")

lines1 = []
lines2 = []

word_counts = Counter()
word_topic_pair_counters = {}

with gzip.open(sys.argv[1], "rt", encoding="UTF8") as reader1, gzip.open(sys.argv[2], "rt") as reader2:
    for line in reader1:
        if not line.startswith("#"):
            lines1.append(line)
    for line in reader2:
        if not line.startswith("#"):
            lines2.append(line)

def parse_line(line):
    fields = whitespace_pattern.split(line.rstrip())
    if len(fields) == 6: # mallet format
        return (fields[0], fields[4], fields[5])
    elif len(fields) == 3: # doc, word, topic
        return (fields[0], fields[1], fields[2])
    else:
        print("unrecognized line format")

line_num = 0
for line1, line2 in zip(lines1, lines2):
    fields1 = parse_line(line1)
    fields2 = parse_line(line2)
    
    if fields1[1] != fields2[1]:
        print(f"strings don't match at {line_num}: {fields1[1]} {fields2[1]}")
        break
    
    word = fields1[1]
    word_counts[word] += 1
    if not word in word_topic_pair_counters:
        word_topic_pair_counters[word] = Counter()
    
    topic_pair = f"{fields1[2]} {fields2[2]}"
    word_topic_pair_counters[word][topic_pair] += 1

    line_num += 1

def counter_entropy(counts, total):
    entropy = 0.0
    for pair, c in counts.most_common():
        entropy += c * np.log(c)
    entropy /= total
    entropy += np.log(total)
    return entropy

for word, c in word_counts.most_common(2000):
    entropy = counter_entropy(word_topic_pair_counters[word], word_counts[word])
    print(f"{entropy: 2.3f}\t{c}\t{word}")