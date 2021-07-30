from random import randint
import string

# Constructs the first number that it reads
# Returns the number along with an index to the next char
def read_num(text, i):
    j = i
    while j < len(text) and text[j].isdigit():
        j += 1
    num = int(text[i:j])
    return num, j

# Constructs the first word that it reads
# Returns the word along with an index to the next char
def read_word(text, i):
    j = i
    while j < len(text) and text[j].isalpha():
        j += 1
    word = text[i:j]
    
    if not i or text[i-2] in '.!':
        return word, j
    
    return word.lower(), j

# Returns the punctuation along with an index to the next char
def read_punc(text, i):
    return text[i], i + 1

# Returns the next word in the text starting from i
def get_next_word(text, i = 0):
    
    while i < len(text):
        
        while text[i].isspace():
            i += 1
            if i == len(text): return None, i

        if text[i].isdigit():
            num, i = read_num(text, i)
            # print(num)
            return num, i 

        elif text[i] in string.punctuation:
            punctuation, i = read_punc(text, i)
            # print(punctuation)
            return punctuation, i

        elif text[i].isalpha():
            word, i = read_word(text, i)
            # print(word)
            return word, i
        
        else:
            # print("Unexpected character in position: " + str(i))
            i += 1
    return None, i


def construct_dicts(text, states):
    
    # Get the first 'states' words
    textIndex = 0
    prevWord = ''
    prevWords = [None for i in range(states)]
    for i in range(states):
        prevWords[i], textIndex = get_next_word(text, textIndex)
    prevWord = ''.join(prevWords)

    # Dictionary to count how many times any word appears after a certain word
    followingWordCount = dict()

    # Dictionary to count how many times every word appears after a certain word
    countPairs = dict()

    # Read all the words and fill the dictionaries
    while textIndex < len(text):

        # Get the next word and update the index
        currWord, textIndex = get_next_word(text, textIndex)
        if currWord == None: break

        # If the previous word is not in the dictionaries
        if prevWord not in followingWordCount:

            # Initialize the value of the key with 1
            followingWordCount[prevWord] = 1

            # Initialize the key with a dict()
            countPairs[prevWord] = dict()
            # and initialize the value of key in the new dict with 1
            countPairs[prevWord][currWord] = 1

        else:
            # Inreace the word count by 1
            followingWordCount[prevWord] += 1

            # If the current word is not in the dictionary of the pairs
            if currWord not in countPairs[prevWord]:

                #Initialize it with 1
                countPairs[prevWord][currWord] = 1

            else:
                # Else increase the count by 1
                countPairs[prevWord][currWord] += 1
        
        if states:
            prevWords.pop(0)
            prevWords.append(currWord)
            prevWord = ' '.join(map(str, prevWords))
        else:
            prevWord = currWord
        
    return followingWordCount, countPairs


def generate_words(infile, states, words):
    
    # Read infile
    text = open(infile, 'r').read()
    
    # Construct the dictionaries
    followingWordCount, countPairs = construct_dicts(text, states)

    # Get the first word
    currWord = list(followingWordCount.keys())[randint(0, len(followingWordCount.keys()) - 1)]
    
    prevOut = ''
    for i in range(words):
    
        # Print the next word
        output = currWord.split()[0]
        if i and not output in string.punctuation:
            print(' ', end='')
        if prevOut == '' or prevOut in '.!':
            print(output[0].upper() + output[1:], end='')
        else:
            print(output, end = '')
        prevOut = output
        
        # Generate the next word
        if not states:
            currWord = list(followingWordCount.keys())[randint(0, len(followingWordCount.keys()) - 1)]
        else:
            newRand = randint(1, followingWordCount[str(currWord)])
            for word, count in countPairs[currWord].items():
                if newRand - count <= 0:
                    if states:
                        tempWord = currWord.split()[1:]
                        currWord = ' '.join(tempWord) + ' ' + word
                    else:
                        currWord = word
                    # print(":::" + currWord + ":::")
                    break
                else:
                    newRand -= count
                

def main():
    # Get infile name
    infile = input("Filename: ")
    # Get number of previous words to take into consideration
    # when generating a new word
    states = int(input("States: "))
    if states < 0:
        states = 0
    # Get number of words to generate
    words = int(input("Words: "))
    if states >= words:
        states = words - 1
    
    print()
    generate_words(infile, states, words)
    print()
    
main()