import pygame, random
from sys import exit

windowdimensions = (800, 400) # window size (currently)
bodydimensions = (150, 75) # ignore this
moveincrement = 3 # pixels the dog will move per frame
treeprev = True # ignore
treenum = 0 # ignore
movedir = 0 # direction the player is moving
dogbottomleft = 0
dogbottomright = 0
shiftindex = 0
parklimit = 5000
treelist = []
breedslist = ['Golden retriever', 'Dachshund', 'Border collie']

class NewTree(pygame.sprite.Sprite):
    def __init__(self, basepos):
        super().__init__()
        self.basepos = basepos
    def draw(self):
        global shiftindex
        if shiftindex - 125 < self.basepos < shiftindex + 925:
            self.treepos = (self.basepos - shiftindex, 300)
            self.tree = pygame.image.load('./Dog park simulator/tree pixelated test.png')
            self.rect = self.tree.get_rect(midbottom = (self.treepos[0] + 25, self.treepos[1]))
            screen.blit(self.tree, self.rect)

class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
#        colour = self.colour
#        height = self.height
#        breed = self.breed
#        sound = self.sound
        self.playerright = pygame.image.load('./Dog park simulator/Player/dog pixelated right.png').convert_alpha()
        self.playerleft = pygame.image.load('./Dog park simulator/Player/dog pixelated left.png').convert_alpha()
        self.player_rect = self.playerright.get_rect(midbottom = (400,325))
        self.poslist = []
        self.playerleft1 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk left 1.png')
        self.playerleft2 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk left 2.png')
        self.playerleft3 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk left 3.png')
        self.playerleft4 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk left 4.png')
        self.playerright1 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk right 1.png')
        self.playerright2 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk right 2.png')
        self.playerright3 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk right 3.png')
        self.playerright4 = pygame.image.load('./Dog park simulator/Player/dog pixelated walk right 4.png')
        self.walkleft = [self.playerleft1, self.playerleft2, self.playerleft3, self.playerleft4]
        self.walkright = [self.playerright1, self.playerright2, self.playerright3, self.playerright4]
        self.costume = 1
        self.animateindex = 0
    def blit(self):
        global movedir
        if movedir == 1:
            self.costume = 1
        elif movedir == -1:
            self.costume = -1
        if movedir == 0:
            self.animateindex = -1
        elif movedir != 0:
            if self.animateindex <= 3.8 and self.animateindex != -1:
                self.animateindex += 0.15
            else:
                self.animateindex = 0
        if movedir == 1:
            screen.blit(self.walkright[int(self.animateindex)], self.player_rect)
        elif movedir == -1:
            screen.blit(self.walkleft[int(self.animateindex)], self.player_rect)
        elif movedir == 0:
            if self.costume == 1:
                screen.blit(self.playerright, self.player_rect)
            elif self.costume == -1:
                screen.blit(self.playerleft, self.player_rect)
    def getpos(self):
        self.poslist.append(self.player_rect.bottomleft)
        self.poslist.append(self.player_rect.bottomright)
        self.poslist.append(self.player_rect.topleft)
        self.poslist.append(self.player_rect.topright)
        return self.poslist
    def movedog(self, x):
        global dogbottomleft, dogbottomright
        self.player_rect.x += x
        dogbottomleft += x
        dogbottomright += x

class NPCDog(pygame.sprite.Sprite):
    def __init__(self, basepos, dogtype):
        super().__init__()
        self.dogtype = dogtype
        self.basepos = basepos
        self.walking = False
        self.walktime = 0
        self.walkdir = 0
        self.walkdistance = 0
        self.walkspeed = 0
        self.animateindex = 0
        self.costume = 1
        self.blit = True
        self.walkcooldown = 0
        self.dogleft = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog left.png")
        self.dogleft1 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog left 1.png")
        self.dogleft2 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog left 2.png")
        self.dogleft3 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog left 3.png")
        self.dogleft4 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog left 4.png")
        self.dogright = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog right.png")
        self.dogright1 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog right 1.png")
        self.dogright2 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog right 2.png")
        self.dogright3 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog right 3.png")
        self.dogright4 = pygame.image.load(f"./Dog park simulator/{self.dogtype}/dog right 4.png")
        self.walkleft = [self.dogleft1, self.dogleft2, self.dogleft3, self.dogleft4]
        self.walkright = [self.dogright1, self.dogright2, self.dogright3, self.dogright4]
        self.dogrect = self.dogright.get_rect(midbottom = (basepos, 325))
            
    def interaction(self):
        if not random.randint(0, 15) and not self.walking and not self.walkcooldown:
            self.walking = True
            self.walkdir = random.randint(1, 2)
            if self.walkdir == 2:
                self.walkdir = -1
            self.walktime = random.randint(50, 150)
            self.walkdistance = random.randint(self.walktime, self.walktime*5)
            self.walkspeed = (self.walktime/(self.walkdistance))*self.walkdir*random.randint(4, 10)
        #print(self.walktime, self.walkdistance, self.walkspeed)
        elif self.walkcooldown:
            self.walkcooldown -= random.randint(1, 5)
    def walk(self):
        global parklimit
        if self.walking:
            if self.walkdistance >= 0:
                if self.basepos >= 200 and self.basepos <= parklimit - 200:
                    self.dogrect.x += self.walkspeed
                elif self.basepos < 200:
                    self.walking = False
                    self.basepos = 200
                elif self.basepos > parklimit - 200:
                    self.walking = False
                    self.basepos = parklimit - 200
                if self.walkdir == -1:
                    self.walkdistance += self.walkspeed
                    self.basepos += self.walkspeed
                else:
                    self.walkdistance -= self.walkspeed
                    self.basepos += self.walkspeed
                
            else:
                self.walking = False
                self.walkdir = 0
                self.walkdistance = 0
                self.walkspeed = 0
                self.walktime = 0
        else:
            self.walkdir = 0
            self.walkdistance = 0
            self.walkspeed = 0
            self.walktime = 0
    def draw(self):
        self.dogpos = (self.basepos - shiftindex, 325)
        self.dogrect = self.dogright.get_rect(midbottom = self.dogpos)
        self.blit = True
        if self.walking:
            if self.animateindex <= 3.8:
                self.animateindex += 0.15
            else:
                self.animateindex = 0
            if self.walkdir == 1:
                self.costume = 1
                if self.blit:
                    screen.blit(self.walkright[int(self.animateindex)], self.dogrect)
            if self.walkdir == -1:
                self.costume = -1
                if self.blit:
                    screen.blit(self.walkleft[int(self.animateindex)], self.dogrect)
        else:
            if self.costume == 1:
                if self.blit:
                    screen.blit(self.dogright, self.dogrect)
            elif self.costume == -1:
                if self.blit:
                    screen.blit(self.dogleft, self.dogrect)
                

pygame.init()
screen = pygame.display.set_mode(windowdimensions)
pygame.display.set_caption("dog simulator or something")
screen.fill('0xaaaaff')

ground_rect = pygame.Rect((0, windowdimensions[1] - 75), (windowdimensions[0], 75))
ground = pygame.draw.rect(screen, '0xaa8844', ground_rect, 0, 0)

grasslist = []
basex = 0
floor = windowdimensions[1]
##defaulty = windowdimensions[1] / 2 - bodydimensions[1] / 2
##if ground:
##    defaulty = 175
##dogpos = (windowdimensions[0] / 2 - bodydimensions[0] / 2, defaulty)
clock = pygame.time.Clock()
##dog_body_rect = pygame.Rect(dogpos, bodydimensions)
##dog_body = pygame.draw.rect(screen, 'White', dog_body_rect,0, 20)
treedimensions = (200, 175)

grass_rect = pygame.Rect((0, 300), (800,25))

trees = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Dog())
dogs = pygame.sprite.Group()
for dog in breedslist:
    dogpos = random.randint(400, parklimit-1500)
    dogs.add(NPCDog(dogpos, dog))
    print(f"{dog} added at {dogpos}.")

for i in range(50):
    treelist.append(random.randint(0, 1))
for i in range(50):
    if treelist[i]:
        tree = NewTree((i+1)*100)
        trees.add(tree)

while True:
##    dog_body = pygame.draw.rect(screen, '0xdddddd', dog_body_rect,0, 20)
##    dog_body_outline = pygame.draw.rect(screen, '0x777777', dog_body_rect, 3, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
##        if event.type == tree_timer:
##            if movedir == 1:
##                treenum = random.randint(1, 9)
##                if treeprev:
##                    treenum += 2
##                    treeprev = False
##                if treenum >= 8:
##                    trees.add(Tree())
##                    treeprev = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                movedir = 1
            if event.key == pygame.K_LEFT:
                movedir = -1
        if event.type == pygame.KEYUP:
            if pygame.key.get_pressed()[80] and pygame.key.get_pressed()[81]:
                movedir = 0
            elif pygame.key.get_pressed()[81] and shiftindex < parklimit:
                movedir = -1
            elif pygame.key.get_pressed()[80] and shiftindex > 0:
                movedir = 1
            else:
                movedir = 0
    if shiftindex < 0:
        movedir = 0
        shiftindex = 0
        for dog in player:
            dog.movedog(3)
        basex -= 3
    elif shiftindex > parklimit:
        movedir = 0
        shiftindex = parklimit
        for dog in player:
            dog.movedog(-3)
        basex += 3
    screen.fill('0xccccff')
    if not dogbottomleft:
        for dog in player:
            dogbottomleft = dog.getpos()[0][0]
            dogbottomright = dog.getpos()[1][0]

    for dog in player:
        dog.movedog(movedir*moveincrement)
    for i in range(22):
        x = basex + i*40
        x -= 40
        grassblade = pygame.image.load('./Dog park simulator/grass ground size8.png').convert_alpha()
        grassrect = grassblade.get_rect(topleft = (x, 320))
        screen.blit(grassblade, grassrect)

    if basex <= -40:
        basex = 0
    elif basex >= 40:
        basex = 0
    if dogbottomleft < 101 or dogbottomright > 699:
        if 0 <= shiftindex <= parklimit:    
            basex -= (moveincrement*movedir)
            shiftindex += moveincrement*movedir
    grass = pygame.draw.rect(screen, '0x83c883', grass_rect)
    for dog in player:    
        if dogbottomleft <= 100:
            dog.movedog(moveincrement)
        if dogbottomright >= 700:
            dog.movedog(moveincrement*-1)
    for tree in trees:
        tree.draw()
         
    for dog in dogs:
        dog.interaction()
        dog.walk()
        dog.draw()

    for dog in player:
        dog.blit()
    
    pygame.display.update()
    clock.tick(40)
