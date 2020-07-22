import readData

if __name__ == '__main__':
    print("Loading the file and preparing the system....")
    readData.init()
    x = input("The system is ready. Enter your text:")

    while x:
        if x[-1] != '#':
            x = readData.format_line(x)
            suggestions = readData.find_sequence(x)

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
