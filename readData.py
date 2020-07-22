import re, string
from collections import defaultdict, namedtuple
from AutoCompleteData import AutoCompleteData
from pathlib import Path


sentences = {}
data_dict = defaultdict(list)
subString = namedtuple('subString', ['id', 'offset'])
sentence_path = namedtuple('sentence_url', ['sentence', 'path'])
sentences_index = 0


def find_sequence(string):
    indexes = data_dict[string][:5]
    return [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset, get_score(sentences[index.id].sentence, string)) for index in indexes]


def get_score(sentences, string, decrease=0):
    return len(string)*2 - decrease


def format_line(line):
    line = line.translate(line.maketrans("", "", string.punctuation))
    return re.sub(' +', ' ', line).lower()


def all_sub_words(line):
    return [line[i: j] for i in range(len(line)) for j in range(i + 1, len(line) + 1)]

# are there data file directory out of our project ?
# def find_path(file_name):
#     # return os.path.abspath(file_name)
#     for root, dirs, files in os.walk(r"C:\Users\Lenovo\Documents\google_project\c-api"):
#         for name in files:
#             if name == str(file_name) + ".txt":
#                 return os.path.abspath(os.path.join(root, name))
#     return False


def read_data(file_name):
    x_file = open(file_name, "r")
    x_line = x_file.read().splitlines()
    global sentences_index

    for line in x_line:
        line_ = format_line(line)
        sub_words = all_sub_words(line_)

        for word in sub_words:
            if sentences_index not in data_dict[word]:
                data_dict[word].append(subString(sentences_index, line_.index(word)))

        sentences[sentences_index] = sentence_path(line, file_name)
        sentences_index += 1


def init():

    directory_list = ["c-api"]
    while len(directory_list) != 0:
        basepath = Path(directory_list.pop(-1))
        for entry in basepath.iterdir():
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
                    print(f'{i+1}. {suggestions[i].get_complete_sentence()} , path = {suggestions[i].get_source_text()}')

            else:
                print("There are'nt suggestions")

            print(x, end='')
            x += input()

        else:
            x = input("Enter your text:")



