import argparse
import sys

db_file_name = 'wordle_db.txt'
debug = True


def load_db():
    db = []
    #get file object
    f = open(db_file_name, "r")

    while(True):
        line = f.readline()
        #if line is empty, you are done with all lines in the file
        if not line:
            break
        #you can access the line
        db.append(line.strip())

    f.close
    return db

def process_args():
    global debug

    parser = argparse.ArgumentParser(description='Help with Wordle. Add pairs. Each pair: 5 letter string then 5 numbers. 0 = no match. 1 = match wrong position. 2 = match right position')
    parser.add_argument('inputs', metavar='N', nargs='+', help='')
    args = parser.parse_args()
    if debug: print(args.inputs)

    if ((len(args.inputs) % 2) == 1):
        print("Error: must specify inputs as pairs: a 5 letter words followed by 5 digits in range 0-2")
        sys.exit(1)
    
    u_pairs = []
    while len(args.inputs) > 0:
        # Get next 2 items
        u_word = args.inputs.pop(0)
        u_pos_info = args.inputs.pop(0)
        u_pairs.append((u_word, u_pos_info))

    return u_pairs

# use u_word and u_pos_info to remove impossible solutions from ok_words list
def remove_words(ok_words, u_word, u_pos_info):
    assert len(u_word) == len(u_pos_info)

    new_ok_words = []

    for word in ok_words:

        # print("Processing word {}".format(word))
        keep_word = True

        for index, letter in enumerate(u_word):
            pos_info = u_pos_info[index]
            # print ("Letter {} has pos_info {}".format(letter, pos_info))

            if pos_info == '0': # Letter must not be in word.
                if letter in word:
                    keep_word = False
                    break

            elif pos_info == '2': # Letter must be in word at position index.
                if not letter == word[index]:
                    keep_word = False
                    break 

            elif pos_info == '1': # Letter must be in word but not at position index.
                if not ((letter in word) and not (letter == word[index])):
                    keep_word = False
                    break 

            else:
                print("Error. position numbers must be 0,1, or 2")
                sys.exit(1)
    
        if keep_word: 
            new_ok_words.append(word)

    return new_ok_words

def get_all_found_letters(u_pairs):
    all_found = []
    for (u_word,u_pos_info) in u_pairs:
        for l in u_word:
            if not l in all_found:
                all_found.append(l)
    return all_found
    

# Find the best of the remaining words.
# A good candidate is one that eliminates lots of others.
# So try to find words that have letters in common with other possible words.
# but ignore the letters we have already tried.
def get_best_words(ok_words, all_found):
    best_word = ''
    best_score = 0
    for word in ok_words:
        score = 0
        for l in word:
            if l in all_found: 
                continue
            for w in ok_words:
                if w == word: 
                    continue
                if l in w: 
                    score = score + 1
        if score >= best_score:
            best_score = score
            best_word = word
    return best_word

# Get the Wordle dictionary (all legal words)
db = load_db()
if debug: print("Read {} words from {}.".format(len(db), db_file_name))

# Process user args. u_pairs is a list of tuples: (5 letter word, 5 digit number string)
u_pairs = process_args()
# New list of all words.
ok_words = db.copy()
for (u_word,u_pos_info) in u_pairs:

    ok_words = remove_words(ok_words, u_word, u_pos_info)

num_ok_words = len(ok_words)
print ("After processing {} and {} there are {} viable words remaining.".format(u_word, u_pos_info, num_ok_words))


all_found = get_all_found_letters(u_pairs)

suggestion = get_best_words(ok_words, all_found)

print("Suggested word is {}".format(suggestion))