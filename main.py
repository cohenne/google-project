"""
The system is currently working on a small number of files,
because the data is saved on disk.
The next feature will save the data in an file(Probably of the json type)
"""

from offline import init
from utils import format_line
from online import get_best_k_completions


if __name__ == '__main__':
    STOP_INPUT = '#'
    print("Loading the file and preparing the system....")
    init()
    string_to_complete = input("The system is ready. Enter your text:")

    while string_to_complete:
        if string_to_complete[-1] != STOP_INPUT:
            string_to_complete = format_line(string_to_complete)
            suggestions = get_best_k_completions(string_to_complete)

            if suggestions:
                print(f"There are {len(suggestions)} suggestions")

                for i in range(len(suggestions)):
                    print(f'{i + 1}. {suggestions[i].get_complete_sentence()} , path = {suggestions[i].get_source_text()}')

            else:
                print("There are'nt suggestions")

            print(string_to_complete, end='')
            string_to_complete += input()

        else:
            string_to_complete = input("Enter your text:")

