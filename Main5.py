import os
import sys
import time
import pygame
from screens.loadingScreens.InitialLoadingScreen import InitialLoadingScreen
from screens.loadingScreens.NewLoadingScreen import NewLoadingScreen
from screens.InstructionsScreen import InstructionsScreen
from screens.FinalScreen import FinalScreen
from pygame.locals import *
from Constants import *
#from inputs import get_gamepad
#from XBoxController import *
from Player2 import *
from items.Sword import Sword
from Obstacle import *
from Overworld import *

pygame.init()

# Set up screen dimensions
screen_width, screen_height = 1500, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brown Zelda (But Not Garbage)")
pygame.mixer.init()
font = pygame.font.Font('freesansbold.ttf', 32)
current_screen = None


def init_loading_screen():
    #set screen to initial loading screen
    current_screen = InitialLoadingScreen(screen)
    loadingscreenstarttime = time.time()
    #load in title music
    pygame.mixer.music.load(os.path.join("Assets", "originalzeldatitlemusic.mp3"))  
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play()

    #initialize loading screen booleans - when each section of loading screen is complete will turn them to true
    gameLoop = True
    initialLoadingScreenDone = False
    newLoadingScreenDone = False
    instructionsScreenStarted = False
    firstSongSet = False
    secondSongSet = False
    thirdSongSet = False
    fourthSongSet = False
    while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            #when loading screen animation is complete - user can move onto story with space
            elif newLoadingScreenDone and not instructionsScreenStarted and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.set_volume(0.2)
                    loadingscreenstarttime = time.time()
                    instructionsScreenStarted = True

        #fades out of original zelda loading screen to new brown zelda loading screen - adds music
        if not initialLoadingScreenDone:
            #sets how long it has been since loading screen started
            elapsedTime = time.time() - loadingscreenstarttime
            if elapsedTime > 20:
                initialLoadingScreenDone = True
                current_screen = NewLoadingScreen(screen)
                loadingscreenstarttime = time.time()
                pygame.mixer.music.set_volume(0.7)
            elif elapsedTime > 18 and not thirdSongSet: 
                pygame.mixer.music.set_volume(0.55)
                thirdSongSet = True
            elif elapsedTime > 16 and not secondSongSet:
                #swap to chotta bheem music
                pygame.mixer.music.load(os.path.join("Assets", "chottabheemtitlesong.mp3"))  
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                secondSongSet = True
            elif elapsedTime > 13 and not fourthSongSet:
                pygame.mixer.music.set_volume(0.15)
                fourthSongSet = True
            elif elapsedTime > 10 and not firstSongSet:
                pygame.mixer.music.set_volume(0.3)
                firstSongSet = True
            elif elapsedTime > 4:
                current_screen.display(elapsedTime - 4)
            else:
                current_screen.display(0)
        elif not newLoadingScreenDone:
            elapsedTime = time.time() - loadingscreenstarttime
            if elapsedTime > 6:
                newLoadingScreenDone = True
            else:
                current_screen.display(elapsedTime)    
        elif instructionsScreenStarted:
            elapsedTime = time.time() - loadingscreenstarttime
            current_screen.displayfade(elapsedTime)
            if elapsedTime > 2:
                gameLoop = False         
        pygame.display.update()


def init_instructions_screen():
    #sets screen to instructions screen - also tracks time since screen started
    current_screen = InstructionsScreen(screen) 
    instructionsscreenstarttime = time.time()

    gameLoop = True
    while gameLoop:
        elapsedTime = time.time() - instructionsscreenstarttime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            #allows player to skip instructions screen if they wish by hitting space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    gameLoop = False

        #scrolls down instructions screen - tracking elapsed time to know how far down to scroll
        if elapsedTime > 72:
            pygame.mixer.music.stop()
            gameLoop = False
        elif elapsedTime > 68:
            current_screen.displayfade(elapsedTime - 68)
        elif elapsedTime > 65:
            pygame.mixer.music.set_volume(.1)
        else:
            current_screen.display(elapsedTime)
        pygame.display.update()
        
        
def init_home_screen():
    #creates clock to make fps consistent across machines
    clock = pygame.time.Clock()
    controller_detected=True
    sword = Sword()
    #loads in player and weapon
    player1 = Player2("bheem", {}, sword, 1, 1.2, 1, 5, 5, "str", 750, 400, 0)
    
    #test mode variable to skip slower parts of gameplay
    test_mode = True
    overworld = Overworld()
    curr_screen = overworld.cricketroom1
    curr_screen = overworld.room1
    if test_mode:
        curr_screen = overworld.cricketroom1
        overworld.cricketroom3.add_key(Key(overworld.cricketroom3, 800, 400, 800, 100))
    if curr_screen == overworld.schoolroom1:
        player1.player_rectangle.topleft = (750, 700)
        
    curr_screen_x_pos = 0
    curr_screen_y_pos = 0
    
    """
    try:
        joystick=XboxController()
    except:
        controller_detected=False
    # Establishing game loop to keep screen running
    """

    #adds gameloop variable and direction variable to keep track of player movement
    #also adds in text variables to keep track of text display
    gameLoop = True
    direction = None
    framecounter = 0
    firstchange = False
    display_text = True
    keep_text_displayed = True
    text_index = 0
    texts = []
    display_count = 0

    timestart = time.time()


    while gameLoop:
        #sets fps to 30 frames
        clock.tick(30)
        #tracks number of frames since game started for animation purposes
        framecounter = framecounter + 1
        overworld.obstacles_in_biome(player1, curr_screen)
        next_screen = overworld.picksupitems(player1, curr_screen, screen)
        if next_screen != None:
            curr_screen = next_screen
            keep_text_displayed = False
            text_index = 0
            texts = []
        #checks if player is in a room with a key and if they have picked it up - also unlocks rooms if player has key
        overworld.pickupkeys(player1, curr_screen)
        overworld.unlockroom(player1, curr_screen, screen)
        overworld.keydrop(player1, curr_screen)

        #renders page (items, players, background, monsters)
        curr_screen.render(curr_screen_x_pos, curr_screen_y_pos, player1, screen)
        
        #renders text if necessary
        if curr_screen.text != None and text_index < len(curr_screen.text) and display_text:
            new_text = overworld.display_text(curr_screen.text[text_index], curr_screen, player1, text_index, texts, screen)
            texts.append(new_text)
            keep_text_displayed = True
            display_text = False
        
        curr_screen.render_characters(player1, screen)
            
        if keep_text_displayed:
            display_count += 1
            for t in texts:
                screen.blit(t[0], t[1])
            if display_count == 1:
                display_count = 0
                text_index += 1 
                display_text = True
        
        #checks if player is going to next biome
        if curr_screen != None:
            new_screen = overworld.going_to_next_biome(player1, curr_screen, curr_screen_x_pos, curr_screen_y_pos, screen)
            if new_screen != None:
                keep_text_displayed = False
                text_index = 0
                texts = []
                curr_screen = new_screen
                curr_screen_x_pos = 0
                curr_screen_y_pos = 0
                
        if player1.check_checkpoint():
            screen_before_death = curr_screen
            curr_screen = overworld.game_over_screen
            player1.checkpoint = False
            respawn = True
            keep_text_displayed = False
            text_index = 0
            texts = []
            overworld.shah_rukh.paralyzing = False
                
        monsters_alive = overworld.monster_attack(curr_screen, player1, screen)[1]

        # player contorls
        """
        if controller_detected:        
            new_state=(joystick.get_x_axis(), joystick.get_y_axis())

            # player movement with x box controller

        if (new_state[0]<-1*Constants.controller_threshold):
            direction = "left"
            player1.current_frame = 10
        elif (new_state[0]>Constants.controller_threshold):
            direction = "right"
            player1.current_frame = 10
        if (new_state[1]<-1*Constants.controller_threshold):
            direction = "down"
            player1.current_frame = 11
        if (new_state[1]>controller_threshold):
            direction = "up"   
            player1.current_frame = 9
        if (joystick.X) and not sword.attacking:
            attacktime = time.time()
            sword.attack(curr_screen.monsters[0])
        """
 
        #controls movement - sets direction variable
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:                   
                if event.key == pygame.K_LEFT: 
                    direction = "left"
                    firstchange = True
                elif event.key == pygame.K_RIGHT: 
                    direction = "right"
                    firstchange = True
                elif event.key == pygame.K_UP: 
                    direction = "up"
                    firstchange = True
                elif event.key == pygame.K_DOWN: 
                    direction = "down"
                    firstchange = True
                elif event.key == pygame.K_k:
                    if respawn:
                        if screen_before_death.name[0:4] == "cric":
                            curr_screen = overworld.room1
                        elif screen_before_death.name[0:4] == "hous":
                            curr_screen = overworld.houseroom1
                        elif screen_before_death.name[0:4] == "gala":
                            curr_screen = overworld.galaroom1
                        else:
                            curr_screen = overworld.schoolroom1
                        keep_text_displayed = False
                        text_index = 0
                        player1.health_bar = 5
                        respawn = False
                        
            #stops movement if key is released - sets direction to None
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1.current_frame = 10
                    direction = None
                elif event.key == pygame.K_UP:
                    player1.current_frame = 11
                    direction = None
                elif event.key == pygame.K_DOWN:
                    player1.current_frame = 9
                    direction = None
                elif (event.key == pygame.K_SPACE) and not player1.attacking:
                    player1.attacking = True
                    player1.attackingtime = time.time()
                    player1.attack(curr_screen.monsters) 

            if event.type == pygame.QUIT:
                gameLoop=False
                pygame.quit()
                sys.exit()

        #handles monsters dropping keys to unlock dungeons
        overworld.monsterkeydrop(player1, curr_screen)
        #handles player movement and renders health
        player1.handlemove(direction, framecounter, firstchange)
        player1.renderhealth(10, 10, screen)
        firstchange = False
        
        pygame.display.update()

#final screen method - follows similar logic to instructions sceen
def init_final_screen():
    current_screen = FinalScreen(screen)
    finalscreenstarttime = time.time()

    pygame.mixer.music.load(os.path.join("Assets", "chottabheemtitlesong.mp3"))  
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    gameLoop = True
    while gameLoop:
        elapsedTime = time.time() - finalscreenstarttime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    gameLoop = False

        if elapsedTime > 59:
            pygame.mixer.music.stop()
            gameLoop = False
        elif elapsedTime > 55:
            current_screen.displayfade(elapsedTime - 55)
        else:
            current_screen.display(elapsedTime)
        pygame.display.update()
        
# init_loading_screen()
# init_instructions_screen()
init_home_screen()
# init_final_screen()