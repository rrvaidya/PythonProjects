# Mini-Project #6 - Blackjack

# Importing all the Required Modules
import simplegui
import random

# Defining the Parameters Associated with the Card and Card Back Matrix followed by Loading the Card Matrix
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png") 

# Initializing the Global Variables
in_play = False
standFlag = False
outcome = ' '
playerPrompt = ' '
score = 0

# Defining Globals for Card
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# Defining CARD class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0], pos[1]], CARD_SIZE)

        
# Defining HAND class
class Hand:
    def __init__(self):
    # Create HAND object
        self.hand = []

    def __str__(self):
    # Return a string representation of a HAND
        s = ' '
        for i in range(len(self.hand)):
            s = s + str(self.hand[i]) + ' '
        return s

    def add_card(self, card):
    # Add card to HAND
        self.card = card
        self.hand.append(card)

    def get_value(self):
    # Calculating HAND VALUE first using ACES as 1
        handValue = 0
        if len(self.hand) > 0:
            for i in range(len(self.hand)):
                dictEntry = str(self.hand[i])
                dictEntry = dictEntry[1]
                handValue = handValue + VALUES[dictEntry]
                if dictEntry == 'A':
                    aceFlag = True
                else:
                    aceFlag = False
        else:
            return handValue
    
    # Implementing CHECK for ACE in HAND
        if aceFlag == False:
            return handValue
        else:
            if handValue + 10 <= 21:
                return handValue + 10
            else:
                return handValue    
   
    def draw(self, canvas, pos):
    # Draw a hand on the canvas, use the draw method for cards        
        for i in range(len(self.hand)):
            handString = str(self.hand[i])
            xPos = handString[1]
            yPos = handString[0]
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(xPos), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(yPos))
            canvas.draw_image(card_images, card_loc, CARD_SIZE,
                              [(pos[0] + (i*100)), pos[1]], CARD_SIZE)
  

    
# Defining DECK class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                card = Card(SUITS[i], RANKS[j])
                self.deck.append(card)

    def shuffle(self):
        # Shuffle the Deck
        random.shuffle(self.deck)

    def deal_card(self):
    # Deal a CARD object from the DECK
        dealtCard = self.deck[0]
        self.deck.pop(0)
        return dealtCard
    
    def __str__(self):
        s = ' '
        for i in range(0, len(self.deck)):
            s = s + str(self.deck[i]) + ' '
        return s

    

# Defining Event Handlers for 3 Buttons - DEAL, HIT and STAND
def deal():
    global deck
    global playerHand, dealerHand
    global outcome, playerPrompt, in_play, score, standFlag
    outcome = ' '
    playerPrompt = 'Hit or Stand?'
    if in_play == False:    
        deck = Deck()
        deck.shuffle()
        playerHand = Hand()
        dealerHand = Hand()
        playerHand.add_card(deck.deal_card())
        playerHand.add_card(deck.deal_card())
        dealerHand.add_card(deck.deal_card())
        dealerHand.add_card(deck.deal_card())
        in_play = True
        standFlag = False
    else:
        outcome = 'Game Reset-You LOSE'
        print('You hit deal in between the hand-You lose...')
        in_play = False
        standFlag = False
        playerPrompt = 'New Deal?'
        score = score - 1
        

def hit():
    global outcome, playerPrompt, in_play, score, standFlag
    # If the HAND is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if in_play == True:
        playerHand.add_card(deck.deal_card())
        print(playerHand)
        if playerHand.get_value() > 21:
            print('You went beyond 21...')
            outcome = 'Busted-You LOSE'
            playerPrompt = 'New Deal?'
            in_play = False
            score = score - 1
    
       
def stand():
    global outcome, playerPrompt, in_play, score, standFlag
    # If hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # Assign a message to outcome, update in_play and score
    if in_play == True:
        standFlag = True
        if dealerHand.get_value() >= 17:
            if dealerHand.get_value() > playerHand.get_value():
                print('Dealer has better hand in 2 Cards')
                outcome = 'You LOSE'
                playerPrompt = 'New Deal?'
                score = score - 1
                in_play = False
            else:
                print('Dealer is more than or equal to 17 in 2 cards but less than you')
                outcome = 'You WIN'
                playerPrompt = 'New Deal?'
                score = score + 1
                in_play = False
        else:
            while (dealerHand.get_value() < 17):
                dealerHand.add_card(deck.deal_card())
                if dealerHand.get_value() > 21:
                    print('Dealer went beyond 21...')
                    outcome = 'Dealer Busted-You WIN'
                    playerPrompt = 'New Deal?'
                    score = score + 1
                    in_play = False
            if in_play == True:
                if (dealerHand.get_value() > playerHand.get_value()) and (dealerHand.get_value() <= 21):
                    print('Dealer beat you after hitting him...')
                    outcome = 'You LOSE'
                    playerPrompt = 'New Deal?'
                    score = score - 1
                    in_play = False
                elif dealerHand.get_value() == playerHand.get_value():
                    print('Tie...Dealer wins ties...')
                    outcome = 'TIE-You LOSE'
                    playerPrompt = 'New Deal?'
                    score = score - 1
                    in_play = False                
                else:
                    print('Dealer could not beat you after hitting him...')
                    outcome = 'You WIN'
                    playerPrompt = 'New Deal?'
                    score = score + 1
                    in_play = False
    print(dealerHand)


# Defining DRAW handler    
def draw(canvas):
    global outcome, playerPrompt, in_play, score
    # Test to make sure that card.draw works, replace with your code below    
    playerHand.draw(canvas, [60, 450])
    if standFlag == True:
        dealerHand.draw(canvas, [60, 225])
    else:
        canvas.draw_image(card_back, [CARD_CENTER[0], CARD_CENTER[1]], CARD_SIZE,
                          [60, 225], CARD_SIZE)
        secondCard = dealerHand.hand[1]
        secondCard.draw(canvas, [160, 225])
    canvas.draw_text('Blackjack', (30, 40), 40, 'White', 'monospace')
    canvas.draw_text('Score: %d' %score, (400, 40), 30, 'Black', 'monospace')
    canvas.draw_text('Dealer', (30, 150), 25, 'Black')
    canvas.draw_text(outcome, (400, 150), 25, 'Red', 'monospace')
    canvas.draw_text('Player', (30, 375), 25, 'Black')
    canvas.draw_text(playerPrompt, (400, 375), 25, 'Black')   


# Initializing FRAME
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")


# Creating BUTTONS and CANVAS callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# Starting the Actual GAME...
deal()
frame.start()