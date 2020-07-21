import re
from collections import defaultdict


words = ["hello world", "nice world", "wow beautiful", "I am", "hi", "hii"]


def find_sequence(string):
    indexes = data_dict[string][:5]
    return [words[i] for i in indexes]
    # return words[data_dict[string].get(0)]


def format_line(line):
    return re.sub(' +', ' ', line).lower()


def all_sub_words(line):
    return [line[i: j] for i in range(len(line)) for j in range(i + 1, len(line) + 1)]


data_dict = defaultdict(list)


def main():
    x_file = open("some_file.txt", "r")
    x_line = x_file.readlines()

    # for line in x_line:
    #     #     line = format_line(line)
    #     #     sub_words = all_sub_words(line)
    #     #     for word in sub_words:
    #     #         data_dict[word] = 1
    #     #     for data in data_dict.keys():
    #     #         print(data)

    for i in range(len(words)):
        line = format_line(words[i])
        sub_words = all_sub_words(line)
        for word in sub_words:
            data_dict[word].append(i)

    x_file.close()


if __name__ == '__main__':

    main()
    print(find_sequence("hello"))
    print(find_sequence("ell"))
    print(find_sequence("world"))
    print(find_sequence("i"))



