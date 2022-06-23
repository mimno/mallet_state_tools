import sys
import state, metrics
from collections import Counter

word_counts = Counter()
word_topic_pair_counters = {}
word_left_topics = {}
word_right_topics = {}

left_tokens = state.read_state(sys.argv[1])
right_tokens = state.read_state(sys.argv[2])

line_num = 0
for fields1, fields2 in zip(left_tokens, right_tokens):
    if fields1[1] != fields2[1]:
        print(f"strings don't match at {line_num}: {fields1[1]} {fields2[1]}")
        break
    
    left_topic = fields1[2]
    right_topic = fields2[2]

    word = fields1[1]
    word_counts[word] += 1
    if not word in word_topic_pair_counters:
        word_topic_pair_counters[word] = Counter()
        word_left_topics[word] = Counter()
        word_right_topics[word] = Counter()
    
    topic_pair = f"{left_topic} {right_topic}"
    word_topic_pair_counters[word][topic_pair] += 1
    word_left_topics[word][left_topic] += 1
    word_right_topics[word][right_topic] += 1

    line_num += 1

for word, c in word_counts.most_common(2000):
    left_entropy = metrics.counter_entropy(word_left_topics[word], word_counts[word])
    right_entropy = metrics.counter_entropy(word_right_topics[word], word_counts[word])
    joint_entropy = metrics.counter_entropy(word_topic_pair_counters[word], word_counts[word])
    mutual_info = left_entropy + right_entropy - joint_entropy

    if left_entropy + right_entropy == 0.0:
        normalized_mi = 1
    else:
        normalized_mi = (2 * mutual_info) / (left_entropy + right_entropy)
        
    #print(word_topic_pair_counters[word])
    print(f"{left_entropy: 2.3f}\t{right_entropy: 2.3f}\t{joint_entropy: 2.3f}\t{mutual_info: 2.3f}\t{normalized_mi: 1.3f}\t{c}\t{word}")

