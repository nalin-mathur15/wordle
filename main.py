import nltk
import numpy as np
from nltk.corpus import words

nltk.download('words')

wordList = [w.lower() for w in words.words() if len(w) == 5 and w.isalpha()]
wordList = list(set(wordList))

def filter(pool, guess, feedback):
    newPool = []
    for word in pool:
        match = True
        visitedIndices = set()
        
        for i in range(5):
            if feedback[i] == 'R':
                if word[i] != guess[i]:
                    match = False
                    break
                visitedIndices.add(i)
        
        if not match:
            continue
        
        for i in range(5):
            if feedback[i] == 'P':
                if guess[i] == word[i] or guess[i] not in word:
                    match = False
                    break
                found = False
                for j in range(5):
                    if (j != i) and (word[j] == guess[i]) and (j not in visitedIndices) and (guess[j] != word[j]):
                        visitedIndices.add(j)
                        found = True
                        break
                if not found:
                    match = False
                    break
        
        if not match:
            continue
        
        for i in range(5):
            if feedback[i] == 'W':
                letter = guess[i]
                totalMarked = sum(1 for j in range(5) if guess[j] == letter and feedback[j] in ['R', 'P'])
                if word.count(letter) > totalMarked:
                    match = False
                    break
                    
    if match:
        newPool.append(word)
    
    return newPool


def playWordle():
    print("Welcome to the Wordle Solver")

    pool = wordList.copy()
    guess = 'adieu'
    for attempt in range(1, 7):
        print(f"Program: {guess}")
        feedback = input("User: ").strip().upper()
        if feedback == 'RRRRR':
            print("Correct Word Guessed!")
            return None
        pool = filter(pool, guess, feedback)
        if not pool:
            print("No possible words remain. Please re-check your feedback inputs")
            return None
        
        letterFreq = np.zeros(26)
        for word in pool:
            for c in set(word):
                letterFreq[ord(c) - ord('a')] += 1
        
        def score(w):
            return sum(letterFreq[ord(c) - ord('a')] for c in set(w))
        
        guess = max(pool, key=score)
    print("Out of Attempts! Wordle Failed :(")
    
if __name__ == '__main__':
    playWordle()