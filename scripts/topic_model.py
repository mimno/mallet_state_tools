from collections import Counter

class TopicModel:
    topic_word_counters = {}
    topic_sizes = Counter()
    doc_topic_counters = {}
    doc_lengths = Counter()

    def add_state(self, state):
        for doc, word, topic in state:
            if not doc in self.doc_topic_counters:
                self.doc_topic_counters[doc] = Counter()
            if not topic in self.topic_word_counters:
                self.topic_word_counters[topic] = Counter()
            
            self.doc_topic_counters[doc][topic] += 1
            self.doc_lengths[doc] += 1

            self.topic_word_counters[topic][word] += 1
            self.topic_sizes[topic] += 1
    