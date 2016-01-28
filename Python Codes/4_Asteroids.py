# Week 7,8 Project - Asteroids


#==========================================================================================================================
# Importing all the Modules
#==========================================================================================================================
import simplegui
import math
import random


#==========================================================================================================================
# Globals for UI
#==========================================================================================================================
widthHeight = [1200, 900]
score = 0
lives = 3
time = 0
friction = 0.01
started = False
explosion_group  = set([])



#==========================================================================================================================
# Defining the CLASSES associated with the Game
#==========================================================================================================================
# Defining the Class ImageInfo
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated    

# Defining the Class Sprite
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if self.animated == True:
            if self.age <= self.lifespan:
                expX = 64 + (self.age*128)
                canvas.draw_image(self.image, [expX, 64], self.image_size,  self.pos, self.image_size, self.angle)   
        else:
            canvas.draw_image(self.image, self.image_center,  self.image_size,  self.pos, self.image_size, self.angle)
    
    def update(self):
        self.age = self.age + 1
        if self.age <= self.lifespan:
            self.angle = self.angle + self.angle_vel
            for i in range(len(self.pos)):
                self.pos[i] = (self.pos[i] + self.vel[i])%widthHeight[i]
            return True
        else:
            return False
            
    def collide(self, other_object):
        collision = False
        other_object_pos = other_object.get_position()
        other_object_radius = other_object.get_radius()
        distance = dist(other_object_pos, self.pos)
        if distance < (self.radius + other_object_radius):
            collision = True
        return collision
            
# Defining the Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.missile = False
        self.missileDisp = False
        self.angle = angle
        self.angle_vel = (math.pi*0)/180
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust == False:
            self.image_center = [45, 45]
            canvas.draw_image(self.image, self.image_center,  self.image_size,  self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()            
        else:
            self.image_center = [45+90, 45]
            canvas.draw_image(self.image, self.image_center,  self.image_size,  self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()

    def update(self):
        self.angle = self.angle + self.angle_vel
        if self.thrust == True:
            thrust = angle_to_vector(self.angle)
            self.vel[0] = (1-friction)*self.vel[0] + 0.2*thrust[0]
            self.vel[1] = (1-friction)*self.vel[1] + 0.2*thrust[1]
        else:
            self.vel[0] = (1-friction)*self.vel[0]
            self.vel[1] = (1-friction)*self.vel[1]
        for i in range(len(self.pos)):
            self.pos[i] = (self.pos[i] + self.vel[i])%widthHeight[i]
            
    def shoot(self):
        self.missileDisp = True
        self.missile = True
        if self.missile == True:
            missileComponent = angle_to_vector(self.angle)
            missileVelX = self.vel[0] + 10*missileComponent[0]
            missileVelY = self.vel[1] + 10*missileComponent[1]
            noseX = self.pos[0] + self.radius*missileComponent[0]
            noseY = self.pos[1] + self.radius*missileComponent[1]
            missile = Sprite([noseX, noseY], [missileVelX, missileVelY], 0, 0, missile_image, missile_info, missile_sound)
            return missile

#==========================================================================================================================
# Defining the Art associted with the Game - Images
# Art assets created by Kim Lathrop, Special thanks to Kim Lathrop
#==========================================================================================================================
# DEFINING ALL THE IMAGES
# Debris Images
# List - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#        debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Nebula Images
# List - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# Splast image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image
ship_info = ImageInfo([45, 45], [90, 90], 45)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile images
# List - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images
# List - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Animated explosion images
# List - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")


#==========================================================================================================================
# Defining the Art associted with the Game - Sounds
# Sound assets purchased from sounddogs.com, PLEASE DO NOT REDISTRIBUTE
#==========================================================================================================================
# Defining Game Soundtrack
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(1.0)

# Defining Missile Launch sound
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(1.0)

# Defining Ship Thrust sound
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(1.0)

# Defining Explosion sound 
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


#==========================================================================================================================
# Defining the Helper functions to handle Transformations
#==========================================================================================================================
# Function to convert Angle to Vector
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# Distance calculation function
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Defining Canvas draw handler
def draw(canvas):
    global started, time, lives, score, rock_group, missile_group
    
    # Displaying Splash screen
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [widthHeight[0] / 2, widthHeight[1] / 2], splash_info.get_size())
    
    else:
        # Animiating background
        time += 1
        wtime = (time / 4) % widthHeight[0]
        center = debris_info.get_center()
        size = debris_info.get_size()
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [widthHeight[0] / 2, widthHeight[1] / 2], [widthHeight[0], widthHeight[1]])
        canvas.draw_image(debris_image, center, size, (wtime - widthHeight[0] / 2, widthHeight[1] / 2), (widthHeight[0], widthHeight[1]))
        canvas.draw_image(debris_image, center, size, (wtime + widthHeight[0] / 2, widthHeight[1] / 2), (widthHeight[0], widthHeight[1]))

        # Drawing Scores and Lives
        canvas.draw_text('Lives:%d' %lives, [30, 30], 30, 'White', 'monospace')
        canvas.draw_text('Score:%d' %score, [1000, 30], 30, 'White', 'monospace')

        # Drawing and Updating Ship
        my_ship.draw(canvas)
        my_ship.update()

        # Drawing and updating Sprite Objects (Rocks and Missile)
        process_sprite_group(rock_group, canvas)
        if my_ship.missileDisp == True:
            missile_group = process_sprite_group(missile_group, canvas)

        # Checking the Collison of Missile and Rock
        rocksBlast, missile_group, rock_group = group_group_collide(missile_group, rock_group)
        if rocksBlast > 0:
              score = score + (rocksBlast*10)
                
        # Drawing the explosion if there is Collision
        process_sprite_group(explosion_group, canvas)

        # Checking the Collison of Ship and Rock
        rock_group, shipRocksCollision = group_collide(rock_group, my_ship)
        if shipRocksCollision == True:
            lives = lives - 1
            if lives <=0:
                started = False
                rock_group = set([])
                lives = 3
                score = 0
                soundtrack.rewind()

# Defining Keydown handler
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel =  -(math.pi*2/180)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = (math.pi*2/180)
        
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        
    if key == simplegui.KEY_MAP['space']:
        a_missile = my_ship.shoot()
        missile_group.add(a_missile)
        
# Defining Keydown handler
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel =  0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel =  0
        
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        
    if key == simplegui.KEY_MAP['space']:
        my_ship.missile = False
        
# Defining Mouseclick handler
def click(gameStart):
    global started
    gameStart = True
    started = gameStart
    soundtrack.play()
    
            
# Defining Timer handler that spawns a rock    
def rock_spawner():
    global my_ship
    if started == True:
        rockPos = [random.randint(0,widthHeight[0]), random.randint(0,widthHeight[1])]
        rockVel = [random.choice([-3,-2,-1,1,2,3]), random.choice([-3,-2,-1,1,2,3])]
        rock_angle = (math.pi/180)*(random.randint(0,360))
        rock_angle_vel = (math.pi/180)*(random.choice([-3,-2,-1,1,2,3]))
        if len(rock_group) < 12:
            a_rock = Sprite(rockPos, rockVel, rock_angle, rock_angle_vel, asteroid_image, asteroid_info)
            rockShipDistance = dist(my_ship.get_position(), a_rock.get_position())
            if rockShipDistance > 50:
                rock_group.add(a_rock)
        
# Defining helper function for updating set of Rocks
def process_sprite_group(randomSet, canvas):
    randomSetCopy = set(randomSet)
    for object in randomSet:
        object.draw(canvas)
        killDecision = object.update()
        if killDecision == False:
            randomSetCopy.remove(object)
    randomSet = randomSetCopy
    return randomSet
        
# Defining helper function for Group Collide
def group_collide(group, other_object):
    global explosion_group
    group_collide = False
    objectCollision = False
    groupCopy = set(group)
    for object in group:
        objectCollision = object.collide(other_object)
        if objectCollision == True:
            explosion = Sprite(object.get_position(), [0,0], 0,  0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group_collide = True
            groupCopy.remove(object)
    group = groupCopy
    return group, group_collide

# Defining helper function for Group Group Collide
def group_group_collide(group1, group2):
    group_group_collide = False
    objectGroupCollision = False
    numberOfCollisions = 0
    group1Copy = set(group1)
    for object1 in group1:
        group2, objectGroupCollision = group_collide(group2, object1)
        if objectGroupCollision == True:
            numberOfCollisions = numberOfCollisions + 1
            group1Copy.remove(object1)
    group1 = group1Copy
    return numberOfCollisions, group1, group2
    

#==========================================================================================================================
# Initializing the Frame
#==========================================================================================================================
frame = simplegui.create_frame("Asteroids", widthHeight[0], widthHeight[1])
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)


#==========================================================================================================================
# Initializing the Ship, a Rock and a Missile
my_ship = Ship([widthHeight[0]/2, widthHeight[1]/2], [0, 0], (math.pi*0/180), ship_image, ship_info)
missile_group = set([])
rock_group = set([])   

#==========================================================================================================================
# Registering the Draw and Timer handlers
#==========================================================================================================================
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)


#==========================================================================================================================
# Starting the Game
#==========================================================================================================================
timer.start()
frame.start()