import re
from collections import defaultdict
from AutoCompleteData import AutoCompleteData
# import os

words = [AutoCompleteData("hello world", ""), AutoCompleteData("nice world", ""), AutoCompleteData("wow beautiful", ""), AutoCompleteData("I am", ""), AutoCompleteData("hi", ""), AutoCompleteData("hii", "")]


def find_sequence(string):
    indexes = data_dict[string][:5]
    return [words[i] for i in indexes]


def format_line(line):
    return re.sub(' +', ' ', line).lower()


def all_sub_words(line):
    return [line[i: j] for i in range(len(line)) for j in range(i + 1, len(line) + 1)]


data_dict = defaultdict(list)


# def read_data(file_name):
#     x_file = open(file_name, "r")
#     x_line = x_file.readlines()
#     for i in range(len(x_line)):
#         line = format_line(words[i])
#         sub_words = all_sub_words(line)
#         for word in sub_words:
#             data_dict[word].append(i)


def init():
    # entries = os.listdir()
    # pass
    #
    for i in range(len(words)):
        line = format_line(words[i].get_complete_sentence())
        sub_words = all_sub_words(line)
        for word in sub_words:
            data_dict[word].append(i)


if __name__ == '__main__':

    print("Loading the file and preparing the system....")
    init()
    x = input("The system is ready. Enter your text:")
    while x:

        print("There are 5 suggestions")
        suggestions = find_sequence(x)
        for i in range(len(suggestions)):
            print(f'{i+1}. {suggestions[i].get_complete_sentence()}')
        if x[-1] != '#':
            print(x, end='')
            x += input()
        else:
            x = input()



