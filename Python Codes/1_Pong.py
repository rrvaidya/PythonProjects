# Python Program for the Game - Pong

# Importing all the Dependencies
import simplegui
import random

# Initializing Globals - pos and vel encode vertical info for paddles
width = 600
height = 400       
ballRadius = 10
padWidth = 8
padHeight = 80
halfPadWidth = padWidth / 2
halfPadHeight = padHeight / 2
left = False
right = True
ballPosition = [width/2, height/2]
ballVelocity = [1, 1]
padLeftPosition = 200
padRightPosition = 200
padLeftVelocity = 0
padRightVelocity = 0
leftScore = 0
rightScore = 0
sI = 1


# Initialize ballPosition and ballVelocity for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ballPosition, ballVelocity
    ballPosition = [width/2, height/2]
    if direction == left:
        ballVelocity = [-1*random.randrange(2, 5), -1*random.randrange(2, 5)]
    elif direction == right:
        ballVelocity = [random.randrange(2, 5), -1*random.randrange(2, 5)]
        
        
# Define event handlers
def new_game():
    global padLeftPosition, padRightPosition, padLeftVelocity, padRightVelocity
    global leftScore, rightScore
    global sI
    sI = 1
    if left:
        spawn_ball(left)
    else:
        spawn_ball(right)

def draw(canvas):
    global leftScore, rightScore
    global padLeftPosition, padRightPosition, padLeftVelocity, padRightVelocity
    global ballPosition, ballVelocity
    global left, right
    global sI
        
    # Drawing midline, Left Gutter and Right gutter
    canvas.draw_line([width/2, 0],[width/2, height], 1, "White")
    canvas.draw_line([padWidth, 0],[padWidth, height], 1, "White")
    canvas.draw_line([width - padWidth, 0],[width - padWidth, height], 1, "White")
        
    # Update ball plus Collison and Reflection of Ball
    if (ballPosition[1] + ballVelocity[1] > ballRadius and ballPosition[1] + ballVelocity[1] < height - ballRadius):
        ballPosition[0] = ballPosition[0] + ballVelocity[0]
        ballPosition[1] = ballPosition[1] + ballVelocity[1]
        if (ballPosition[0] <= ballRadius + padWidth):
            if ((ballPosition[1] >= padLeftPosition - halfPadHeight) and (ballPosition[1] <= padLeftPosition + halfPadHeight)):
                sI = sI + (0.1*sI)
                ballVelocity[0] = -1*sI*ballVelocity[0]                
            else:
                rightScore = rightScore + 1
                left = False
                right = True
                new_game()
        elif (ballPosition[0] >= width - padWidth - ballRadius):
            if ((ballPosition[1] >= padRightPosition - halfPadHeight) and (ballPosition[1] <= padRightPosition + halfPadHeight)):
                sI = sI + (0.1*sI)
                ballVelocity[0] = -1*sI*ballVelocity[0]
            else:
                leftScore = leftScore + 1
                left = True
                right = False
                new_game()
    else:
        ballVelocity[1] = -1*ballVelocity[1]
        
            
    # Draw ball
    canvas.draw_circle(ballPosition, ballRadius, 1, "Red", "Red")
    
    # Update paddle's vertical position and Keeping paddle on the screen
    if (padLeftPosition + padLeftVelocity > halfPadHeight and padLeftPosition + padLeftVelocity < height - halfPadHeight):
        padLeftPosition = padLeftPosition + padLeftVelocity
        
    if (padRightPosition + padRightVelocity > halfPadHeight and padRightPosition + padRightVelocity < height - halfPadHeight):
        padRightPosition = padRightPosition + padRightVelocity
    
    # Draw Paddles - Left and Right
    canvas.draw_polygon([[0, padLeftPosition - halfPadHeight], [padWidth, padLeftPosition - halfPadHeight], [padWidth, padLeftPosition + halfPadHeight], [0, padLeftPosition + halfPadHeight]], 1, "White", "White")
    canvas.draw_polygon([[width - padWidth, padRightPosition - halfPadHeight], [width, padRightPosition - halfPadHeight], [width, padRightPosition + halfPadHeight], [width - padWidth, padRightPosition + halfPadHeight]], 1, "White", "White")
       
    # Draw scores
    canvas.draw_text(str(leftScore), [25, 45], 30, "Green", "sans-serif")
    canvas.draw_text(str(rightScore), [560, 45], 30, "Green", "sans-serif")
        
def keydown(key):
    global padLeftVelocity, padRightVelocity
    if key == simplegui.KEY_MAP["w"]:
        padLeftVelocity = -4*sI
    elif key == simplegui.KEY_MAP["s"]:
        padLeftVelocity = 4*sI
    elif key == simplegui.KEY_MAP["up"]:
        padRightVelocity = -4*sI
    elif key == simplegui.KEY_MAP["down"]:
        padRightVelocity = 4*sI

def keyup(key):
    global padLeftVelocity, padRightVelocity
    if key == simplegui.KEY_MAP["w"]:
        padLeftVelocity = 0
    elif key == simplegui.KEY_MAP["s"]:
        padLeftVelocity = 0
    elif key == simplegui.KEY_MAP["up"]:
        padRightVelocity = 0
    elif key == simplegui.KEY_MAP["down"]:
        padRightVelocity = 0
        
def button_handler():
    global leftScore, rightScore
    leftScore = 0
    rightScore = 0
    new_game()


# Create frame
frame = simplegui.create_frame("Pong Game", width, height)
restartButton = frame.add_button('Restart', button_handler, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# Start frame
new_game()
frame.start()