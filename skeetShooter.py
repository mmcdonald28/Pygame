# skeetShooter.py
# A game where you shoot at targets 
# Name: Matt McDonald
# Date: December Third

import pygame
from random import randint

# Initialize all that Pygame provides
pygame.init()
pygame.mixer.init() # Enables sound effects

# Global constants:
WIDTH     = 901
HEIGHT    = 600
NUM_PIGEONS = 30
PIGEON_SIZE = 40
FOLLOWER_SIZE = 15
WINNING_SCORE = 15

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Matt McDonald")


## CLASS DEFINITIONS ##

class Pigeon(pygame.sprite.Sprite):
    # A clay pigeon gets shot across the screen, if the mouse clicks on it it breaks
        
    def __init__(self, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("clayPigeon.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.image.get_at((1,1)) ) 
        self.rect.center = position  # position is an (x, y) pair
        (self.dx, self.dy) = speed   # speed is a (speedX, speedY) pair
        self.intact = True

    def update(self, screen):
        # This method controls movement of the pigeon object

        if self.intact :     # Only move if it's a not broken pigeon
            # .dx and .dy are going to move the pigeon either left or right
            # so it moves diagonally

            self.rect.left = self.rect.left + self.dx
            self.rect.top = self.rect.top + self.dy
        else:
            self.rect.top = self.rect.top + self.dy

    

            #### Add code here: Move the object.

    def shatter(self):

        self.image.fill((255,255,0))
        self.image = pygame.image.load("brokenPigeon.png")
        self.image.set_colorkey(self.image.get_at((1,1)) ) 


        self.dx = 0
        self.dy = 20
        self.intact = False
        #### Add code here: Stop the motion of the object, and
        ####  change the "self.alive" Boolean to be False.

##############################################################################

class Follower(pygame.sprite.Sprite):
    # Follows mouse around, if mouse is pressed on pigeon, the pigeon breaks     
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (FOLLOWER_SIZE ,FOLLOWER_SIZE ) )
        self.image.fill( (255,255,255) )
        self.image.set_colorkey( (255,255,255) ) # Make background transparent
        pygame.draw.line(self.image, (255,0,0), (FOLLOWER_SIZE / 2, 0), (FOLLOWER_SIZE / 2, FOLLOWER_SIZE), 1)
        pygame.draw.line(self.image, (255,0,0), (0, FOLLOWER_SIZE / 2), (FOLLOWER_SIZE, FOLLOWER_SIZE / 2), 1)

        self.rect = self.image.get_rect()
        
    def update(self, screen):

        self.rect.center = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        #### Add code here to have the position of the follower
        ####    follow the movement of the mouse.
    
##############################################################################
        
class Label(pygame.sprite.Sprite):
    # This class puts a message on the screen
    
    def __init__(self, textStr, center, fontType, fontSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontType, fontSize)
        self.text = textStr
        self.center = center
        self.textColor = textColor

    # self.update() - Render the text on the label.
    def update(self, screen):
        self.image = self.font.render(self.text, 1, self.textColor)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.center[0]
        self.rect.centery = self.center[1]

##############################################################################

def game():
    
    # Create the background Surface object
    background = pygame.Surface(screen.get_size())
    background = pygame.image.load("fieldBackground.jpg")
    screen.blit(background, (0, 0))
    
    # Create Sound objects

    gunshot = pygame.mixer.Sound("gunshot.wav")
    shatterSound = pygame.mixer.Sound("shatter.wav")

        
    # Create a follower object
    follower = Follower()
    
    #Make variables
    score = 0
    time = 30
    frames = 0
        
    # Create Label objects
    timeRemaining = Label("Time remaining: " + str(time), (WIDTH * .15, HEIGHT - 50), None, 30,(255,255,255))
    scoreCounter = Label("Score: " + str(score) , (WIDTH * .9, HEIGHT - 50), None, 30,(255,255,255))
            
    # Create sprite groups.
    # Every sprite must be in a group, but there can be more than one group.
    pigeonGroup = pygame.sprite.Group()# All pigeons will be added 
    brokenPigeonGroup = pygame.sprite.Group()# Will be broken pigeons
    otherSprites = pygame.sprite.Group(follower, timeRemaining, scoreCounter)
    
    keepGoing = True
    win = False
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        frames = frames + 1
        # Make one pigeon per second
        # define 30 clay pigeon objects, making it so they either start on the left
        # and travel right, or start on right & travel left
        # Move to loop so only one is released at a time
        if frames % 30 == 0 and time > 0:
            time = time - 1 # Sets time of game
            # Clay pigeon creator
            pigeonStartSide = randint(0,1)
            if pigeonStartSide == 0:
                pigeonX = 0 - (PIGEON_SIZE / 2)
                pigeonSpeed = (randint(10,25),randint(-5,-1))
            else:
                pigeonX = screen.get_width() + (PIGEON_SIZE / 2)
                pigeonSpeed = (randint(-25,-10),randint(-5,-1))
            pigeonY = randint(screen.get_height() * .25, screen.get_height() / 2)
            pigeonPos = (pigeonX,pigeonY)
            pigeon = Pigeon(pigeonPos,pigeonSpeed)
            pigeonGroup.add(pigeon)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # detect collison and add to group, inc / dec score & play shoot or break noise
                brokenList = pygame.sprite.spritecollide(follower, pigeonGroup, True)
                if len(brokenList) > 0:
                    for brokenPigeon in brokenList:
                            gunshot.play()
                            shatterSound.play()
                            brokenPigeon.shatter()
                            brokenPigeonGroup.add(brokenPigeon)
                            score = score + 1
                else:
                    #score = score - 1
                    gunshot.play()
                    

        timeRemaining.text = ("Time remaining: " + str(time))
        scoreCounter.text = ("Score: " + str(score))
                
        # detect win
        if (time == 0 and score >= WINNING_SCORE):
            win = True
            keepGoing = False
        elif time == 0:
            win = False
            keepGoing = False

        # Clear update draw
        pigeonGroup.clear(screen, background)
        brokenPigeonGroup.clear(screen, background)
        otherSprites.clear(screen, background)
        
        pigeonGroup.update(screen)
        brokenPigeonGroup.update(screen)
        otherSprites.update(screen)
        
        pigeonGroup.draw(screen)
        brokenPigeonGroup.draw(screen)
        otherSprites.draw(screen)
    
        pygame.display.flip()
       
    return (win,score,time)

##############################################################################

def titleScreen():
    
    background = pygame.Surface(screen.get_size()) # Construct a background
    background = pygame.image.load("range.jpg")
    screen.blit(background, (0,0))  # Blit background to screen only once.

    # Construct labels for a title and game instructions.  
    titleMsg = Label("Skeet Shooter!", (WIDTH / 2, HEIGHT * .10), None, 60, (0,0,0))
    startMsg = Label("Click to start", (WIDTH / 2, HEIGHT * .25), None, 30,(0,0,0))
    instructionsMsg1 = Label("Score " + str(WINNING_SCORE) + " points or more in 30 seconds to win", (WIDTH / 2, HEIGHT * .3), None, 30,(0,0,0))
    instructionsMsg2 = Label("Hitting a target gets you 1 point, while missing subtracts 1", (WIDTH / 2, HEIGHT * .35), None, 30,(0,0,0))


    # Add the labels to a group  
    labelGroup = pygame.sprite.Group(titleMsg, startMsg, instructionsMsg1, instructionsMsg2)

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:  
        clock.tick(30)  # Frame rate 30 frames per second.

        for event in pygame.event.get():      # Handle any events
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # Title screen ends
                keepGoing = False                      # when mouse clicked
            elif event.type == pygame.KEYDOWN:         # or any key pressed
                keepGoing = False
                                                       
        labelGroup.clear(screen, background)  # Update the display
        labelGroup.update(screen)
        labelGroup.draw(screen)
        
        pygame.display.flip()

##############################################################################

def playAgain(winLose,score,time,):
    
    background = pygame.Surface(screen.get_size()) # Construct a background
    background = background.convert()

    if winLose:
        fillColor = (110,255,100)
        labelText = "You Win!!!"
        labelColor = (128,0,0)
        label3Text = "You scored " + str(score) + " points in " + str(30 - time) + " seconds. Great job!"
    else:
        fillColor = (128,0,0)
        labelText = "You Lose..."
        labelColor = (110,255,100)
        label3Text = "You scored " + str(score) + " points in " + str(30 - time) + " seconds. Hit more targets to win"


    background.fill(fillColor)
    screen.blit(background, (0,0))

    shell = pygame.mixer.Sound("shellFalling.wav")
    
    # Construct Labels 
    label0 = Label(labelText, (WIDTH / 2, 100), None, 60, labelColor)
    label1 = Label("Play again?", (WIDTH / 2,200), None, 60, labelColor)
    label2 = Label("(Y/N)", (WIDTH / 2, 300), None, 60, labelColor)
    label3 = Label(label3Text, (WIDTH / 2, 400), None, 30, labelColor)
    labelGroup = pygame.sprite.Group( label0, label1, label2, label3)

    clock = pygame.time.Clock()
    keepGoing = True
    replay = False

    shell.play()

    while keepGoing:
    
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    replay = True
                    keepGoing = False
                elif event.key == pygame.K_n:
                    keepGoing = False

        labelGroup.clear(screen, background)
        labelGroup.update(screen)
        labelGroup.draw(screen)

        pygame.display.flip()
        
    return replay

##############################################################################

def endMessage():
    
    background = pygame.Surface(screen.get_size()) # Construct a background
    background = background.convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))   # Blit background to screen only once.

    # Construct a Label object to display the message and add it to a group.
    label1 = Label("Good Bye...", (WIDTH / 2,210), None, 60, (255,255,255))
    label2 = Label("Matt McDonald", (WIDTH / 2,320), None, 30, (255,255,255))
    label3 = Label("©2020", (WIDTH / 2,360), None, 30, (255,255,255))
    labelGroup = pygame.sprite.Group( label1, label2, label3 )

    clock = pygame.time.Clock()
    keepGoing = True
    frames = 0                  # 3 seconds will be 150 frames

    while keepGoing:
    
        clock.tick(30)          # Frame rate 30 frames per second.
        frames = frames + 1     # Count the number of frames displayed
        if frames == 90:        # After 5 seconds end the message display
            keepGoing = False 

        for event in pygame.event.get():    # Impatient people can quit earlier
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN or
                event.type == pygame.MOUSEBUTTONDOWN) :
                keepGoing = False

        labelGroup.clear(screen, background)
        labelGroup.update(screen)
        labelGroup.draw(screen)

        pygame.display.flip()

##############################################################################
        
def main():

    titleScreen()               # Display title and instructions.
    
    replay = True
    while replay :
        winLose = game()                      # Play the game.
        replay = playAgain(winLose[0], winLose[1],winLose[2])
        
    endMessage()     # Final "The End" Screen.

##############################################################################
            
# Run the program
main()
pygame.quit()
