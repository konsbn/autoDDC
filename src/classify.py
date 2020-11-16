import os
from autoDDCv3 import wrapper
from tabulate import tabulate
def classify():
    os.system('clear')
    print('Enter the ISBN number to automatically classify the book.')

    while True:
        try:
            isbn = input('ISBN: ')
            data = wrapper(isbn)
            if data == f'No Entry for {isbn}':
                print(data)
                continue
            data = {i: [data[i]] for i in data.keys()}
            print()
            print(tabulate(data, headers='keys'))
            print()
        except KeyboardInterrupt:
            break
        except EOFError:
            print('\nPress Ctrl+C to exit')
            pass
    print('\nProgram Exited')
    return
    
if __name__ == '__main__':
    classify()
