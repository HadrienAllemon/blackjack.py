""""Instance of a blackjack game"""

from time import sleep
import random
import functools


deck = functools.reduce(lambda a,b:a+b,[[i]*4 for i in range(2,11)]) + functools.reduce(lambda a,b:a+b,[[c]*4 for c in "VQK"]) + ["♠","♣","♦","♥"]
#deck = functools.reduce(lambda a,b:a+b,[[i]*4 for i in range(1,10)])+[10]*16



discard=[]
balance = 100
bet = 0
starting_screen="Welcome to this BlackJack game"

def getCard(value):
    if str(value)!="10":value=" "+str(value)
    return """
 _____ 
|     |
| {}  |
|_____|
    """.format(value).split("\n")

def getHand(hand):
    toZip=[]
    zipped=[]
    for card in hand:
        toZip.append(getCard(card))
    for i in range(6):
        zipped.append([val[i] for val in toZip])
    return "\n".join([" ".join(value) for value in zipped])

def loading_screen(string,i=0):
    print(string[i],end="")
    sleep(.1)
    if i != len(string)-1:
        loading_screen(string,i+1)

"""for x in range (len(starting_screen)+1):
    b = starting_screen[:x]
    print (b, end="\r")
    sleep(.05)"""

def score(hand):
    elevens = [11 if str(val) in "♠♣♦♥" else 10 if str(val) in "KQV" else val for val in hand]
    while sum(elevens) > 21 and 11 in elevens:
        index = elevens.index(11)
        elevens[index] = 1
    return sum(elevens)

def shuffle_and_deal(deck):
    if len(deck) < 4:
        global discard
        random.shuffle(discard)
        deck += discard
        discard = []
    shuffled_deck = [card for card in deck]
    random.shuffle(shuffled_deck)
    player_hand = [shuffled_deck[0],shuffled_deck[2]]
    cpu_hand = [shuffled_deck[1],shuffled_deck[3]]
    shuffled_deck = shuffled_deck[4:]
    return player_hand,cpu_hand,shuffled_deck

while True:
    player_hand,cpu_hand,deck = shuffle_and_deal(deck)

    while True:

        while not bet:
            if bet==0:
                print("""
                CPU Hand : 
                {}
                Your Hand : 
                {}
                
                """.format(getHand([cpu_hand[0],"?"]), getHand(player_hand), end="\r"))

            bet = input("How much do you wish to bet ? ( Minimum bet is 1, current funds : ${} )  ".format(balance))
            try:
                bet = int(bet)
            except:
                print("Please enter a number.")
                bet = ""
                continue
            if bet<=0 or bet>balance:
                print(["This exceeds your current funds ! ", "You can't bet 0 or below !"][bet<=0])
                bet=""
                continue
            balance -= bet



        print("""
        CPU Hand : 
        {}
        Your Hand : 
        {}
        
        your bet : {}
        """.format(getHand([cpu_hand[0],"?"]), getHand(player_hand),bet))

        ipt = input("Do you wish to call or save ? C/S \n").lower()
        if ipt not in "cs":
            print("This does not awnser my question !\n")
            continue

        if ipt == "c":
            player_hand.append(deck[0])
            deck=deck[1:]
            if score(player_hand)>21:
                for i in range(1,4):
                    print("BUSTED "+"."*i,end="\r")
                    sleep(.5)
                print("\n")
                break
            elif score(player_hand)==21:
                print("Twenty-one ! \n")
                break
            else:
                continue
        else:
            break

    if score(player_hand) <= 21:
        for i in range(1,4):
            print("CPU turn" + "."*i,end="\r")
            sleep(.5)
        while score(cpu_hand) < score(player_hand) and score(cpu_hand) < 21:
            print("""
            CPU Hand : 
            {}
            Your Hand : 
            {}
            """.format(getHand(cpu_hand), getHand(player_hand)))

            cpu_hand+=[deck[0]]
            deck=deck[1:]
            sleep(1)

        else:
            print("""
            CPU Hand : 
            {}
            Your Hand : 
            {}
            """.format(getHand(cpu_hand), getHand(player_hand)))

    if score(player_hand) > 21 or score(player_hand)<score(cpu_hand) <= 21:
        print("     You lost !\n")
        bet=0
        if balance==0:
            print("\n")
            for i in range(1,4):
                print("Unfortunately you went bankrupt :( "+"."*i,end="\r")
                sleep(.5)
            break

    elif score(player_hand) == score(cpu_hand):
        print("     This is a tie !\n")
        balance+=bet
        bet=0

    else:
        print("     You won !\n")
        balance+=bet+bet
        bet=0

    print(
"""    Final Hands :

        CPU Hand : {} 
    score = {}
    
        Your Hand : {} 
    score = {}
        """.format(getHand(cpu_hand), score(cpu_hand), getHand(player_hand), score(player_hand)))

    discard += player_hand + cpu_hand
    playagain = ""

    while not playagain:
        playagain = input("do you want to play again ? y/n").lower()
        if playagain not in "yn":
            print("please enter Y or N")
            playagain = ""

    if playagain == "y":
        continue
    else:
        break

print("\n\nThanks for playing ! \nFinal score: ${}\n".format(balance))









