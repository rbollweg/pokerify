#odds source: https://en.wikipedia.org/wiki/Poker_probability

def oddsOfWinning(hand)
#input: a list of cards forming a hand
#output: probibility of winining hand
	handType = getHandType(hand)
	
	oddsOfLose=0
	index = handType*1
	while index <= 9
		oddsOfLose += oddsOf(index)
		index+=1
	
	hand.sort()
	return 1 - (oddsOfLose+(14/hand[0].value+1))
	
def getHandType(hand)
#input: a list of cards forming a hand
#output: a numarical reprasentation of hand type
	hand.sort()
	if hand[0].value == 10 && hand[1].face == hand[2].face && hand[1].face == hand[3].face && hand[1].face == hand[4].face && hand[1].face == hand[0].face && hand[1].value == hand[2].value+1 && hand[2].value == hand[3].value+1 && hand[3].value == hand[4].value+1 && hand[1].value+1 == hand[0].value :#royal flush
		return 9
	elif hand[1].value == hand[2].value && hand[1].value == hand[3].value && hand[1].value == hand[4].value && hand[1].value == hand[0].value && hand[1].face == hand[2].face && hand[1].face == hand[3].face && hand[1].face == hand[4].face && hand[1].face == hand[0].face :#straight flush
		return 8
	elif (hand[0].value == hand[1].value && hand[0].value == hand[2].value && hand[0].value == hand[3].value) || hand[1].value == hand[2].value && hand[1].value == hand[3].value && hand[1].value == hand[4].value :#four of a kind
		return 7
	elif hand[0].value == hand[1].value && hand[0].value == hand[2].value && hand[0].value == hand[3].value && hand[3].value == hand[4].value :#full house
		return 6
	elif hand[1].face == hand[2].face && hand[1].face == hand[3].face && hand[1].face == hand[4].face && hand[1].face == hand[0].face :#flush
		return 5
	elif hand[1].value == hand[2].value+1 && hand[2].value == hand[3].value+1 && hand[3].value == hand[4].value+1 && hand[1].value+1 == hand[0].value :#straight
		return 4
	elif (hand[0].value == hand[1].value && hand[0].value == hand[2].value) || (hand[1].value == hand[2].value && hand[1].value == hand[3].value) || (hand[2].value == hand[3].value && hand[4].value == hand[2]) :#three of a kind
		return 3
	elif ((hand[0].value == hand[1].value && (hand[2].value == hand[3}.value) || hand[4].value == hand[3}.value) || (hand[2].value == hand[1].value && (hand[4].value == hand[3}.value) :#two pair
		return 2
	elif (hand[0].value == hand[1].value) || (hand[2].value == hand[1].value) || (hand[2].value == hand[3].value) || (hand[3].value == hand[4].value) :#one pair
		return 1
	else :#higher
		return 0

def oddsOf (handType)
#input: a numarical reprasentation of hand type
#output: the probiblity of getting the hand
	if handType==9 :
		return 0.0000154
	elif handType==8 :
		return 0.0000139
	elif handType==7 :
		return 0.00024
	elif handType==6 :
		return 0.001441
	elif handType==5 :
		return 0.001965
	elif handType==4 :
		return 0.003925
	elif handType==3 :
		return 0.021128
	elif handType==2 :
		return 0.047539
	elif handType==1 :
		return 0.422569
	else :
		return 0.50177
	