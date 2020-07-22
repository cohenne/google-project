import string
from collections import defaultdict, namedtuple
from AutoCompleteData import AutoCompleteData
from pathlib import Path

from utils import format_line, all_sub_words
from score import get_score, is_best_score


subString = namedtuple('subString', ['id', 'score', 'offset'])
sentence_path = namedtuple('sentence_url', ['sentence', 'path'])
sentences_index = 0
sentences = {}
data_dict = defaultdict(list)


def replace_char(word, start, end):
    for index in range(end-1, start-1, -1):
        for i in string.ascii_lowercase:

            if word.replace(word[index], i, 1) in data_dict.keys():
                detraction = (5 - index) if index < 5 else 1
                return word.replace(word[index], i, 1), detraction
    return None, 0


def delete_unnecessary_char(word, start, end):
    for index in range(end-1, start-1, -1):

        if word.replace(word[index], "", 1) in data_dict.keys():
            detraction = 5 - index if index < 5 else 1
            return word.replace(word[index], "", 1), detraction*2

    return None, 0


def add_missed_char(word, start, end):
    for index in range(end-1, start-1, -1):
        for i in string.ascii_lowercase:

            if word.replace(word[index], word[index] + i) in data_dict.keys():
                detraction = (5 - index) if index < 5 else 1
                return word.replace(word[index], word[index] + i), detraction*2
            return None, 0


def add_to_result(senten, fix_word, result, detraction, string):
     senten = data_dict[fix_word][:(5 - len(senten))]
     result += [AutoCompleteData(sentences[index.id].sentence,
sentences[index.id].path, index.offset,
                                 get_score(string, detraction)) for index
in senten]


def find_sequence(string):
     detraction = 0
     senten = data_dict[string][:5]
     result = [AutoCompleteData(sentences[index.id].sentence,
sentences[index.id].path, index.offset, get_score(string, detraction))
for index in senten]

     if len(result) < 5:
         if len(string) > 1:
             fix_word, detraction = replace_char(string, 1, len(string))
             add_to_result(senten, fix_word, result, detraction, string)

     if len(result) < 5:
         if len(string) > 3:
             fix_word, detraction = delete_unnecessary_char(string, 3, 4)
             add_to_result(senten, fix_word, result, detraction, string)

     if len(result) < 5:
         if len(string) > 3:
             fix_word, detraction = add_missed_char(string, 3, 4)
             add_to_result(senten, fix_word, result, detraction, string)

     if len(result) < 5:
         if len(string) > 0:
             fix_word, detraction = replace_char(string, 0, 1)
             add_to_result(senten, fix_word, result, detraction, string)

     if len(result) < 5:

         fix_word, detraction = delete_unnecessary_char(string, 0,
len(string))
         add_to_result(senten, fix_word, result, detraction, string)

     if len(result) < 5:
         fix_word, detraction = add_missed_char(string, 0, len(string))
         add_to_result(senten, fix_word, result, detraction, string)

     return result[:5]


def read_data(file_name):
     x_file = open(file_name, "r")
     x_line = x_file.read().splitlines()
     global sentences_index

     for line in x_line:
         line_ = format_line(line)
         sub_words = all_sub_words(line_)
         sentences[sentences_index] = sentence_path(line, file_name)

         for word in sub_words:
             # prevent duplication of sentences
             if line not in [sentences[sentence_.id].sentence for
sentence_ in data_dict[word]]:
                 if len(data_dict[word]) < 5:
                     data_dict[word].append(subString(sentences_index, 0,
line_.index(word)))

                 else:
                     is_best_score(word, data_dict[word])
         sentences_index += 1


def init():
     directory_list = ["c-api"]

     while len(directory_list) != 0:
         base_path = Path(directory_list.pop(-1))

         for entry in base_path.iterdir():
             if entry.is_dir():
                 directory_list.append(entry)

             else:
                 print(entry)
                 read_data(entry)