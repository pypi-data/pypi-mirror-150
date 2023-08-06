import random

def oneCardFunc():
    with open('cards.txt', 'r') as x:
        cards = [line.rstrip('\n') for line in x]

    return(random.choice(cards))
