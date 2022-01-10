import regex


import gzip, regex

whitespace_pattern = regex.compile("\s+")

def read_state(filename):
    tokens = []
    with gzip.open(filename, "rt", encoding="UTF8") as reader:
        for line in reader:
            if not line.startswith("#"):
                tokens.append(parse_line(line))
    return tokens

def parse_line(line):
    fields = whitespace_pattern.split(line.rstrip())
    if len(fields) == 6: # mallet format
        return (fields[0], fields[4], fields[5])
    elif len(fields) == 3: # doc, word, topic
        return (fields[0], fields[1], fields[2])
    else:
        print("unrecognized line format")

