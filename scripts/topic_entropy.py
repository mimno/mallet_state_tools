import sys
import state
import metrics
from collections import Counter

left_topic_totals = Counter()
right_topic_totals = Counter()
left_topic_words = {}
right_topic_words = {}
left_topic_topics = {}
right_topic_topics = {}

left_tokens = state.read_state(sys.argv[1])
right_tokens = state.read_state(sys.argv[2])

line_num = 0
for fields1, fields2 in zip(left_tokens, right_tokens):

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

for left_topic, c in left_topic_totals.most_common():
    top_words = " ".join([w for w,c in left_topic_words[left_topic].most_common(20)])
    entropy = metrics.counter_entropy(left_topic_topics[left_topic], left_topic_totals[left_topic])
    print(f"left\t{entropy: 2.3f}\t{c}\t{left_topic}\t{top_words}")

for right_topic, c in right_topic_totals.most_common():
    top_words = " ".join([w for w,c in right_topic_words[right_topic].most_common(20)])
    entropy = metrics.counter_entropy(right_topic_topics[right_topic], right_topic_totals[right_topic])
    print(f"right\t{entropy: 2.3f}\t{c}\t{right_topic}\t{top_words}")