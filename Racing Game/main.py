import pygame
import sys
import time
import threading
import socket
from _thread import *
# -- PyGame Init --#
pygame.init()
win_width = 900
win_height = 550
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Racing Game")
# map = pygame.image.load("maps/map_1.png")
player = pygame.image.load("Car.png")
enemy=pygame.image.load("car2_red.png")
intro_bg = pygame.image.load("intro.png")
play_music = True
pygame.mixer.music.load("music/track0.wav")
#pygame.mixer.music.load("music/track1.mp3")
singleplayer = False
multiplayer = False
intro =False
self_banana=False
other_banana=False
banana_sent =False
drifting = False
game = False
mouse = pygame.mouse.get_pos()
data_in = "0%0$0* &"
data_out="0%0$0* &"
outcoming_packets=0
incoming_packets=0
pps=30
pps*=1.111
pps = int(1000/(pps+pps*7.3/30))
fps=0
letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","backspace","return","0","1","2","3","4","5","6","7","8","9","."]
"""
#-----ABOUT------#
THIS GAME WAS MADE BY EYAL ANGEL AT 2019 BETWEEN OCTOBER AND DECEMBER AND TOOK ABOUT 30 HOURS
THE GAME WAS MADE FROM SCRATCH AND IS YET MY BIGGEST PROJECT(FROM 2019 OCTOBER -2019 DECEMBER)
#-----ABOUT-------#
@@@@@@@@@@@@@@@@
#-----CREDITS-----#
SOME OF THE MUSIC - NITAYL SKILL
AHARON HAGEVER - GEVER
LETTERS - MATAN 
IMAGES - KENNY FROM "OPENGAMEART.ORG"
#-----CREDITS-----#
"""
# -- Colors --#
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
dark_green = (0, 200, 0)

if play_music:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()


class map():
    def __init__(self, path, x, y, map_height, map_width, cycles):
        self.x = x
        self.y = y
        self.path = path + ".png"
        self.load = pygame.image.load(self.path)
        self.map_wide, self.map_length = self.load.get_size()
        self.map_height = map_height
        self.map_width = map_width
        self.cycles = cycles


# -- maps --#
map_list = []
map_1 = map("maps/map_1", 0.2 * win_width, 0.5 * win_height, -700, -100, 5)
map_2 = map("maps/map_2", 0.5 * win_width, 0.5 * win_height, -100, -100, 5)
map_list = [map_1, map_2]


class text:
    def __init__(self, msg, color, x, y, size):
        self.font = pygame.font.SysFont(None, size)
        self.msg = msg
        self.color = color
        self.x = x
        self.y = y

    def display(self):
        self.text = self.font.render(self.msg, True, self.color)
        win.blit(self.text, (self.x, self.y))




class button():
    def __init__(self, msg, color, dark, x, y, height, width, img):
        self.color = color
        self.dark = dark
        self.msg = msg
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.img = img

    def on_but(self):
        if self.x + self.width >= mouse[0] >= self.x and self.y + self.height >= mouse[1] >= self.y:
            return True
        else:
            return False

    def display(self):
        if self.on_but() == True and self.img == "":
            pygame.draw.rect(win, (self.dark), (self.x, self.y, self.width, self.height))
        elif self.on_but() == True and self.img != "":
            path = "maps/mini/" + self.img + ".png"
            path = pygame.image.load(path)
            win.blit(path, (self.x, self.y))
        elif self.img == "":
            pygame.draw.rect(win, (white), (self.x - 5, self.y - 5, self.width + 10, self.height + 10))
            pygame.draw.rect(win, (self.color), (self.x, self.y, self.width, self.height))

        else:
            path = "maps/mini/" + self.img + ".png"
            path = pygame.image.load(path)
            win.blit(path, (self.x, self.y))
        if self.msg != "":
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.msg, 1, black)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

class entry:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.msg=""
        self.width =400
        self.height=10

    def display(self):
        pygame.draw.rect(win, (white), (self.x, self.y+60, self.width, self.height))
        if self.msg!="":
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.msg, 1, black)
            win.blit(text, (self.x , self.y))
    def back_space(self):
        old_m = self.msg
        self.msg=""
        for i in range(len(old_m)-1):
            self.msg+=old_m[i]
    def click(self, key):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE] or keys[pygame.K_DELETE]:
            self.msg = ""
            return ""
        for i in letters:
            if i ==key:
                return i
        return ""


# -- Intro Vars --#
status= ""
me=""
button1 = button("Train", green, white, 60, 350, 100, 250, "")
button2 = button("Play Online", green, white, 60, 200, 100, 250, "")
volume = button("Music: ON", green, white,win_width -200, 100,100,100, "")
map_buttons = []
button3 = button("", green, dark_green, 360, 350, 100, 200, "map_1")
button4 = button("", green, dark_green, 360, 450, 100, 200, "map_2")
map_buttons = [button3, button4]
text1 = text("Choose A  Map", black, 100, 200, 60)
text2 = text("Map A", black, 100, 350, 60)
text3 = text("Map B", black, 100, 450, 60)

text5= text("Enter Server IP:", black,100,150,40)
#--IP input--#
server_ip=entry(200,200)

#--name input--#
entry1=entry(200, 200)



#--- client---#
class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = ip
        if ip =="9060":
            self.server= "79.182.68.58"
        elif ip =="1234":
            self.server= "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self, data):
        try:
            self.client.sendto(str.encode(data), self.addr)
            return True
        except:
            return False

    def packet_loss_counter(self):
        global game, incoming_packets, outcoming_packets, packet_text
        while game:
            time.sleep(1)
            try:
                if incoming_packets >= outcoming_packets:
                    packet_text.msg="Packet Loss: " + str(100-outcoming_packets/incoming_packets*100) +"%"
                else:
                    packet_text.msg = "Packet Loss: 0%"
            except:
                packet_text.msg = "Packet Loss: 0%"
            incoming_packets=0
            outcoming_packets = 0

    def send(self):
        global game, packets_num, packets_ps, pps, outcoming_packets
        p = threading.Thread(target=self.packet_loss_counter)
        p.start()
        while game:
            global data_out
            try:
                self.client.sendto(str.encode(data_out), self.addr)
                outcoming_packets+=1
            except socket.error as e:
                print(e)
            pygame.time.delay(pps)
    def get(self):
        global game, incoming_packets
        while game:
            global data_in
            try:
                data, server = self.client.recvfrom(64)
                data_in=data.decode()
                incoming_packets+=1
            except:
                pass

"""
main main loop
"""
run = True

while run:

    """
    CLASSES
    """

    class check_point:
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height

        def location_x(self):
            return self.x + map_width

        def location_y(self):
            return self.y + map_height


    class car:
        def __init__(self, color, width, height):
            self.color = color
            self.width = width
            self.height = height
            self.vel = 0
            self.vel_y = 0
            self.vel_x = 0
            self.speed = 2.5
            self.col = 0.08
            self.wall_bounce = 0.5


    class wall:
        def __init__(self, x, y, width, height, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color

        def location_x(self):
            return self.x + map_width

        def location_y(self):
            return self.y + map_height


    class slower:
        def __init__(self, x, y, width, height, color, slowing_s):
            self.slowing_s = slowing_s
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color

        def location_x(self):
            return self.x + map_width

        def location_y(self):
            return self.y + map_height

    #-- sign in ---#
    while not intro:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                letter = entry1.click(pygame.key.name(event.key))
                if letter=="backspace" :
                    if len(entry1.msg)>0:
                        entry1.back_space()
                elif len(entry1.msg)<10 and letter!= "return" :
                    entry1.msg+=letter
                if letter =="return" and len(entry1.msg) >3:
                    intro =True


        win.fill(white)
        entry1.display()
        pygame.display.update()
    # -- intro --#
    text4=text(entry1.msg, black, 50, 0, 60)
    if play_music:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/track0.wav")
        pygame.mixer.music.play(-1)
    while intro:
        walls = []
        slowers = []
        check_points = []
        mouse = pygame.mouse.get_pos()
        pygame.time.delay(30)
        # -- Exit Button --#
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            singleplayer = False
            multiplayer = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(1)
            if multiplayer:
                if event.type == pygame.KEYDOWN:
                    letter=server_ip.click(pygame.key.name(event.key))
                    if letter == "backspace":
                        if len(server_ip.msg) > 0:
                            server_ip.back_space()
                    elif len(server_ip.msg) < 15 and letter != "return":
                        server_ip.msg += letter
                    if letter == "return" and len(server_ip.msg) > 3:
                        try:
                            me = Network(server_ip.msg)
                            if me.connect("0%0$0* &"):
                                intro =False
                        except:
                            pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.on_but():
                    singleplayer = True
                if button2.on_but():
                    multiplayer = True
                if volume.on_but():
                    if volume.msg=="Music: ON":
                        pygame.mixer.music.stop()
                        volume.msg="Music: OFF"
                        play_music=False
                    else:
                        volume.msg = "Music: ON"
                        pygame.mixer.music.load("music/track0.wav")
                        pygame.mixer.music.play(-1)
                        play_music=True
                if singleplayer:
                    for but in map_buttons:
                        if but.on_but():
                            map = map_list[map_buttons.index(but)]
                            intro = False
                            if map_buttons.index(but) == 0:
                                wallA = wall(550, 500, 600, 500, black)
                                slowerA = slower(400, 350, 800, 850, green, 1.8)
                                slowerB = slower(1200, 350, 225, 700, green, 1.8)
                                slowerC = slower(500, 1200, 630, 160, green, 1.8)
                                check_point2 = check_point(700, 0, 100, 500)
                                check_point3 = check_point(1150, 900, 850, 100)
                                check_point4 = check_point(900, 1000, 100, 1000)
                                check_point5 = check_point(180, 530, 400, 100)
                                walls = [wallA]
                                slowers = [slowerA, slowerB, slowerC]
                                check_points = [check_point2, check_point3, check_point4, check_point5]
                            else:
                                walls = []
                                slowers = []
                                check_points = []
                            checkP_num = 0
                            cycle = num = 0
        win.blit(intro_bg, (0, 0))
        if not singleplayer:
            if not multiplayer:
                button1.display()
                button2.display()
                volume.display()
                text4.display()
            else:
                ##--multiplayer--##
                text4.display()
                text5.display()
                server_ip.display()
        else:
            text1.display()
            text2.display()
            text3.display()

            button3.display()
            button4.display()
        pygame.display.update()

    # -- Vars --#
    if multiplayer:
        map =map_1
        p2_name= text("", red,0,0, 40 )
        wallA = wall(550, 500, 600, 500, black)
        slowerA = slower(400, 350, 800, 850, green, 1.8)
        slowerB = slower(1200, 350, 225, 700, green, 1.8)
        slowerC = slower(500, 1200, 630, 160, green, 1.8)
        check_point2 = check_point(700, 0, 100, 500)
        check_point3 = check_point(1150, 900, 850, 100)
        check_point4 = check_point(900, 1000, 100, 1000)
        check_point5 = check_point(180, 530, 400, 100)
        walls = [wallA]
        slowers = [slowerA, slowerB, slowerC]
        check_points = [check_point2, check_point3, check_point4, check_point5]
        checkP_num = 0
        cycle = num = 0
        packet_text = text("Packet Loss: ", black, 200, 20, 30)
    map_wide, map_length = map.load.get_size()
    map_height = map.map_height
    map_width = map.map_width
    player1 = car(green, 100, 100)
    rotate_r = False
    rotate_l = False
    crashed = False
    show_walls = False
    negative = False
    is_first = True

    rotation = 0
    dir_y = 100
    dir_x = 0
    angle = 5
    w, h = player.get_size()

    x = map.x
    y = map.y
    times = 0
    pos = (x, y)
    self_banana=False


    class banana:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.image = pygame.image.load("banana.png")
            self.show = True

        def on_banana(self):
            if self.x + 100 +map_width> x> self.x + map_width and self.y + 100 + map_height> y  > self.y+ map_height:
                return True
            else:
                return False

        def display(self):
            win.blit(self.image, (self.x + map_width, self.y + map_height))
        def life_time(self, t, type):
            global self_banana
            global other_banana
            if type:
                self_banana = True
            else:
                other_banana = True
            time.sleep(t)
            if type:
                self_banana = False
            else:
                other_banana = False


    banana2 = banana(10, 10)
    # -- Rotate Function --#
    def blitRotate(surf, image, pos, originPos, angle):
        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
        pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        # rotate and blit the image
        surf.blit(rotated_image, origin)


    def up_down():
        ret = ""
        if rotation > 270 or rotation < 90:
            ret = "UP"
        elif 90 < rotation < 270:
            ret = "DOWN"
        return (ret)


    def right_left():
        ret = ''
        if rotation > 180:
            ret = "RIGHT"
        elif rotation < 180:
            ret = "LEFT"
        return ret


    # -- Game Vars --#
    laps = text("laps:" + str(cycle) + "/" + str(map.cycles), black, 20, 20, 30)
    fps_text = text("fps: ", black, win_width-100, 20, 30)
    timer = text("0", black, 30, win_height - 50, 30)
    nameP = text(text4.msg, dark_green,y-50, x, 40)
    lost = text("", black, win_height*0.5, win_width*0.5, 100)
    game = True


    def timecounter():
        global fps
        sec = 0
        while game:
            time.sleep(1)
            sec += 1
            timer.msg = str(sec)
            fps_text.msg="fps: " + str(fps)
            fps=0

    def drift():
        global angle
        global drifting
        drifting =True
        angle*=2
        time.sleep(2)
        angle/=2
        drifting = False
    t = threading.Thread(target=timecounter)
    t.start()
    # -- MainLoop --#
    if play_music:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/track1.mp3")
        pygame.mixer.music.play(-1)
    if multiplayer and not singleplayer:
        get = threading.Thread(target=me.get)
        get.start()
        sender = threading.Thread(target=me.send)
        sender.start()
    while game:
        timedif = time.time()
        pygame.time.delay(30)
        # -- Exit Button --#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if multiplayer:
                    me.connect("disconnect")
                game = False
                run = False
                #sys.exit(0)

        # -- GUi --#
        keys = pygame.key.get_pressed()

        # -- Check Calculate Speed --#
        if player1.vel > 0:
            if player1.vel < 1:
                player1.vel = 0
            else:
                player1.vel -= player1.vel * player1.col


        elif player1.vel < 0:
            if player1.vel > -1:
                player1.vel = 0
            else:
                player1.vel -= player1.vel * player1.col


        if keys[pygame.K_SPACE] and not self_banana:
            banana1=banana(x-map_width,y - map_height)
            start_new_thread(banana1.life_time, (3, True))
        # -- Developer Keys --#
        if keys[pygame.K_EQUALS] and show_walls == False:
            show_walls = True
        elif keys[pygame.K_EQUALS] and show_walls == True:
            show_walls = False
        # -- Check If Gas is Pressed --#
        if keys[pygame.K_ESCAPE]:
            game = False
            intro = True
        if keys[pygame.K_UP]:
            player1.vel += player1.speed
            pygame.mixer.music.unpause()
        if keys[pygame.K_DOWN]:
            player1.vel -= player1.speed / 2
            pygame.mixer.music.unpause()
        if keys[pygame.K_RIGHT] and player1.vel > 5 or keys[pygame.K_RIGHT] and player1.vel < -5:

            if dir_y + angle <= 100 and dir_x < 0 and dir_y >= 0:
                dir_y += angle
                dir_x += angle

            elif dir_y - angle >= 0 and dir_x >= 0:
                dir_x += angle
                dir_y -= angle

            elif dir_x - angle >= 0:
                dir_y -= angle
                dir_x -= angle

            elif dir_y + angle <= 0:
                dir_y += angle
                dir_x -= angle
            rotate_r = True
        elif keys[pygame.K_LEFT] and player1.vel > 5 or keys[pygame.K_LEFT] and player1.vel < -5:
            if dir_y - angle >= 0 and dir_x <= 0 and dir_y > 0:
                dir_y -= angle
                dir_x -= angle

            elif dir_x + angle <= 0:
                dir_y -= angle
                dir_x += angle

            elif dir_y + angle <= 0:
                dir_y += angle
                dir_x += angle

            elif dir_y + angle <= 100 and dir_x >= 0:
                dir_x -= angle
                dir_y += angle
            rotate_l = True

        player1.vel_x = player1.vel * dir_x / 100
        player1.vel_y = player1.vel * dir_y / 100
        # -- Check What Animation To Do --#

        for slower in slowers:
            if slower.location_x() + slower.width >= x + 0.5 * player1.width >= slower.location_x() and slower.location_y() + slower.height >= y + 0.5 * player1.height >= slower.location_y():
                if up_down() == "UP" and player1.vel_y > 0 or up_down() == "DOWN" and player1.vel_y < 0 or right_left() == "RIGHT" and player1.vel_x > 0 or right_left() == "LEFT" and player1.vel_x < 0:
                    player1.vel -= slower.slowing_s * player1.vel * player1.col

        for wall in walls:
            if not crashed:
                if player1.vel_x > 0 and x + player1.vel_x + 0.5 * player1.width > wall.location_x() and wall.location_y() + wall.height > y + player1.height * 0.5 > wall.location_y() and x + 0.5 * player1.width <= wall.location_x():
                    if player1.vel_x > 5:
                        player1.vel_x /= -player1.wall_bounce
                        player1.vel /= -player1.wall_bounce
                    else:
                        player1.vel_x = 0
                    crashed = True
                elif player1.vel_x < 0 and x + player1.vel_x + player1.width * 0.5 < wall.location_x() + wall.width and wall.location_y() + wall.height > y + player1.height * 0.5 > wall.location_y() and x + 0.5 * player1.width >= wall.location_x() + wall.width:
                    if player1.vel_x < -5:
                        player1.vel_x /= -player1.wall_bounce
                        player1.vel /= -player1.wall_bounce
                    else:
                        player1.vel_x = 0

                    crashed = True
                elif player1.vel_y > 0 and y - player1.vel_y + player1.height * 0.5 < wall.location_y() + wall.height and wall.location_x() + wall.width > x + player1.width * 0.5 > wall.location_x() and y + player1.height * 0.5 >= wall.location_y():
                    if player1.vel_y > 5:
                        player1.vel_y /= -player1.wall_bounce
                        player1.vel /= -player1.wall_bounce
                    else:
                        player1.vel_y = 0
                    crashed = True
                elif player1.vel_y < 0 and y - player1.vel_y + player1.height * 0.5 > wall.location_y() and wall.location_x() + wall.width > x + player1.width * 0.5 > wall.location_x() and y + 0.5 * player1.height <= wall.location_y():
                    if player1.vel_y < -5:
                        player1.vel_y /= -player1.wall_bounce
                        player1.vel /= -player1.wall_bounce
                    else:
                        player1.vel_y = 0
                    crashed = True

        if player1.vel_y > 0:
            if map_height == -map_length + win_height and y - player1.vel_y >= 0.5 * win_height:
                y -= player1.vel_y
            elif map_height == -map_length + win_height and y - player1.vel_y < 0.5 * win_height:
                map_height += player1.vel_y - (y - 0.5 * win_height)
                y = 0.5 * win_height
            elif map_height + player1.vel_y <= 0:
                map_height += player1.vel_y
            elif map_height + player1.vel_y > 0 and map_height < 0:
                y -= player1.vel_y - (map_height)
                map_height = 0
            elif y - player1.vel_y >= 0:
                y -= player1.vel_y
            else:
                y = 0
                if -player1.vel_y < dir_x * 0.5 < player1.vel_y:
                    player1.vel *= -player1.wall_bounce
                else:
                    player1.vel /= 1.5

        elif player1.vel_y < 0:
            if map_height == 0 and y - player1.vel_y <= 0.5 * win_height:
                y -= player1.vel_y
            elif map_height == 0 and y - player1.vel_y > 0.5 * win_height:
                map_height += player1.vel_y - (y - 0.5 * win_height)
                y = 0.5 * win_height
            elif map_height + player1.vel_y >= -map_length + win_height:
                map_height += player1.vel_y
            elif map_height + player1.vel_y < -map_length + win_height and map_height > -map_length + win_height:
                y -= player1.vel_y + 0.5 * win_height - y
                map_height = -map_length + win_height
            elif y - player1.vel_y + player1.height <= win_height:
                y -= player1.vel_y
            else:
                y = win_height - player1.height
                if player1.vel_y < dir_x * 0.5 < -player1.vel_y:
                    player1.vel *= -player1.wall_bounce
                else:
                    player1.vel /= 1.5

        if player1.vel_x > 0:
            if map_width == 0 and x + player1.vel_x <= 0.5 * win_width:
                x += player1.vel_x

            elif map_width == 0 and x + player1.vel_x > 0.5 * win_width:
                map_width += 0.5 * win_width - x
                x += player1.vel_x - (0.5 * win_width - x)

            elif map_width - player1.vel_x >= -map_wide + win_width:
                map_width -= player1.vel_x


            elif map_width - player1.vel_x < -map_wide + win_width and map_width > -map_wide + win_width:
                x += player1.vel_x + (-map_wide + win_width - map_width)
                map_width = -map_wide + win_width

            elif x + player1.vel_x + player1.width <= win_width:
                x += player1.vel_x
            else:
                x = win_width - player1.width
                if -player1.vel_x < dir_y * 0.5 < player1.vel_x:
                    player1.vel *= -player1.wall_bounce
                else:
                    player1.vel /= 1.5

        elif player1.vel_x < 0:
            if map_width == -map_wide + win_width and x + player1.vel_x >= 0.5 * win_width:
                x += player1.vel_x
            elif map_width == -map_wide + win_width and x - player1.vel_x < 0.5 * win_width:
                map_width -= player1.vel_x + x - 0.5 * win_width
                x = 0.5 * win_width
            elif map_width - player1.vel_x <= 0:
                map_width -= player1.vel_x
            elif map_width - player1.vel_x > 0 and map_width < 0:
                x += player1.vel_x - map_width
                map_width = 0
            elif x + player1.vel_x >= 0:
                x += player1.vel_x
            else:
                x = 0
                if player1.vel_x < dir_y * 0.5 < -player1.vel_x:
                    player1.vel *= -player1.wall_bounce
                else:
                    player1.vel /= 1.5
        if rotate_r:
            if rotation - angle * 0.9 < 0:
                rotation = 360 - angle * 0.9 + rotation
            else:
                rotation -= angle * 0.9
            rotate_r = False



        elif rotate_l:
            if rotation + angle * 0.9 > 360:
                rotation = 0.9 * angle - 360 + rotation
            else:
                rotation += angle * 0.9
            rotate_l = False

        crashed = False
        on= banana2.on_banana()
        if other_banana and on and not drifting:
            dr = threading.Thread(target=drift)
            dr.start()

        # -- Screen Update --#

        # win.fill((grey))
        pos = (x + 0.5 * player1.width, y + 0.5 * player1.height)
        win.blit(map.load, (map_width, map_height))
        if len(check_points) != 0:
            if check_points[checkP_num].location_x() + check_points[checkP_num].width >= x + 0.5 * player1.width >= check_points[checkP_num].location_x() and check_points[checkP_num].location_y() + check_points[checkP_num].height >= y + 0.5 * player1.height >= check_points[checkP_num].location_y():
                checkP_num += 1
                if checkP_num == len(check_points):
                    checkP_num = 0
                    if cycle == map.cycles:
                        if multiplayer:
                            me.client.close()
                        game = False
                        intro = True
                    else:
                        cycle += 1
                        laps.msg = "laps:" + str(cycle) + "/" + str(map.cycles)

        if show_walls:
            for slower in slowers:
                pygame.draw.rect(win, (slower.color),(slower.location_x(), slower.location_y(), slower.width, slower.height))
            for wall in walls:
                pygame.draw.rect(win, (wall.color), (wall.location_x(), wall.location_y(), wall.width, wall.height))
            pygame.draw.rect(win, (blue), (check_points[checkP_num].location_x(), check_points[checkP_num].location_y(),check_points[checkP_num].width, check_points[checkP_num].height))
        laps.display()
        timer.display()
        nameP.x=x
        nameP.y=y-50

        #-- show bananas --#
        if self_banana:
            banana1.display()
        if other_banana:
            banana2.display()
        if multiplayer and not singleplayer:
            packet_text.display()
            in_rot=""
            in_x=""
            in_y=""
            data_out= str(int(x -map_width)) +"%" + str(int(y- map_height))  + "$" + str(int(rotation)) + "*" + nameP.msg + "&"
            if not self_banana:
                banana_sent=False
            if self_banana and banana_sent==False:
                data_out+="b"
                banana_sent=True
            i=0
            try:
                s=data_in
                if s == "wait":
                    pass
                else:
                    if s=="lost":
                        lost.msg =p2_name.msg + " Won"
                        lost.display()
                        time.sleep(2)
                        multiplayer = False
                        game = False
                        intro = True
                        me.client.close()
                        break

                    while s[i] != "%":
                        in_x+=s[i]
                        i+=1
                    i+=1
                    while s[i]!="$":
                        in_y+=s[i]
                        i+=1
                    i+=1
                    while s[i] != "*":
                        in_rot+=s[i]
                        i+=1
                    i+=1
                    if len(p2_name.msg)<4:
                        while s[i] != "&":
                            p2_name.msg+=s[i]
                            i+=1
                    else:
                        while s[i] != "&":
                            i += 1
                    if len(s)-1>= i+1:
                        i+=1
                        if s[i] =="b":
                            banana2.y = float(in_y)
                            banana2.x = float(in_x)
                            start_new_thread(banana2.life_time, (3, False))

            except :
                pass
            if game == False:
                me.connect("disconnect")
            if s!="wait":
                in_x = float(in_x)+ 0.5 * player1.width
                in_y=float(in_y)+ 0.5 * player1.height
                in_rot=float(in_rot)
                p2_name.x=in_x +map_width
                p2_name.y=in_y + map_height - player1.height
                blitRotate(win, enemy, ((in_x + map_width , in_y + map_height)),(w / 2, h / 2), in_rot)
                p2_name.display()
            #pygame.draw.rect(win, (red), (float(in_x) + map_width, float(in_y) + map_height, 100, 100))
        nameP.display()
        fps_text.display()
        # pygame.draw.rect(win, (red), (x, y, player1.width, player1.height))
        blitRotate(win, player, (pos), (w / 2, h / 2), rotation)
        pygame.display.update()
        if game==False and intro and play_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/track0.wav")
            pygame.mixer.music.play(-1)
        fps +=1
# -- Exit --#

pygame.quit()

