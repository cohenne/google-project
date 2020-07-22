import string
from collections import defaultdict, namedtuple
from AutoCompleteData import AutoCompleteData
from pathlib import Path

from utils import format_line, all_sub_words


subString = namedtuple('subString', ['id', 'score', 'offset'])
sentence_path = namedtuple('sentence_url', ['sentence', 'path'])
sentences_index = 0
sentences = {}
data_dict = defaultdict(list)


def replace_char(word):
    for index, char in enumerate(word):
        for i in string.ascii_lowercase:
            if word.replace(char, i, 1) in data_dict.keys():
                detraction = 5 - index if index < 5 else 1
                return word.replace(char, i, 1), detraction
    return None, 0


def delete_unnecessary_char(word):
    for index, char in enumerate(word):
        if word.replace(char, "", 1) in data_dict.keys():
            detraction = 5 - index if index < 5 else 1
            return word.replace(char, "", 1), detraction*2
    return None, 0


def add_missed_char(word):
    for index, char in enumerate(word):
        for i in string.ascii_lowercase:
            if word.replace(char, char + i) in data_dict.keys():
                detraction = (5 - index) if index < 5 else 1
                return word.replace(char, char + i),  detraction*2
    return None, 0


def find_sequence(string):
    detraction = 0
    senten = data_dict[string][:5]
    result = [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset, get_score(string, detraction)) for index in senten]

    if len(result) < 5:
        fix_word, detraction = replace_char(string)
        senten = data_dict[fix_word][:(5 - len(senten))]
        result += [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset,
                                   get_score(string, detraction)) for index in senten]

    if len(result) < 5:
        fix_word, detraction = delete_unnecessary_char(string)
        senten = data_dict[fix_word][:(5 - len(senten))]
        result += [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset,
                                    get_score(string, detraction)) for index in senten]

    if len(result) < 5:
        fix_word, detraction = delete_unnecessary_char(string)
        senten = data_dict[fix_word][:(5 - len(senten))]
        result += [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset,
                                    get_score(string, detraction)) for index in senten]

    return result


def get_score(string, decrease):
    # print(len(string))
    # print(decrease)
    return len(string)*2 - decrease


def is_best_score(new_sentence, sentences):
    for sentence in sentences:
        # choose the best score
        pass


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
            if line not in [sentences[sentence_.id].sentence for sentence_ in data_dict[word]]:
                if len(data_dict[word]) < 5:
                    data_dict[word].append(subString(sentences_index, 0, line_.index(word)))

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


if __name__ == '__main__':
    print("Loading the file and preparing the system....")
    init()
    x = input("The system is ready. Enter your text:")

    while x:
        if x[-1] != '#':
            x = format_line(x)
            suggestions = find_sequence(x)

            if suggestions:
                print(f"There are {len(suggestions)} suggestions")

                for i in range(len(suggestions)):
                    print(f'{i + 1}. {suggestions[i].get_complete_sentence()} , path = {suggestions[i].get_source_text()}, score = {suggestions[i].get_score()}')

            else:
                print("There are'nt suggestions")

            print(x, end='')
            x += input()
        else:
            x = input("Enter your text:")