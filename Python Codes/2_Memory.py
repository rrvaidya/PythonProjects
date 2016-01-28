# Card Game - Memory
# Importing required Modules
import simplegui
import random


# Defining helper functions for Initiating Globals
def new_game():
    global cards1, cards2, combinedCards
    global turns, state, exposed, clickLocation1, clickLocation2, clickLocation3
    
    cards1 = range(8)
    cards2 = range(8)
    combinedCards = cards1 + cards2
    random.shuffle(combinedCards)
    print(combinedCards)
    
    turns = 0
    state = 0
    exposed = [False]*16
    clickLocation1 = 0
    clickLocation2 = 0
    clickLocation3 = 0


# Defining Event Handlers
def mouseclick(pos):
    global combinedCards, turns, state, exposed
    global clickLocation1, clickLocation2, clickLocation3
    # Defining the Actual Logic of Game (Having 3 States)
    if state == 0:
        clickLocation1 = (pos[0]//100)
        if exposed[clickLocation1] == False:
            exposed[clickLocation1] = True
            state = 1
    elif state == 1:
        clickLocation2 = (pos[0]//100)
        if (clickLocation2 != clickLocation1) and (exposed[clickLocation2] != True):
            turns = turns + 1
            if exposed[clickLocation2] == False:
                exposed[clickLocation2] = True
                state = 2
    else:
        clickLocation3 = (pos[0]//100)
        if (clickLocation3 != clickLocation2) and (clickLocation3 != clickLocation1) and (exposed[clickLocation3] != True):
            if combinedCards[clickLocation1] != combinedCards[clickLocation2]:
                exposed[clickLocation3] = True
                exposed[clickLocation1] = False
                exposed[clickLocation2] = False
                clickLocation1 = clickLocation3
                state = 1
            else:
                exposed[clickLocation3] = True
                clickLocation1 = clickLocation3
                state = 1


# Drawing Cards Canvas having Resolution of  1600x200 Pixels 
def draw(canvas):
    global turns, cardsCombined, exposed    
    # Drawing the Deck of Cards and Game in Progress on Canvas (Order is Exposed Cards, Card Tet and Vertical Lines)
    for i in range(0, 16):
        if exposed[i] == True:
            canvas.draw_polygon([(100*i, 200), (100*i, 0), (100*(i+1), 0), (100*(i+1), 200)], 6, 'White','Black')
            canvas.draw_text(str(combinedCards[i]), [(i*100 + 37.5), 120], 60, 'White')
        canvas.draw_line((100*i, 200), (100*i, 0), 1, 'Black')
        label.set_text('Turns = %d' %turns)
        

# Creatig Frame (1600x1200) and Adding Buttons and Turns Label
frame = simplegui.create_frame('Memory', 1600, 200)
frame.set_canvas_background('Green')
frame.add_button('Reset', new_game)
label = frame.add_label('Turns = 0')


# Registering Event Handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


# Starting the Actual Game
new_game()
frame.start()