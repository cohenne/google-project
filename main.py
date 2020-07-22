"""
The system is currently working on a small number of files,
because the data is saved on disk.
The next feature will save the data in an file(Probably of the json type)
"""

from offline import init
from utils import format_line
from online import find_sequence


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
                    print(f'{i + 1}. {suggestions[i].get_complete_sentence()} , path = {suggestions[i].get_source_text()}')

            else:
                print("There are'nt suggestions")

            print(x, end='')
            x += input()

        else:
            x = input("Enter your text:")

