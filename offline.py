from collections import defaultdict, namedtuple
from pathlib import Path
import json

from utils import format_line, all_sub_words
RESULT_LEN = 5

subString = namedtuple('subString', ['id', 'score', 'offset'])
sentence_path = namedtuple('sentence_url', ['sentence', 'path'])
sentences_id = 0
sentences = {}
data_dict = defaultdict(list)


def read_data(file_name):
    x_file = open(file_name, "r")
    x_line = x_file.read().splitlines()
    global sentences_id
    line_number = 1

    for line in x_line:
        line_ = format_line(line)
        sub_words = all_sub_words(line_)
        sentences[sentences_id] = sentence_path(line, file_name)

        for word in sub_words:
            # prevent duplication of sentences
            if line not in [sentences[sentence_.id].sentence for sentence_ in data_dict[word]]:

                if len(data_dict[word]) < RESULT_LEN:
                    data_dict[word].append(subString(sentences_id, 0, line_number))

        sentences_id += 1
        line_number += 1


def init():

    directory_list = ["c-api"]

    while len(directory_list) != 0:
        base_path = Path(directory_list.pop(-1))

        for entry in base_path.iterdir():
            if entry.is_dir():
                directory_list.append(entry)

            else:
                read_data(entry)
