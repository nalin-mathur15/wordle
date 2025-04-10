import nltk
import numpy as np
from nltk.corpus import words

nltk.download('words')

wordList = [w.lower() for w in words.words() if len(w) == 5 and w.isalpha()]
wordList = list(set(wordList))

def filter(word_pool, guess, feedback):
    new_pool = []

    for word in word_pool:
        match = True
        used_indices = set()  # track matched positions to avoid double-matching on 'P'

        # First pass: check all 'R' (exact matches)
        for i in range(5):
            if feedback[i] == 'R':
                if word[i] != guess[i]:
                    match = False
                    break
                used_indices.add(i)

        if not match:
            continue

        # Second pass: check 'P' (wrong position but present)
        for i in range(5):
            if feedback[i] == 'P':
                if guess[i] == word[i] or guess[i] not in word:
                    match = False
                    break
                # try to find a different index to match it with
                found = False
                for j in range(5):
                    if j != i and word[j] == guess[i] and j not in used_indices and guess[j] != word[j]:
                        used_indices.add(j)
                        found = True
                        break
                if not found:
                    match = False
                    break

        if not match:
            continue

        # Third pass: check 'W' (not present at all)
        for i in range(5):
            if feedback[i] == 'W':
                # If a letter was marked 'W' but occurs in the guess multiple times,
                # and some of them were marked 'R' or 'P', we allow only those.
                letter = guess[i]
                total_marked = sum(1 for j in range(5) if guess[j] == letter and feedback[j] in ['R', 'P'])
                if word.count(letter) > total_marked:
                    match = False
                    break

        if match:
            new_pool.append(word)

    return new_pool


guess = 'adieu'
feedback = 'RWWPW'
pool = wordList.copy()
newpool = filter(pool, guess, feedback)
print(f"New Pool: {newpool}")