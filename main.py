import os

os.chdir('words')

def hacker(command, size = 20):
    letter, skipped_letters, length = 'a', '', 15

    c = command.split()

    try:
        letter = c[0]
    except:
        pass

    try:
        length = int(c[1])
    except IndexError:
        pass
    except:
        if c[1]:
            skipped_letters = c[1]

    try:
        length = int(c[2])
    except IndexError:
        pass
    except:
        if c[2]:
            skipped_letters = c[2]

    word_list = list(get_words(letter.lower(), skipped_letters.lower(), length))
    
    if not word_list:
        print('Nothing found')
    
    for word in list(word_list)[:size]:
        print(f'{len(word)}: {word}')


def get_words(letter, skipped, length):
    # Get list from json file with starting letter
    cur = eval(open(f'{letter[:1]}.json', 'r').read())

    # Sort words by length descendingly
    cur_sorted = sorted(cur, key = len)[::-1]

    # Filter words that may contain chars from skipped_letters
    # and <= given length
    end_letter = ''
    if len(letter) == 2:
        end_letter = letter[1]

    for word in cur_sorted:
        if len(word) <= length:
            if word.endswith(end_letter):
                if all(l not in word for l in skipped):
                    yield word

    # One-liner
    # return filter(lambda w: all(l not in w for l in skipped) and len(w) <= length and w[-1] == end_letter, cur_sorted)

def main():
    size = 20
    command = 'size 10'
    while True:
        command = input('\n>> ')
        c = command.split()
        if len(c) == 2 and c[0] == 'size':
            try:
                size = int(c[1])
                print(f'Size set to {size}')
                continue
            except:
                pass
        elif command == 'exit':
            print(f'Script Terminated')
            break
        elif not c:
            continue
        hacker(command, size)
        

if __name__ == '__main__':
    main()
