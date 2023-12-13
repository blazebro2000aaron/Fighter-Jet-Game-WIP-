
import pygame,random,sys

pygame.init()
#Load images
PLAYER_JET_IMG = pygame.transform.scale(pygame.image.load("Fighter Jet Game/player jet.jpg"),(100,100))
ENEMY_JET_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Fighter Jet Game/enemy jet.jpg"),(100,100)),180)
PLAYER_BULLET_IMG = pygame.transform.scale(pygame.image.load("Fighter Jet Game/bullet.jpg"),(50,50))
ENEMY_BULLET_IMG = pygame.transform.rotate(PLAYER_BULLET_IMG,180)
CLOUD_IMG = pygame.transform.scale(pygame.image.load("Fighter Jet Game/cloud.jpg"),(200,200))
EXPLOSION = pygame.transform.scale(pygame.image.load("Fighter Jet Game/explosion.jpg"),(200,200))
#Load sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound("Fighter Jet Game/missile fire sound.mp3")
BULLET_FIRE_SOUND.set_volume(0.5)
EXPLOSION_SOUND = pygame.mixer.Sound("Fighter Jet Game/explosion sound.mp3")
BUTTON_CLICK_SOUND = pygame.mixer.Sound("Fighter Jet Game/button click.mp3")
BUTTON_CLICK_SOUND.set_volume(1000)
#Background Music
BACKGROUND_MUSIC = "Fighter Jet Game/background music.mp3"
pygame.mixer.music.set_volume(0.5)
#RGB color tuples
SKY_BLUE = (135, 206, 235)
#Player X and Y Limits
MAX_PLAYER_BULLETS = 3
MAX_PLAYER_X =  730
MIN_PLAYER_X =  -30
MAX_PLAYER_Y = 530
MIN_PLAYER_Y = 200
#Font
FONT = pygame.font.Font("Fighter Jet Game/Scorchedearth.otf",50)

#Define Classes
class game_object:
    def __init__(self,rect,alive,tick=0,last_x_dir=None,last_y_dir=None,x_vel=None,y_vel=None,max_x=730,min_x=-30,max_y=570,min_y=0):
        self.rect = rect
        self.alive = alive
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.last_x_dir = last_x_dir
        self.last_y_dir = last_y_dir
        self.tick = tick
        self.max_x=max_x
        self.min_x=min_x
        self.max_y=max_y
        self.min_y=min_y
    def up(self,vel):
        if self.rect.y > self.min_y:
            self.rect.y -= vel
        else:
            self.rect.y = self.min_y
    def down(self,vel):
        if self.rect.y < self.max_y:
            self.rect.y += vel
        else:
            self.rect.y = self.max_y
    def right(self,vel):
        if self.rect.x < self.max_x:
            self.rect.x += vel
        else:
            self.rect.x = self.max_x
    def left(self,vel):
        if self.rect.x > self.min_x:
            self.rect.x -= vel
        else:
            self.rect.x = self.min_x

class Game:
    def __init__(self):
        #Initialize
        pygame.init()
        #Define Surface Object
        self.WIN = pygame.display.set_mode((800,600),pygame.DOUBLEBUF)
        pygame.display.set_caption("Fighter Jet Game")
    
    def draw_window(self,player,enemy_jets,player_bullets,enemy_bullets,explosions,clouds):
        self.WIN.fill(SKY_BLUE)
        if self.player_jet.alive:
            self.WIN.blit(PLAYER_JET_IMG,(player.rect.x,player.rect.y))
        for bullet in player_bullets:
            self.WIN.blit(PLAYER_BULLET_IMG,(bullet.rect.x,bullet.rect.y))
        for enemy in enemy_jets:
            self.WIN.blit(ENEMY_JET_IMG,(enemy.rect.x,enemy.rect.y))
        for explosion in explosions:
            self.WIN.blit(EXPLOSION,(explosion.rect.x,explosion.rect.y))
        for bullet in enemy_bullets:
            self.WIN.blit(ENEMY_BULLET_IMG,(bullet.rect.x,bullet.rect.y))
        for cloud in clouds:
            self.WIN.blit(CLOUD_IMG,(cloud.x,cloud.y))
    def draw_text(self,num_of_bullet,lives,score):
        if self.player_jet.alive:
            SCORE_TEXT = FONT.render("Score "+str(score),1,(0,0,0)) 
            BULLETS_TEXT = pygame.transform.scale(FONT.render("Bullets "+str(num_of_bullet),1,(0,0,0)),(180,40))
            LIVES_TEXT = pygame.transform.scale(FONT.render("Lives "+str(lives),1,(0,0,0)),(150,40))
            self.WIN.blit(SCORE_TEXT,(0,0))
            self.WIN.blit(BULLETS_TEXT,(0,560))
            self.WIN.blit(LIVES_TEXT,(620,560))
        else:
            TITLE_TEXT = FONT.render("Explosive Flights",1,(0,0,0))
            self.WIN.blit(TITLE_TEXT,(100,100))
    def draw_buttons(self,quit_button,play_button):
        if self.quit_button_hover:
            QUIT_BUTTON_IMG = pygame.transform.scale(FONT.render("Quit", 1,(0,0,0),(200,0,0)),(180,70))
            self.WIN.blit(QUIT_BUTTON_IMG,(quit_button.rect.x-5,quit_button.rect.y-5))
        else:
            QUIT_BUTTON_IMG = pygame.transform.scale(FONT.render("Quit", 1,(0,0,0),(200,0,0)),(170,60))
            self.WIN.blit(QUIT_BUTTON_IMG,(quit_button.rect.x,quit_button.rect.y))
        if self.play_button_hover:
            START_RESUME_BUTTON_IMG = pygame.transform.scale(FONT.render("Play", 1,(0,0,0),(0,255,0)),(210,70))
            self.WIN.blit(START_RESUME_BUTTON_IMG,(play_button.rect.x-5,play_button.rect.y-5))
        else:
            START_RESUME_BUTTON_IMG = pygame.transform.scale(FONT.render("Play", 1,(0,0,0),(0,255,0)),(200,60))
            self.WIN.blit(START_RESUME_BUTTON_IMG,(play_button.rect.x,play_button.rect.y))
    def handle_movement(self,keys_pressed,player):
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            if player.x_vel < 9:
                player.last_x_dir = "RIGHT"
                player.x_vel += 1
            else:
                player.x_vel = 10
            player.right(player.x_vel)
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            if player.x_vel < 9:
                player.last_x_dir = "LEFT"
                player.x_vel += 1
            else:
                player.x_vel = 10
            player.left(player.x_vel)
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            if player.y_vel < 9:
                player.last_y_dir = "DOWN"
                player.y_vel += 1
            else:
                player.y_vel = 10
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            if player.y_vel < 9:
                player.last_y_dir = "UP"
                player.y_vel += 1
            else:
                player.y_vel = 10
        if player.x_vel > 0:
            player.x_vel -= 0.2
        if player.x_vel < 0:
            player.x_vel = 0
        if player.y_vel > 0:
            player.y_vel -= 0.2
        if player.y_vel < 0:
            player.y_vel = 0
        
        if player.last_x_dir == "LEFT":
            player.left(player.x_vel)
        elif player.last_x_dir == "RIGHT":
            player.right(player.x_vel)
        if player.last_y_dir == "UP":
            player.up(player.y_vel)
        elif player.last_y_dir == "DOWN":
            player.down(player.y_vel)

    def handle_bullets(self,player_bullets,enemy_bullets,enemy_jets,player,explosions):
        for player_bullet in player_bullets:
            if player_bullet.x_vel > 0:
                player_bullet.x_vel -= 0.1
            else:
                player_bullet.x_vel = 0
           
            if player_bullet.y_vel > 0:
                player_bullet.y_vel -= 1
            else:
                player_bullet.y_vel = 0
            player_bullet.rect.y -= player_bullet.y_vel
            if player_bullet.last_x_dir == "RIGHT":
                player_bullet.right(player_bullet.x_vel)
            else:
                player_bullet.left(player_bullet.x_vel)

            if player_bullet.rect.y < 10:
                player_bullets.remove(player_bullet)
            else:
                for enemy_jet in enemy_jets:
                    if enemy_jet.rect.colliderect(player_bullet.rect):
                        self.score += 1
                        explosion = game_object(pygame.Rect(enemy_jet.rect.x,enemy_jet.rect.y,150,160),True,0)
                        explosions.append(explosion)
                        if enemy_jet in enemy_jets and player_bullet in player_bullets:
                            enemy_jets.remove(enemy_jet)
                            player_bullets.remove(player_bullet)
                        EXPLOSION_SOUND.play()
            for enemy_bullet in enemy_bullets:
                if enemy_bullet.rect.colliderect(player_bullet):
                        if enemy_bullet in enemy_bullets and player_bullet in player_bullets:
                            enemy_bullets.remove(enemy_bullet)
                            player_bullets.remove(player_bullet)
                        explosion = game_object(pygame.Rect(enemy_jet.rect.x,enemy_jet.rect.y,150,160),True,0)
                        explosions.append(explosion) 
                        EXPLOSION_SOUND.play()
             
        
        # slow part
        
        for enemy_jet in enemy_jets:
            for enemy_bullet in enemy_bullets:
                if enemy_bullet.x_vel > 0:
                    enemy_bullet.x_vel -= 1
                else:
                    enemy_bullet.x_vel = 0
                if enemy_bullet.y_vel > 0:
                    enemy_bullet.y_vel -= 0.02
                else:
                    enemy_bullet.y_vel = 0
                enemy_bullet.rect.y += enemy_bullet.y_vel
                
                if enemy_bullet.last_x_dir == "RIGHT":
                    enemy_bullet.right(enemy_bullet.x_vel)
                else:
                    enemy_bullet.left(enemy_bullet.x_vel)
                
                if enemy_bullet.rect.y > 700:
                    enemy_bullets.remove(enemy_bullet)
                elif enemy_bullet.rect.colliderect(player.rect):
                    explosion = game_object(pygame.Rect(enemy_jet.rect.x,enemy_jet.rect.y,150,160),True,0)
                    explosions.append(explosion)
                    if enemy_bullet in enemy_bullets:
                        enemy_bullets.remove(enemy_bullet)
                    EXPLOSION_SOUND.play()
                    # if enemy bullet hits the player, it dies
                    self.player_lives -= 1


    def handle_enemys(self,enemy_jets,bullets):
        for enemy in enemy_jets:
            enemy.tick += 1
            if enemy.last_x_dir == "RIGHT" and enemy.rect.x <= enemy.max_x:
                enemy.rect.x += enemy.x_vel
            if enemy.last_x_dir == "LEFT" and enemy.rect.x >= enemy.min_x:
                enemy.rect.x -= enemy.x_vel
            if enemy.rect.x >= enemy.max_x:
                enemy.last_x_dir = "LEFT"
                enemy.rect.y += enemy.y_vel
            if enemy.rect.x <= enemy.min_x:
                enemy.last_x_dir = "RIGHT"
                enemy.rect.y += enemy.y_vel
            if (enemy.tick / random.randint(100,150)).is_integer():
                bullets.append(game_object(pygame.Rect(enemy.rect.x + 20,enemy.rect.y - 20,50,50),True,0,enemy.last_x_dir,enemy.last_y_dir,enemy.x_vel,5,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y))
            if enemy.rect.y > 570:
                self.player_lives = 0
    def handle_explosions(self,explosions,player):
        for explosion in explosions:
            explosion.tick += 1
            

            if explosion.rect.colliderect(player.rect):
                explosions.remove(explosion)
                pygame.time.delay(100)
                self.player_lives -= 1
            # reduce explosion time
            if explosion.tick == 20   and explosion in explosions: # and explosion in explosions:
                explosions.remove(explosion)
    def handle_buttons(self,cursor,quit_button,play_button):
        if cursor.colliderect(quit_button.rect):
            self.quit_button_hover = True
            if self.mousedown:
                BUTTON_CLICK_SOUND.play()
                sys.exit()
        if cursor.colliderect(play_button.rect):
            self.play_button_hover = True
            if self.mousedown:
                BUTTON_CLICK_SOUND.play()
                self.player_lives = 5
                self.player_jet.alive = True
    def handle_clouds(self,clouds):
        for cloud in clouds:
            cloud.y += 1
            if cloud.y > 600:
                clouds.remove(cloud)
    def main(self):
        self.score = 0
        self.player_jet = game_object(pygame.Rect(370,500,100,100),False,0,None,None,0,0,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y)
        self.enemy_jet = game_object(pygame.Rect(370,100,100,100),True,0,None,None,0,2)
        self.cloud_rect = pygame.Rect(370,300,100,50)
        self.clouds = []
        self.enemy_jets = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.fps = 30 # Lower it
        self.clock = pygame.time.Clock()
        self.enemy_spawn_timer = 0
        self.cloud_spawn_timer = 0
        self.min_spawn_speed = 5
        self.max_spawn_speed = 10
        self.last_key_pressed = None
        self.play_button = game_object(pygame.Rect(300,200,205,65),False)
        self.quit_button = game_object(pygame.Rect(325,400,175,35),False)
        self.mousedown = False
        self.player_lives = 0
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play()
        #Main Game loop
        while 1:
            self.clock.tick(self.fps)
            self.cursor = pygame.Rect((pygame.mouse.get_pos())[0],(pygame.mouse.get_pos())[1],20,20)
            self.play_button_hover = False
            self.quit_button_hover = False
            #Check Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.player_jet.alive:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and len(self.player_bullets) < MAX_PLAYER_BULLETS:
                            self.player_bullet = game_object(pygame.Rect(self.player_jet.rect.x + 20,self.player_jet.rect.y - 20,50,50),True,0,self.player_jet.last_x_dir,self.player_jet.last_y_dir,self.player_jet.x_vel,34,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y)
                            self.player_bullets.append(self.player_bullet)
                            print("Bullets ",len(self.player_bullets))
                            BULLET_FIRE_SOUND.play()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mousedown = True
                    else:
                        self.mousedown = False
            #Spawn Enemys
            if self.player_jet.alive:
                if self.enemy_spawn_timer >= 20 and len(self.enemy_jets) < 5:
                    self.enemy_spawn_timer = 0
                    self.enemy_jet = game_object(pygame.Rect(random.randint(-30,730),random.randint(20,100),100,100),True,0,"RIGHT",None,5,5,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MAX_PLAYER_X)
                    self.enemy_jets.append(self.enemy_jet)
                    self.enemy_spawn_timer = random.randint(self.min_spawn_speed,self.max_spawn_speed)
                if self.cloud_spawn_timer >= 100:
                    self.cloud_spawn_timer = 0
                    self.cloud_rect = pygame.Rect(random.randint(0,600),-30,100,50)
                    self.clouds.append(self.cloud_rect)
                self.handle_clouds(self.clouds)
                self.handle_movement(self.keys_pressed,self.player_jet)
                self.handle_bullets(self.player_bullets,self.enemy_bullets,self.enemy_jets,self.player_jet,self.explosions)
                self.handle_enemys(self.enemy_jets,self.enemy_bullets)
                self.handle_explosions(self.explosions,self.player_jet)

            self.keys_pressed = pygame.key.get_pressed()
            self.draw_window(self.player_jet,self.enemy_jets,self.player_bullets,self.enemy_bullets,self.explosions,self.clouds)
            if not self.player_jet.alive:
                self.player_lives = 5
                self.score = 0
                self.player_jet = game_object(pygame.Rect(370,500,100,100),False,0,None,None,0,0,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y)
                self.clouds = []
                self.player_bullets = []
                self.enemy_jets = []
                self.enemy_bullets = []
                self.explosions = []
                self.handle_buttons(self.cursor,self.quit_button,self.play_button)
                self.draw_buttons(self.quit_button,self.play_button)
            if self.player_lives == 0:
                self.draw_text(MAX_PLAYER_BULLETS-len(self.player_bullets),self.player_lives,self.score)
                pygame.display.update()
                pygame.time.delay(1000)
                self.player_jet.alive = False
            self.draw_text(MAX_PLAYER_BULLETS-len(self.player_bullets),self.player_lives,self.score)
            self.cloud_spawn_timer += 1
            self.enemy_spawn_timer += 1
            pygame.display.update()

Game().main()