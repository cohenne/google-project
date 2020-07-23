import string

from auto_complete_data import AutoCompleteData
from offline import data_dict, sentences, RESULT_LEN


def get_score(word, decrease):
    return len(word)*2 - decrease


def change_decrator(f):
    def wrapped(word, start, end):
        for index in range(end - 1, start - 1, -1):
            for i in string.ascii_lowercase:
                if f(index, i, word) in data_dict.keys():
                    detraction = RESULT_LEN - index if index < RESULT_LEN else 1
                    return f(index, i, word), detraction * 2
        return None, 0
    return wrapped


@change_decrator
def add_missed_char(index, char, word):
    return word[:index] + (word[index]+char) + word[index + 1:]


@change_decrator
def replace_char(index, char, word):
    return word[:index-1] + char + word[index+1:]


def delete_unnecessary_char(word, start, end):
    for index in range(end-1, start-1, -1):
        if word[:index] + word[index+1:] in data_dict.keys():
            detraction = RESULT_LEN - index if index < RESULT_LEN else 1
            return word[:index] + word[index+1:], detraction*2

    return None, 0


def add_to_result(senten, fix_word, result, detraction, string):
    senten = data_dict[fix_word][:(RESULT_LEN - len(senten))]
    result += [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset,
                                get_score(string, detraction)) for index in senten]


def get_best_k_completions(string):
    detraction = 0
    senten = data_dict[string][:RESULT_LEN]
    result = [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset, get_score(string, detraction)) for index in senten]

    # if there are not enough suitable sequences
    # the best scores given when replacing a character except from the first character
    # the next best case is delete or add the 4th character
    # after try to replace the first character
    # and the final try is to delete or add a character

    if len(result) < RESULT_LEN:
        if len(string) > 1:
            fix_word, detraction = replace_char(string, 1, len(string))
            add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < RESULT_LEN:
        if len(string) > 3:
            fix_word, detraction = delete_unnecessary_char(string, 3, 4)
            add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < RESULT_LEN:
        if len(string) > 3:
            fix_word, detraction = add_missed_char(string, 3, 4)
            add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < RESULT_LEN:
        if len(string) > 0:
            fix_word, detraction = replace_char(string, 0, 1)
            add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < RESULT_LEN:

        fix_word, detraction = delete_unnecessary_char(string, 0, len(string))
        add_to_result(senten, fix_word, result, detraction, string)

    if len(result) < RESULT_LEN:
        fix_word, detraction = add_missed_char(string, 0, len(string))
        add_to_result(senten, fix_word, result, detraction, string)

    return result[:RESULT_LEN]


