import pygame,random,sys
pygame.init()
#Load images
PLAYER_JET_IMG = pygame.transform.scale(pygame.image.load("Fighter Jet Game/player jet.jpg"),(100,100))
ENEMY_JET_IMG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Fighter Jet Game/enemy jet.jpg"),(100,100)),180)
PLAYER_BULLET_IMG = pygame.transform.scale(pygame.image.load("Fighter Jet Game/bullet.jpg"),(50,50))
ENEMY_BULLET_IMG = pygame.transform.rotate(PLAYER_BULLET_IMG,180)
EXPLOSION = pygame.transform.scale(pygame.image.load("Fighter Jet Game/explosion.jpg"),(200,200))
#Load sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound("Fighter Jet Game/missile fire sound.mp3")
BULLET_FIRE_SOUND.set_volume(0.5)
EXPLOSION_SOUND = pygame.mixer.Sound("Fighter Jet Game/explosion sound.mp3")
#Background Music
BACKGROUND_MUSIC = "Fighter Jet Game/background music.mp3"
#RGB color tuples
SKY_BLUE = (135, 206, 235)
#Player Limits
MAX_PLAYER_BULLETS = 3
MAX_PLAYER_X =  730
MIN_PLAYER_X =  -30
MAX_PLAYER_Y = 530
MIN_PLAYER_Y = 200
#Define Classes
class game_object:
    def __init__(self,rect,alive,life_span=None,last_x_dir=None,vel=None,max_x=None,min_x=None,max_y=None,min_y=None):
        self.rect = rect
        self.alive = alive
        self.vel = vel
        self.last_x_dir = last_x_dir
        self.life_Span = life_span
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
            self.rect.y = self.min_y
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
        self.WIN = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Fighter Jet Game")
    def draw_window(self,player,enemy_jets,player_bullets,explosions):
        self.WIN.fill(SKY_BLUE)
        self.WIN.blit(PLAYER_JET_IMG,(player.rect.x,player.rect.y))
        for bullet in player_bullets:
            self.WIN.blit(PLAYER_BULLET_IMG,(bullet.rect.x,bullet.rect.y))
        for enemy in enemy_jets:
            self.WIN.blit(ENEMY_JET_IMG,(enemy.x,enemy.y))
        for explosion in explosions:
            self.WIN.blit(EXPLOSION,(explosion.rect.x,explosion.rect.y))
    def handle_movement(self,keys_pressed,player):
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            if player.vel < 9:
                player.last_x_dir = "RIGHT"
                player.vel += 1
            else:
                player.vel = 10
            player.right(player.vel)
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            if player.vel < 9:
                player.last_x_dir = "LEFT"
                player.vel += 1
            else:
                player.vel = 10
            player.left(self.player_vel)
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            player.down(5)
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            player.up(5)
        if player.vel > 0:
            player.vel -= 0.2
        if player.vel < 0:
            player.vel = 0
        if player.last_x_dir == "LEFT":
            player.left(player.vel)
        elif player.last_x_dir == "RIGHT":
            player.right(player.vel)
    def handle_bullets(self,player_bullets,enemy_jets,explosions):
        for player_bullet in player_bullets:
            if player_bullet.vel > 0:
                player_bullet.vel -= 0.1
            else:
                player_bullet.vel = 0
            player_bullet.rect.y -= 5
            if player_bullet.last_x_dir == "RIGHT":
                player_bullet.right(player_bullet.vel)
            else:
                player_bullet.left(player_bullet.vel)
            if player_bullet.rect.y < 10:
                player_bullets.remove(player_bullet)
            else:
                for enemy_jet in enemy_jets:
                    if enemy_jet.colliderect(player_bullet.rect):
                        explosion = game_object(pygame.Rect(enemy_jet.x,enemy_jet.y,70,70),True,70)
                        explosions.append(explosion)
                        if enemy_jet in enemy_jets and player_bullet in player_bullets:
                            enemy_jets.remove(enemy_jet)
                            player_bullets.remove(player_bullet)
                        EXPLOSION_SOUND.play()
    def handle_enemys(self,enemy_jets,enemy_x_dir,player):
        for enemy in enemy_jets:
            if enemy.x > player.rect.x:
                enemy.x -= random.uniform(1,5)
            if enemy.x < player.rect.x:
                enemy.x += random.uniform(1,5)
            if enemy.y < MAX_PLAYER_Y:
                enemy.y += random.uniform(0,1)


    def main(self):
        self.player_jet = game_object(pygame.Rect(370,500,100,100),True,None,None,0,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y)
        self.enemy_jet = game_object(pygame.Rect(370,100,100,100),True,None,None,1)
        self.enemy_x_dir = "RIGHT"
        self.enemy_jets = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player_vel = 0
        self.timer = 0
        self.min_spawn_speed = 5
        self.max_spawn_speed = 10
        self.last_key_pressed = None
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play()
        #Main Game loop
        while self.player_jet.alive:
            self.clock.tick(self.fps)
            self.cursor = pygame.Rect((pygame.mouse.get_pos())[0],(pygame.mouse.get_pos())[1],20,20)
            print(self.player_jet.vel)
            #Check Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(self.player_bullets) < MAX_PLAYER_BULLETS:
                        self.player_bullet = game_object(pygame.Rect(self.player_jet.rect.x + 20,self.player_jet.rect.y - 20,50,50),True,None,self.player_jet.last_x_dir,self.player_jet.vel,MAX_PLAYER_X,MIN_PLAYER_X,MAX_PLAYER_Y,MIN_PLAYER_Y)
                        self.player_bullets.append(self.player_bullet)
                        BULLET_FIRE_SOUND.play()
            #Spawn Enemys
            if self.timer < 1 and len(self.enemy_jets) < 5:
                self.timer = 0
                self.enemy_jet.rect = pygame.Rect(random.randint(-30,730),random.randint(20,100),100,100)
                self.enemy_jets.append(self.enemy_jet.rect)
                self.timer = random.randint(self.min_spawn_speed,self.max_spawn_speed)
            self.keys_pressed = pygame.key.get_pressed()
            self.handle_movement(self.keys_pressed,self.player_jet)
            self.handle_bullets(self.player_bullets,self.enemy_jets,self.explosions)
            self.handle_enemys(self.enemy_jets,self.enemy_x_dir,self.player_jet)
            self.draw_window(self.player_jet,self.enemy_jets,self.player_bullets,self.explosions)
            self.timer -= 1
            pygame.display.update()
Game().main()