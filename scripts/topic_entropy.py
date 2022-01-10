import gzip, sys, regex
from collections import Counter
import numpy as np

whitespace_pattern = regex.compile("\s+")

lines1 = []
lines2 = []

left_topic_totals = Counter()
right_topic_totals = Counter()
left_topic_words = {}
right_topic_words = {}
left_topic_topics = {}
right_topic_topics = {}

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
    left_topic = fields1[2]
    right_topic = fields2[2]

    left_topic_totals[left_topic] += 1
    right_topic_totals[right_topic] += 1

    if not left_topic in left_topic_words:
        left_topic_words[left_topic] = Counter()
        left_topic_topics[left_topic] = Counter()

    if not right_topic in right_topic_words:
        right_topic_words[right_topic] = Counter()
        right_topic_topics[right_topic] = Counter()
    
    left_topic_words[left_topic][word] += 1
    left_topic_topics[left_topic][right_topic] += 1

    right_topic_words[right_topic][word] += 1
    right_topic_topics[right_topic][left_topic] += 1

    line_num += 1

def counter_entropy(counts, total):
    entropy = 0.0
    for pair, c in counts.most_common():
        entropy += c * np.log(c)
    entropy /= total
    entropy += np.log(total)
    return entropy

for left_topic, c in left_topic_totals.most_common():
    top_words = " ".join([w for w,c in left_topic_words[left_topic].most_common(20)])
    entropy = counter_entropy(left_topic_topics[left_topic], left_topic_totals[left_topic])
    print(f"left\t{entropy: 2.3f}\t{c}\t{left_topic}\t{top_words}")

for right_topic, c in right_topic_totals.most_common():
    top_words = " ".join([w for w,c in right_topic_words[right_topic].most_common(20)])
    entropy = counter_entropy(right_topic_topics[right_topic], right_topic_totals[right_topic])
    print(f"right\t{entropy: 2.3f}\t{c}\t{right_topic}\t{top_words}")