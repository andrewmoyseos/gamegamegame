import pygame
import sys
import random

#Initialize
pygame.init()

#Window settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch Game")


#Colors
WHITE = (255, 255, 255) #Background color
RED = (255, 0, 0) #Circle color


score = 0
lives = 5

pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 1
        self.pictures=[pygame.transform.scale(pygame.image.load('basket.goleft.jpeg'), (80, 60)), pygame.transform.scale(pygame.image.load('basket.jpeg'), (80, 60)), pygame.transform.scale(pygame.image.load('basket.goright.jpeg'), (80, 60))]
        self.image = self.pictures[self.index]
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height - 50))
        self.base_speed = 1  #Base speed
        self.current_speed = 0.5  #Current speed that starts at half speed
        self.move_update_counter = 0  #Counter to control movement updates

    def move(self, direction):
        self.move_update_counter += 1
        if self.move_update_counter >= (2 if self.current_speed == 0.5 else 1):  # Update movement based on speed
            if direction == "LEFT":
                self.index = 0
                self.image = self.pictures[self.index]
                self.rect.x -= self.base_speed
            elif direction == "RIGHT":
                self.index = 2
                self.image = self.pictures[self.index]
                self.rect.x += self.base_speed
            self.move_update_counter = 0

    def set_speed(self, speed):
        self.current_speed = speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.image = self.pictures[1]
#Player instance
player = Player()

#Circle class
class Circle:
    def __init__(self):
        self.radius = random.randint(10, 10)
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = self.radius
        self.update_counter = 0  #Counter to control fall updates

    def fall(self):
        self.update_counter += 1
        if self.update_counter >= 4:  #Move down every 4 frames
            self.y += 1  #Move down by 1 pixel
            self.update_counter = 0  #Reset counter

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.radius)

#Change difficulty
circle_generator = 1000 #Higher number = less circles on screen

#Player instance
player = Player()

#List of circles
circles = []


background = pygame.image.load('theskygame.jpeg').convert()

#Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            player.reset()

    #Background

    screen.blit(background, (0, 0))

    #Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: #Left arrow
        player.move("LEFT")
    if keys[pygame.K_RIGHT]: #Right arrow
        player.move("RIGHT")
    if keys[pygame.K_a]:  # 'A' key
        player.move("LEFT")
    if keys[pygame.K_d]:  # 'D' key
        player.move("RIGHT")

    if random.randint(0, circle_generator) == 0:
        circles.append(Circle())

        #Update circles and check for collisions and missed catches
    for circle in circles[:]:
        circle.fall()
        if circle.y - circle.radius > screen_height:  #Miss
            circles.remove(circle)
            lives -= 1  #Lost life
        elif player.rect.colliderect(
                (circle.x - circle.radius, circle.y - circle.radius, circle.radius * 2, circle.radius * 2)):
            #Collision detection
            circles.remove(circle)
            score += 1  #Add to score

    #Draw player
    player.draw(screen)

    #Draw circles
    for circle in circles:
        circle.draw(screen)

        #Draw the score
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    #Lives
    lives_text = font.render(f'Lives: {lives}', True, (0, 0, 0))
    screen.blit(lives_text, (screen_width - 120, 10))

    pygame.display.flip()

    #If no lives left, quit game
    if lives <= 0:
        running = False

pygame.quit()
sys.exit()
