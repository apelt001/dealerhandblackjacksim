"""
A simulator for the card game Blackjack 

Goal is to reproduce the dealer bust rates given the upcard the dealer is showing (see for example http://www.edgevegas.com/blackjack-dealer-bust-rates/)
"""


import numpy as np
import pandas as pd

def value(hand):
    # Return the numerical value of a hand given the cards in the hand
	h = sorted(hand)
	if h[1] == 'A':
		if h[0] == 'A':
			return (12,'soft')
		else:
			return (int(h[0])+11,'soft')
	else:
		return (int(h[0])+int(h[1]), 'hard')



def finish(v,deck):
    # Finish dealing the dealer's cards. In this design, dealer hits on soft 17.
	if v[0]>17 and v[0]<=21:
		return v[0]
	elif v[0] > 21:
		return 'BUST'
	else:
		if v[1] == 'hard':
			if v[0] == 17:
				return v[0]
			else:
				d = deck.pop()
				if d == 'A':
					if v[0]+11 <= 21:
						v = (v[0]+11,'soft')
						return finish(v,deck)
					else:
						v=(v[0]+1,'hard')
						return finish(v,deck)
				else:
					v = (v[0]+int(d),'hard')
					return finish(v,deck)
		else:
			d = deck.pop()
			if d == 'A':
				v = (v[0]+1,'soft')
				return finish(v,deck)
			else:
				if v[0]+int(d) > 21:
					v = (v[0]+ int(d) - 10,'hard')
					return finish(v,deck)
				else:
					v = (v[0]+ int(d),'soft')
					return finish(v,deck)


def do(num_decks):
    # create a simulation of dealer hands with a distribution of cards based on the number of decks in the shoe
    shoe = [str(i) for i in range(2,10)]*(4*num_decks)+['10']*(16*num_decks)+['A']*(4*num_decks)
    # Shuffle the deck using a built in numpy random permutation function
    shoe = np.random.permutation(shoe).tolist()
    # Pick two cards
    hand = [shoe.pop(),shoe.pop()]
    upcard = hand[0]
    v = value(hand)
    return [finish(v,shoe),upcard]

# In this iteration, I reshuffle after every hand.
L=[]
num_decks=6
for n in range(100000):
    L.append(do(num_decks))



df = pd.DataFrame(L)
df.columns = ['final_value','dealer_upcard']
D=df.groupby('dealer_upcard')['final_value'].value_counts(normalize=True).sort_index()
order = ['2','3','4','5','6','7','8','9','10','A']
print(D.xs("BUST", level=1).loc[order])




















