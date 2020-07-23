import re
import string


def format_line(line):
    line = line.translate(line.maketrans("", "", string.punctuation))
    return re.sub(' +', ' ', line).lower()


def all_sub_words(line):
    return [line[i: j] for i in range(len(line)) for j in range(i + 1, len(line) + 1)]
