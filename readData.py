import re
from collections import defaultdict
from AutoCompleteData import AutoCompleteData
from pathlib import Path

words = []

sentence_index = 0

data_dict = defaultdict(list)


def find_sequence(string):
    indexes = data_dict[string][:5]
    return [words[i] for i in indexes]


def format_line(line):
    return re.sub(' +', ' ', line).lower()


def all_sub_words(line):
    return [line[i: j] for i in range(len(line)) for j in range(i + 1, len(line) + 1)]


def read_data(file_name):
    x_file = open(file_name, "r")
    x_line = x_file.readlines()
    for line in x_line:
        line = format_line(line)
        sub_words = all_sub_words(line)
        for word in sub_words:
            global sentence_index
            if sentence_index not in data_dict[word]:
                data_dict[word].append(sentence_index)
        sentence_index += 1
        words.append(AutoCompleteData(line, file_name))


def init():

    directory_list = ["c-api"]
    while len(directory_list) != 0:
        basepath = Path(directory_list.pop(-1))
        for entry in basepath.iterdir():
            if entry.is_dir():
                directory_list.append(entry)
            else:
                read_data(entry)


if __name__ == '__main__':

    print("Loading the file and preparing the system....")
    init()
    x = input("The system is ready. Enter your text:")

    while x:
        print("There are 5 suggestions")
        suggestions = find_sequence(x)

        for i in range(len(suggestions)):
            print(f'{i+1}. {suggestions[i].get_complete_sentence()}', end='')

        if x[-1] != '#':
            print(x, end='')
            x += input()
        else:
            x = input()



