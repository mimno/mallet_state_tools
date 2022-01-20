import state
import topic_model
from collections import Counter
import sys, itertools

model = topic_model.TopicModel()
for filename in sys.argv[1:]:
    print(f"reading {filename}")
    sampling_state = state.read_state(filename)
    print("adding")
    model.add_state(sampling_state)

def character_trigrams(strings):
    output = Counter()

    for s in strings:
        padded_string = "  " + s + "  "
        for position in range(len(padded_string) - 2):
            trigram = padded_string[position:(position+3)]
            output[trigram] += 1

    return output

print("getting top words")
topic_ids = list(model.topic_word_counters.keys())
topic_words = {}
topic_trigrams = {}
for topic in topic_ids:
    topic_words[topic] = [w for w, c in model.topic_word_counters[topic].most_common(15)]
    topic_trigrams[topic] = character_trigrams(topic_words[topic])

def jaccard(a, b):
    set_a = set(a.keys())
    set_b = set(b.keys())
    return len(set_a & set_b) / len(set_a | set_b)

topic_pair_scores = []
for t1, t2 in itertools.combinations(topic_ids, 2):
    topic_pair_scores.append((jaccard(topic_trigrams[t1], topic_trigrams[t2]), t1, t2))

for score, t1, t2 in sorted(topic_pair_scores, reverse=True):
    print(score, " ".join(topic_words[t1]), " | ", " ".join(topic_words[t2]))