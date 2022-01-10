import sys
import state, metrics
from collections import Counter

word_counts = Counter()
word_topic_pair_counters = {}

left_tokens = state.read_state(sys.argv[1])
right_tokens = state.read_state(sys.argv[2])

line_num = 0
for fields1, fields2 in zip(left_tokens, right_tokens):
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

for word, c in word_counts.most_common(2000):
    entropy = metrics.counter_entropy(word_topic_pair_counters[word], word_counts[word])
    print(f"{entropy: 2.3f}\t{c}\t{word}")