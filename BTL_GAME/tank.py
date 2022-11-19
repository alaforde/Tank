#Khai báo thư viện
import random
import pygame
import pgzrun

#set up kích thước cửa sổ chơi (background)
WIDTH = 800
HEIGHT = 660
TRUE_HEIGHT = HEIGHT
SIZE_TANK = 25
walls=[]#mảng lưu vật cản trên map
bullets=[]#mảng lưu đạn
bullets_holdoff1 = 0 
bullets_holdoff = 0
enemy_move_count = 0
enemy_bullets=[]
game_over = False
enemies=[]#mảng lưu quái
shields=[]
healths=[]#mảng lưu máu
is_shield = False 
score=0


#setup tank phe mình
tank = Actor("player")
tank.pos = (WIDTH/2, TRUE_HEIGHT - SIZE_TANK) #vị trí ban đầu
tank.angle = 90 #góc quay ban đầu
tank_health = 3 #máu 

#setup quái trên map
def setupEnemy():
    for i in range(1,7):
        if i<5 :
            enemy = Actor("enemy_1")
        else:
            enemy = Actor("enemy_2")
        enemy.x = i*120
        enemy.y = SIZE_TANK+50
        enemy.angle = 90
        enemies.append(enemy)

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

#setup
setupEnemy()
setupWall()

#setup tank phe mình
def tank_set(): 
    original_x = tank.x #cap nhật vị trí nguyên gốc của xe
    original_y = tank.y
    if keyboard.left:
        tank.x = tank.x - 2 
        tank.angle = 180
    if keyboard.right:
        tank.x = tank.x + 2
        tank.angle = 0
    elif keyboard.up:
        tank.y = tank.y - 2
        tank.angle = 90
    elif keyboard.down:
        tank.y = tank.y + 2
        tank.angle = 270
    #khi đối tượng va chạm vào vật cản thì sẽ trả lại vị trí cũ
    if tank.collidelist(walls) != -1: 
        tank.x = original_x
        tank.y = original_y
    #không cho tank ra khỏi màn hình
    if tank.x<SIZE_TANK or tank.x>(WIDTH - SIZE_TANK) or tank.y<SIZE_TANK or tank.y>(TRUE_HEIGHT - SIZE_TANK) or tank.y<60:
        tank.x = original_x
        tank.y = original_y
    #khi va chạm vào quái sẽ game_over nếu không có khiên
    global game_over,is_shield
    if tank.collidelist(enemies)!= -1 and is_shield == False:
        game_over = True

#setup đạn tank phe mình        
def tank_bullets_set(): 
    global bullets_holdoff
    if bullets_holdoff == 0:
        if keyboard.space and not game_over:
                bullet = Actor("bulletblue1")
                #góc của đạn trùng góc của tank
                bullet.angle = tank.angle 
                #hướng tank hướng bullet 
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
        if walls_index != -1:#đã bắn trúng
            sounds.gun9.play()
            wall = walls[walls_index]

            #tạo hình ảnh nổ khi bắn trúng 
            # explosion = Actor("explosion4")
            # explosion.draw()

            if random.randint(1,3) == 1: #random vật phẩm
                if random.randint(1,2) == 1:
                    heal=Actor("icon-heal")
                    heal.angle=0
                    heal.pos=wall.pos
                    healths.append(heal)

                    enemy = Actor("enemy_2")
                    enemy.pos = wall.pos 
                    enemy.angle = 90 
                    enemies.append(enemy)
                else:
                    enemy = Actor("enemy_1")
                    enemy.pos = wall.pos 
                    enemy.angle = 90
                    enemies.append(enemy)

                    shield=Actor("icon-shield")
                    shield.angle=0 
                    shield.pos=wall.pos
                    shields.append(shield)       
            del walls[walls_index] #xoá vật cản
            bullets.remove(bullet) #sau đạn bắn trúng
        #xoá đạn khi ra khỏi map
        if bullet.x<0 or bullet.x>WIDTH or bullet.y<70 or bullet.y>TRUE_HEIGHT: #70 là size y của phần đen
            bullets.remove(bullet)
        enemy_index = bullet.collidelist(enemies)
        global score
        if enemy_index != -1 and bullets.count(bullet)!= 0:
            score +=1 
            sounds.exp.play()
            bullets.remove(bullet)
            del enemies[enemy_index]    
#setup quái        
def enemy_set(): 
    global enemy_move_count, bullets_holdoff1 
    for enemy in enemies:
        original_x=enemy.x
        original_y=enemy.y
        choice = random.randint(0,2)
        if enemy_move_count>0:
            enemy_move_count = enemy_move_count - 1
            if enemy.angle==0:
                enemy.x=enemy.x+2
            elif enemy.angle==180:
                enemy.x=enemy.x-2
            elif enemy.angle==90:
                enemy.y=enemy.y-2
            elif enemy.angle==270:
                enemy.y=enemy.y+2
            if enemy.x<SIZE_TANK or enemy.x>(WIDTH - SIZE_TANK) or enemy.y<SIZE_TANK or enemy.y>(TRUE_HEIGHT - SIZE_TANK) or enemy.y<70:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
            if enemy.collidelist(walls) != -1:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
        elif choice == 0: #quái di chuyển
            enemy_move_count = 10
        elif choice == 1: #quái đổi hướng
            enemy.angle = random.randint(0,3)*90
        else: #quái bắn
            if bullets_holdoff1 == 0:
                bullet=Actor("bulletred1")
                bullet.angle=enemy.angle
                bullet.pos=enemy.pos
                enemy_bullets.append(bullet)
                bullets_holdoff1 = 30
            else:
                bullets_holdoff1 = bullets_holdoff1 - 1

#setup đạn quái                 
def enemy_bullets_set(): 
    global enemies, game_over, tank_health, is_shield
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x = bullet.x + 5
        if bullet.angle == 180:
            bullet.x = bullet.x - 5
        if bullet.angle == 90:
            bullet.y = bullet.y - 5
        if bullet.angle == 270:
            bullet.y = bullet.y + 5
    #đạn quái phá tường,phá tank
        for bullet in enemy_bullets:
            wall_index=bullet.collidelist(walls)
            if wall_index != -1 and not game_over :
                sounds.gun10.play()
                wall = walls[wall_index]
                #vật phẩm or quái khác xuất hiện khi bắn vào tường
                if random.randint(1,5) == 1:
                    if random.randint(1,2) == 1:
                        heal=Actor("icon-heal")
                        heal.angle=0
                        heal.pos=wall.pos
                        healths.append(heal)

                        enemy = Actor("enemy_2")
                        enemy.pos = wall.pos
                        enemy.angle = 90
                        enemies.append(enemy)
                    else:
                        shield=Actor("icon-shield")
                        shield.angle=0
                        shield.pos=wall.pos
                        shields.append(shield)

                        enemy = Actor("enemy_1")
                        enemy.pos = wall.pos
                        enemy.angle = 90
                        enemies.append(enemy)
                del walls[wall_index] #xoá tường khi bị bắn
                enemy_bullets.remove(bullet) #xoá đạn khi bắn trúng
            if bullet.x<0 or bullet.x>WIDTH or bullet.y<70 or bullet.y>TRUE_HEIGHT:
                enemy_bullets.remove(bullet) 
            if bullet.colliderect(tank):
                if is_shield is False: #nếu khiên không còn 
                    tank_health -= 1
                    if tank_health == 0: #nếu hết máu thì thua
                        game_over = True
                else:
                    is_shield = False #nếu đạn bắn trúng tank thì sẽ mất khiên
                enemy_bullets.remove(bullet)

#xoá shield                
def remove_shield(): 
    global is_shield
    is_shield = False

#setup thêm đạn quái
def bonus_set(): 
    global is_shield, tank_health
    for health in healths:
        if health.colliderect(tank):
            if tank_health != 3:
                tank_health += 1
            healths.remove(health)
    for shield in shields:
        #nếu tank va chạm vào khiên thì khiên sẽ được bật và xoá khiên khỏi map
        if shield.colliderect(tank):
            is_shield = True
            shields.remove(shield)

def update():
    tank_set()
    tank_bullets_set()
    enemy_set()
    enemy_bullets_set()
    bonus_set()
    #khiên chỉ bật trong 5s
    if is_shield is True:
        clock.schedule(remove_shield, 5.0)
        
#vẽ ra màn hình
def draw():
    screen.clear()
    
    #bấm tab để chơi lại 
    global tank_health,game_over,walls,shields,healths,enemies,bullets,is_shield,walls1,score
    if keyboard.tab: 
        game_over = False
        tank.pos = (WIDTH/2, TRUE_HEIGHT - SIZE_TANK) #vị trí ban đầu
        tank.angle = 0 #góc quay ban đầu
        tank_health = 3 #máu 
        walls=[]
        walls1=[]  
        shields=[]
        healths=[]
        enemies=[]
        bullets=[]
        is_shield= False
        score=0
        setupWall()
        setupEnemy()
    # hiển thị màn hình thắng thua
    if game_over:
        bg= Actor("loss")
        bg.draw()
        screen.draw.text(str(score), (450,370), color=(227,157,97), fontsize=40)
        screen.draw.text("SCORE:", (340,370), color=(227,157,97), fontsize=40)
    elif len(enemies) == 0:
        bg= Actor("win")
        bg.draw()
        screen.draw.text(str(score), (440,430), color=(227,157,97), fontsize=40)
        screen.draw.text("SCORE:", (330,430), color=(227,157,97), fontsize=40)
    #hiển thị thanh máu 
    else: 
        background.draw()
        if tank_health == 3:
            health=Actor("blood3")
            health.angle=0
            health.pos=(90,20)
        elif tank_health == 2:
            health=Actor("blood2")
            health.angle=0
            health.pos=(90,20)
        else:
            health=Actor("blood1")
            health.angle=0
            health.pos=(90,20)
        health.draw()
        #hiển thị khiên nếu ăn khiên
        if is_shield is True:
            icon_shield=Actor("icon-shield")
            icon_shield.angle=0
            icon_shield.pos=(200,24)
            icon_shield.draw()
        tank.draw()
        for wall in walls:
            wall.draw()
        for shield in shields:
            shield.draw()
        for health in healths:
            health.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
        screen.draw.text(str(score), (360,7), color=(227,157,97), fontsize=40)
        screen.draw.text("SCORE:", (270,10), color=(227,157,97), fontsize=30)
pgzrun.go()