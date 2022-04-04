import sys, regex, itertools
from collections import Counter

iter_pattern = regex.compile("^<(\d+)>")
topic_pattern = regex.compile("^(\d+)\t(\d+\.\d+)\t(.*)")

current_iteration = 0

topic_counters = {}

with open(sys.argv[1]) as reader:
    for line in reader:
        if line.startswith("<"):
            match = iter_pattern.search(line)
            current_iteration = int(match.group(1))
        elif current_iteration > 500:
            match = topic_pattern.search(line)
            if match != None:
                topic = int(match.group(1))
                alpha = float(match.group(2))
                words = match.group(3).split(" ")

                if not topic in topic_counters:
                    topic_counters[topic] = Counter()
                
                for rank, word in enumerate(words):
                    topic_counters[topic][word] += len(words) - rank

def jaccard(a, b):
    set_a = set(a.keys())
    set_b = set(b.keys())
    return len(set_a & set_b) / len(set_a | set_b)

def character_trigrams(strings):
    output = Counter()

    for s in strings:
        padded_string = "  " + s.replace("v", "u") + "  "
        for position in range(len(padded_string) - 2):
            trigram = padded_string[position:(position+3)]
            output[trigram] += 1

    return output

print("getting top words")
topic_ids = list(topic_counters.keys())
topic_words = {}
topic_trigrams = {}
for topic in topic_ids:
    topic_words[topic] = [w for w, c in topic_counters[topic].most_common(15)]
    topic_trigrams[topic] = character_trigrams(topic_words[topic])

topic_pair_scores = []
for t1, t2 in itertools.combinations(topic_ids, 2):
    topic_pair_scores.append((jaccard(topic_trigrams[t1], topic_trigrams[t2]), t1, t2))

for score, t1, t2 in sorted(topic_pair_scores, reverse=True):
    print(score, " ".join(topic_words[t1]), " | ", " ".join(topic_words[t2]))