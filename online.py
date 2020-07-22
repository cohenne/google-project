import string
from auto_complete_data import AutoCompleteData

from offline import data_dict, sentences


def get_score(word, decrease):
    return len(word)*2 - decrease


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
                return word.replace(word[index], word[index] + i),  detraction*2
    return None, 0


def add_to_result(senten, fix_word, result, detraction, string):
    senten = data_dict[fix_word][:(5 - len(senten))]
    result += [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset,
                                get_score(string, detraction)) for index in senten]


def find_sequence(string):
    detraction = 0
    senten = data_dict[string][:5]
    result = [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset, get_score(string, detraction)) for index in senten]

    # if there are not enough suitable sequences
    # the best scores given when replacing a character Except from the first character
    # the next best case is delete or add the 4th character
    # after try to replace the first character
    # and the final try is to delete or add a character

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

        fix_word, detraction = delete_unnecessary_char(string, 0, len(string))
        add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < 5:
        fix_word, detraction = add_missed_char(string, 0, len(string))
        add_to_result(senten, fix_word, result, detraction, string)

    return result[:5]


