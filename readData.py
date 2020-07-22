import re, string
from collections import defaultdict, namedtuple
from AutoCompleteData import AutoCompleteData
from pathlib import Path

subString = namedtuple('subString', ['id', 'offset'])
sentence_path = namedtuple('sentence_url', ['sentence', 'path'])
sentences_index = 0
sentences = {}
data_dict = defaultdict(list)


def replace_char(word):
    # word = word[::-1]
    for char in word:
        for i in string.ascii_lowercase:
            if word.replace(char, i, 1) in data_dict.keys():
                return word.replace(char, i, 1)
    return None


def find_sequence(string):
    senten = data_dict[string][:5]

    if len(senten) < 5:
        fix_word = replace_char(string)
        senten += data_dict[fix_word][:(5 - len(senten))]

    return [AutoCompleteData(sentences[index.id].sentence, sentences[index.id].path, index.offset, get_score(sentences[index.id].sentence, string)) for index in senten]


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


def delete_unnecessary_char(word):
    pass
    #word = word[::-1]
    #for index, char in enumerate(word):
     #   if word.replace(char, "") in sentences[index].sentence[::-1]:
      #      return word.index(char)
    #return -1


def add_missed_char(word):
    pass
#     word = word[::-1]
#     for index, char in enumerate(word):
#         for i in string.ascii_lowercase:
#             if word.replace(char, char + i) in sentences[index].sentence[::-1]:
#                 return index + 1
#     return -1


def is_best_score(new_sentence, sentences):
    for sentence in sentences:
        # choose the best score
        pass


def read_data(file_name):
    x_file = open(file_name, "r")
    x_line = x_file.read().splitlines()
    global sentences_index

    for line in x_line:
        sentences[sentences_index] = sentence_path(line, file_name)
        line_ = format_line(line)
        sub_words = all_sub_words(line)

        for word in sub_words:
            # if the sentences already exists
            if line not in (sentences[sentence_.id].sentence for sentence_ in data_dict[word]):
                if len(data_dict[word]) < 5:
                    data_dict[word].append(subString(sentences_index, line.index(word)))
                else:
                    is_best_score(word, data_dict[word])

        # for word in sub_words:
        #     if len(data_dict[word]) < 5:
        #         if line not in (sentences[sentence_.id].sentence for sentence_ in data_dict[replace_char(word)]):
        #             data_dict[word].append(subString(sentences_index, line.index(word)))

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
    #print(delete_unnecessary_char("Itt is not possible to use these functions on objects that are not"))
    x = input("The system is ready. Enter your text:")

    while x:
        if x[-1] != '#':
            x = format_line(x)
            suggestions = find_sequence(x)

            if suggestions:
                print(f"There are {len(suggestions)} suggestions")
                for i in range(len(suggestions)):
                    print(f'{i + 1}. {suggestions[i].get_complete_sentence()} , path = {suggestions[i].get_source_text()}')

            else:
                print("There are'nt suggestions")

            print(x, end='')
            x += input()

        else:
            x = input("Enter your text:")



