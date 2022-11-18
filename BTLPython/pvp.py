import random
import pgzrun


WIDTH = 800
HEIGHT = 710
TRUE_HEIGHT = HEIGHT-50
SIZE_TANK = 25
walls=[]
bullets=[]
bullets_holdoff = 0
enemy_bullets=[]
game_over = 0
shields=[]
healths=[]

#setup back ground và tường
def setupWall():
    global background
    background = Actor("grass1")
    #map kích thước 16*10
    for x in range(16):
        for y in range(1,11):
            if random.randint(0,80) < 30:
                wall = Actor("wall1")
                wall.x = x*50 + SIZE_TANK+1 
                wall.y = y*50 + SIZE_TANK*3
                walls.append(wall)
            elif random.randint(0,80) > 30:
                wall = Actor("wall2")
                wall.x = x*50 + SIZE_TANK +1
                wall.y = y*50 + SIZE_TANK*3
                walls.append(wall)

setupWall()

#định dạng tank phe mình
tank = Actor("player")
tank.pos = (WIDTH-25, TRUE_HEIGHT - SIZE_TANK) #vị trí ban đầu
tank.angle = 0 #góc quay ban đầu
tank_health = 3 #máu 
tank_shield = False
#tank2 
enemy = Actor("player2")
enemy.pos = (25, SIZE_TANK*2+10)
enemy.angle = 0 #góc quay ban đầu
enemy_health = 3 #máu 
enemy_shield = False
      
def tank_set(): #setup về tank phe mình
    original_x = tank.x #cap nhật vị trí nguyên gốc của xe
    original_y = tank.y
    if keyboard.left:
        tank.x = tank.x - 3
        tank.angle = 180
    if keyboard.right:
        tank.x = tank.x + 3
        tank.angle = 0
    elif keyboard.up:
        tank.y = tank.y - 3
        tank.angle = 90
    elif keyboard.down:
        tank.y = tank.y + 3
        tank.angle = 270
#tránh va đối tượng va chạm vào vật cản
    if tank.collidelist(walls) != -1: 
        tank.x = original_x
        tank.y = original_y
#không cho tank ra khỏi màn hình
    if tank.x<SIZE_TANK or tank.x>(WIDTH - SIZE_TANK) or tank.y<SIZE_TANK or tank.y>(TRUE_HEIGHT - SIZE_TANK) or tank.y<60:
        tank.x = original_x
        tank.y = original_y
#setup về đạn tank phe mình        
def tank_bullets_set(): 
    global bullets_holdoff, enemy_health, enemy_shield, game_over
    if bullets_holdoff == 0:
        if keyboard.space:
            bullet = Actor("bulletblue1")
            bullet.angle = tank.angle #hướng tank hướng bullet
            if bullet.angle == 0:
                bullet.pos = (tank.x + SIZE_TANK, tank.y)
            if bullet.angle == 180:
                bullet.pos = (tank.x - SIZE_TANK, tank.y)
            if bullet.angle == 90:
                bullet.pos = (tank.x, tank.y - SIZE_TANK)
            if bullet.angle == 270:
                bullet.pos = (tank.x, tank.y + SIZE_TANK)
            bullets.append(bullet)    
            bullets_holdoff = 20
    else:
        bullets_holdoff = bullets_holdoff-1
#bắn đạn di chuyển
    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x = bullet.x + 6
        if bullet.angle == 180:
            bullet.x = bullet.x - 6
        if bullet.angle == 90:
            bullet.y = bullet.y - 6
        if bullet.angle == 270:
            bullet.y = bullet.y + 6
#setup đạn tiêu diệt mục tiêu   
    for bullet in bullets: 
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            sounds.gun9.play()
            #lấy vị trí vừa bị bắn
            wall = walls[walls_index]
            if random.randint(1,5) == 1: #random vật phẩm
                if random.randint(1,2) == 1:
                    heal=Actor("icon-heal")
                    heal.angle=0
                    heal.pos=wall.pos
                    healths.append(heal)
                else:
                    shield=Actor("icon-shield")
                    shield.angle=0
                    shield.pos=wall.pos
                    shields.append(shield)
            del walls[walls_index] #xoá vật cản
            bullets.remove(bullet) #sau khi bắn trúng thì xoá đạn
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<70 or bullet.y>TRUE_HEIGHT:
            bullets.remove(bullet)
        if bullet.colliderect(enemy):
            sounds.exp.play()
            if enemy_shield is False:
                enemy_health -= 1
                if enemy_health == 0:
                    game_over = 1
            else:
                enemy_shield = False
            bullets.remove(bullet)

#setup về tank phe địch       
def enemy_set(): 
    original_x = enemy.x #cap nhật vị trí nguyên gốc của xe
    original_y = enemy.y
    if keyboard.a:
        enemy.x = enemy.x - 3
        enemy.angle = 180
    if keyboard.d:
        enemy.x = enemy.x + 3
        enemy.angle = 0
    elif keyboard.w:
        enemy.y = enemy.y - 3
        enemy.angle = 90
    elif keyboard.s:
        enemy.y = enemy.y + 3
        enemy.angle = 270
#tránh va đối tượng va chạm vào vật cản
    if enemy.collidelist(walls) != -1: 
        enemy.x = original_x
        enemy.y = original_y
#không cho enemy ra khỏi màn hình
    if enemy.x<SIZE_TANK or enemy.x>(WIDTH - SIZE_TANK) or enemy.y<SIZE_TANK or enemy.y>(TRUE_HEIGHT - SIZE_TANK) or enemy.y<60:
        enemy.x = original_x
        enemy.y = original_y
#setup về đạn enemy 
def enemy_bullets_set(): #setup đạn tank phe địch
    global bullets_holdoff, tank_health, tank_shield, game_over
    if bullets_holdoff == 0:
        if keyboard.f:
            bullet = Actor("bulletred1")
            bullet.angle = enemy.angle #hướng tank hướng bullet
            if bullet.angle == 0:
                bullet.pos = (enemy.x + SIZE_TANK, enemy.y)
            if bullet.angle == 180:
                bullet.pos = (enemy.x - SIZE_TANK, enemy.y)
            if bullet.angle == 90:
                bullet.pos = (enemy.x, enemy.y - SIZE_TANK)
            if bullet.angle == 270:
                bullet.pos = (enemy.x, enemy.y + SIZE_TANK)
            enemy_bullets.append(bullet)    
            bullets_holdoff = 20
    else:
        bullets_holdoff = bullets_holdoff-1
#bắn đạn di chuyển
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x = bullet.x + 6
        if bullet.angle == 180:
            bullet.x = bullet.x - 6
        if bullet.angle == 90:
            bullet.y = bullet.y - 6
        if bullet.angle == 270:
            bullet.y = bullet.y + 6
#setup đạn tiêu diệt mục tiêu   
    for bullet in enemy_bullets: 
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            sounds.gun9.play()
            #lấy vị trí vừa bị bắn
            wall = walls[walls_index]
            if random.randint(1,5) == 1: #random vật phẩm
                if random.randint(1,2) == 1:
                    heal=Actor("icon-heal")
                    heal.angle=0
                    heal.pos=wall.pos
                    healths.append(heal)
                else:
                    shield=Actor("icon-shield")
                    shield.angle=0
                    shield.pos=wall.pos
                    shields.append(shield)
            del walls[walls_index] #xoá vật cản
            enemy_bullets.remove(bullet) #sau khi bắn trúng thì xoá đạn
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<70 or bullet.y>TRUE_HEIGHT:
            enemy_bullets.remove(bullet)
        if bullet.colliderect(tank):
            sounds.exp.play()
            if tank_shield is False:
                tank_health -= 1
                if tank_health == 0:
                    game_over = 2
            else:
                tank_shield = False
            enemy_bullets.remove(bullet)
def remove_tank_shield(): #setup về shield
    global tank_shield
    tank_shield = False
def remove_enemy_shield(): #setup về shield
    global enemy_shield
    enemy_shield = False

def bonus_set(): #setup ăn máu , khiên 
    global tank_shield, tank_health, enemy_health, enemy_shield
    for health in healths:
        if health.colliderect(tank):
            if tank_health != 3:
                tank_health += 1
            healths.remove(health)   
        if health.colliderect(enemy):
            if enemy_health != 3:
                enemy_health += 1
            healths.remove(health)
    for shield in shields:
        if shield.colliderect(tank):
            tank_shield = True
            shields.remove(shield)
        if shield.colliderect(enemy):
            enemy_shield = True
            shields.remove(shield)

def update():
    #chạy các hàm để chơi game 
    tank_set()
    tank_bullets_set()
    enemy_set()
    enemy_bullets_set()
    bonus_set()
    if tank_shield is True:
        clock.schedule(remove_tank_shield, 5.0)
    if enemy_shield is True:
        clock.schedule(remove_enemy_shield, 5.0)

def draw():
    screen.clear()
    #bấm tab để chơi lại 
    global tank_health,game_over,walls,shields,healths,bullets,tank_shield,walls1,enemy_shield, enemy_health, enemy_bullets
    if keyboard.tab: 
        game_over = 0
        tank.pos = (WIDTH-25, TRUE_HEIGHT - SIZE_TANK) #vị trí ban đầu
        enemy.pos = (25, SIZE_TANK*2+10)
        tank.angle = 90 #góc quay ban đầu
        tank_health = 3 #máu 
        enemy_health = 3 #máu
        enemy.angle = 0
        walls=[]
        walls1=[]  
        shields=[]
        healths=[]
        bullets=[]
        enemy_bullets=[]
        tank_shield= False
        enemy_shield= False
        setupWall()  
    #Vẽ khiên  
    if tank_shield is True:
        icon_shield=Actor("icon-shield")
        icon_shield.angle=0
        icon_shield.pos=(WIDTH-200,HEIGHT-20)
        icon_shield.draw()
    
    #setup người thắng 
    if game_over == 1:
        bg= Actor("win")
        bg.draw()
        screen.draw.text("PLAYER 1", (330,420), color=(227,157,97), fontsize=40)
    elif game_over == 2:
        bg= Actor("win")
        bg.draw()
        screen.draw.text("PLAYER 2", (330,420), color=(227,157,97), fontsize=40)
    else: 
        #setup hình nền, đạn, etc...
        background.draw()
        if tank_health == 3:
            health=Actor("blood3")
            health.angle=0
            health.pos=(WIDTH-85,HEIGHT-20)
        elif tank_health == 2:
            health=Actor("blood2")
            health.angle=0
            health.pos=(WIDTH-85,HEIGHT-20)
        else:
            health=Actor("blood1")
            health.angle=0
            health.pos=(WIDTH-85,HEIGHT-20)
        #máu enemy   
        if enemy_health == 3:
            health2=Actor("blood3")
            health2.angle=0
            health2.pos=(85,20)
        elif enemy_health == 2:
            health2=Actor("blood2")
            health2.angle=0
            health2.pos=(85,20)
        else:
            health2=Actor("blood1")
            health2.angle=0
            health2.pos=(85,20)
        health.draw()
        health2.draw()
        tank.draw()
        enemy.draw()
        for wall in walls:
            wall.draw()
        for shield in shields:
            shield.draw()
        for health in healths:
            health.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw()
        if enemy_shield is True: 
            icon_shield2=Actor("icon-shield")
            icon_shield2.angle=0
            icon_shield2.pos=(200,20)
            icon_shield2.draw()
        
pgzrun.go()