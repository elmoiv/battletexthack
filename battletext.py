import pyautogui as pg
import PIL.ImageGrab
import pynput
import random, os, time

listener = None
current_position = None
os.chdir('words')

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

def smart_randomizer(words:list, randomized=True):
    # Toggle between human like typing and auto-robot
    new_list = words[:10] + words[20:30]
    random.shuffle(new_list)
    if not randomized:
        new_list = words
    return new_list[5]

def on_click(x, y, button, pressed):
    global current_position
    # If mouse clicked store position and stop listener
    if pressed:
        current_position = (x, y)
        listener.stop()
        time.sleep(1)

def capture_click():
    global listener
    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()

def get_keyboard(f=1):
    keys = {}

    x, y = current_position
    
    keys['del'] = (x, y)
    for i in range(7):
        m = 69 * (i + 1) - sum(range(i + 1)) * 3.85
        m *= f
        keys['mnbvcxz'[i]] = (x - m, y)

    keys['l'] = (x, y - 80 * f)
    for i in range(8):
        m = 57 * (i + 1)
        m *= f
        keys['kjhgfdsa'[i]] = (x - m, y - 80 * f)

    keys['p'] = (x + 20 * f, y - 152 * f)
    for i in range(9):
        m = 55 * (i + 1)
        m *= f
        keys['oiuytrewq'[i]] = (x - m + 20 * f, y - 152 * f)
    
    keys['done'] = (x, y - 225 * f)
    
    return keys

def get_current_colors(keys):
    # return active green key
    # and disabled grey keys
    GRN, GRY = '', ''
    screen_colors = PIL.ImageGrab.grab().load()
    for key in keys:
        if key in ['del', 'done']:
            continue
        x, y = keys[key]
        rgb = screen_colors[x, y]
        if rgb == (133, 196, 59):
            GRN = key
        if rgb == (145, 146, 152):
            GRY += key
    return GRN, GRY

def auto_typer(keys, word, delay=0.09, human_like=False):
    # Using some randomness to simulate a human typing
    if human_like:
        time.sleep(random.randint(1, 3))
        for letter in word:
            pg.click(keys[letter])
            time.sleep(random.randint(1, 4) * delay)
    else:
        for letter in word:
            pg.click(keys[letter])
    
    pg.click(keys['done'])

def wait_other_player(keys):
    time.sleep(2)
    x, y = keys['done']
    while True:
        done_color = PIL.ImageGrab.grab().load()[x, y]
        if done_color == (133, 196, 59):
            return 0
        if done_color == (45, 48, 71):
            return 1
        time.sleep(1)

def main():
    isHuman = input('Enter 0 for Robot or 1 for Human: ')
    try:
        isHuman = int(isHuman)
        if not -1 < isHuman < 2:
            isHuman = 1
    except:
        isHuman = 1

    print('Click above backspace middle-point:\n')

    # Capture click on on-screen del button
    capture_click()
    print('- Captured Click')

    # Map the rest of the keys
    keys = get_keyboard()
    print('- Mapped Keys')
    
    rounds = 1
    while True:
        print(f'\n\nRound: {rounds}')

        # Get active letter and skipped ones from screen
        letter, skipped = get_current_colors(keys)
        print(f'\n- Active Letter: {letter}'
              f'\n- Skipped Letters: {skipped}\n')
        
        # Get corresponding words and shuffling them
        words = list(get_words(letter, skipped, 30))
        print(f'- Found {len(words)} words')
        
        # Auto-Type the word and click done
        word = smart_randomizer(words, randomized=isHuman)        # word = words[0]
        print(f'- Auto-typing word: {word}')
        auto_typer(keys, word, human_like=isHuman)

        # Wait for next round or win screen
        print('- Waiting for next round...')
        waiter = wait_other_player(keys)
        
        if waiter:
            print('- Opponent has been defeated XD')
            return
        
        rounds += 1

if __name__ == '__main__':
    main()
