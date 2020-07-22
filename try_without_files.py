
# This file is intended to check the correctness of the function logic without integrating the whole system

import string
sentences = ["hello", "nechama", "bracha"]


def replace_char(word):
    word = word[::-1]
    for index, char in enumerate(word):
        for i in string.ascii_lowercase:
            if word.replace(char, i, 1) in sentences[0][::-1]:# ?
                return len(sentences[0]) - index
    return -1


def delete_unnecessary_char(word):
    word = word[::-1]
    for char in word:
        if word.replace(char, "", 1) in sentences[0][::-1]:
            return len(sentences[0]) - word.index(char)
    return -1


def add_missed_char(word):
    # add char at the end of the word
    for i in string.ascii_lowercase:
        if word +i in sentences[0][::-1]:
            return len(sentences[0])

    # add char In the middle of the word
    word = word[::-1]
    for index, char in enumerate(word):
        for i in string.ascii_lowercase:
            print(word.replace(char, char+i, 1)[::-1])
            if word.replace(char, char + i, 1) in sentences[0][::-1]:
                return len(sentences[0]) - index + 1
    return -1


print(replace_char("helro"))
print(delete_unnecessary_char("hello"))
print(add_missed_char("hell"))

