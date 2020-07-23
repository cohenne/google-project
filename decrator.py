def replace_char(word, start, end):
    for index in range(end-1, start-1, -1):
        for i in string.ascii_lowercase:
            if word.replace(word[index], i, 1) in data_dict.keys():
                detraction = (RESULT_LEN - index) if index < RESULT_LEN else 1
                return word.replace(word[index], i, 1), detraction

    return None, 0


def delete_unnecessary_char(word, start, end):
    for index in range(end-1, start-1, -1):
        if word.replace(word[index], "", 1) in data_dict.keys():
            detraction = 5 - index if index < RESULT_LEN else 1
            return word.replace(word[index], "", 1), detraction*2

    return None, 0


def add_missed_char(word, start, end):
    for index in range(end-1, start-1, -1):
        for i in string.ascii_lowercase:
            if word.replace(word[index], word[index] + i) in data_dict.keys():
                detraction = (RESULT_LEN - index) if index < RESULT_LEN else 1
                return word.replace(word[index], word[index] + i),  detraction*2
    return None, 0