try:
    from random import randint
    from pygame import *
    from time import sleep
    import os
    import shutil

    init()
    mixer.init()
    font.init()

    clock = time.Clock()
    fps = 60

    screen_width = 1366
    screen_height = 768

    screen = display.set_mode((screen_width, screen_height))
    display.set_caption("PyPack Joyride")


    def update_():
        clock.tick(fps)
        display.update()


    class GameSprite(sprite.Sprite):
        def __init__(self, filename, x, y, w, h):
            super().__init__()
            self.image = transform.scale(image.load(filename), (w, h))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.w = w
            self.h = h

        def reset(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))
            color = (255, 0, 0)
            draw.rect(screen, color, Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h), 2)


    class Barry(GameSprite):

        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.t = 0
            self.fall = 0
            self.counter = 0
            self.kind = "run"

        def animate(self):
            self.counter += 1
            if self.kind == "run":
                if 0 <= self.counter < 10:
                    self.image = transform.scale(image.load('img/Walk1.png'), (self.w, self.h))
                elif 10 <= self.counter < 20:
                    self.image = transform.scale(image.load('img/Walk2.png'), (self.w, self.h))
                elif 20 <= self.counter < 30:
                    self.image = transform.scale(image.load('img/Walk3.png'), (self.w, self.h))
                elif 30 <= self.counter < 40:
                    self.image = transform.scale(image.load('img/Walk4.png'), (self.w, self.h))

            elif self.kind == "fly":
                if 0 <= self.counter < 5:
                    self.image = transform.scale(image.load('img/Fly1.png'), (self.w, self.h))
                elif 5 <= self.counter < 10:
                    self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
                elif 10 <= self.counter < 15:
                    self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))
                elif 15 <= self.counter < 20:
                    self.image = transform.scale(image.load('img/Fly1.png'), (self.w, self.h))
                elif 20 <= self.counter < 25:
                    self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
                elif 25 <= self.counter < 30:
                    self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))
                elif 30 <= self.counter < 35:
                    self.image = transform.scale(image.load('img/Fly2.png'), (self.w, self.h))
                elif 35 <= self.counter < 40:
                    self.image = transform.scale(image.load('img/Fly3.png'), (self.w, self.h))

            elif self.kind == "fall":
                self.image = transform.scale(image.load('img/Walk1.png'), (self.w, self.h))

            if self.counter > 40:
                self.counter = 0

        def move(self):
            keys = key.get_pressed()
            if keys[K_SPACE]:
                self.t += 1
                if self.t == 2:
                    bullet = Bullets("img/Bullet.png", self.rect.x, self.rect.y + self.h, 10, 45)
                    bullets.append(bullet)
                    self.t = 0
                    for bullet in bullets:
                        bullet.shoot()

                self.kind = "fly"
                self.rect.y -= self.fall
                self.fall += 0.75
                if sprite.collide_rect(self, floor):
                    self.fall = 4

            if self.fall >= 10:
                self.fall = 10
            elif self.fall <= -20:
                self.fall = -20

            if sprite.collide_rect(self, roof):
                self.rect.y = 41
                self.fall = 0

            if not keys[K_SPACE]:
                self.fall -= 0.75
                self.rect.y -= self.fall
                if sprite.collide_rect(self, floor):
                    self.fall = 0
                    self.rect.y = 645
                    self.kind = "run"
                elif not sprite.collide_rect(self, floor):
                    self.kind = "fall"
                if sprite.collide_rect(self, roof):
                    self.rect.y = 41


    class Explosion(GameSprite):
        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.frame = 0
            self.w = w
            self.h = h

        def explode(self):
            if self.frame == 0:
                explode.play()
            self.frame += 1
            if 0 <= self.frame <= 4:
                self.image = transform.scale(image.load("img/gif/2a9n-8.png"), (self.w, self.h))
            elif 5 <= self.frame <= 9:
                self.image = transform.scale(image.load("img/gif/2a9n-9.png"), (self.w, self.h))
            elif 10 <= self.frame <= 14:
                self.image = transform.scale(image.load("img/gif/2a9n-10.png"), (self.w, self.h))
            elif 15 <= self.frame <= 9:
                self.image = transform.scale(image.load("img/gif/2a9n-11.png"), (self.w, self.h))
            elif 20 <= self.frame <= 24:
                self.image = transform.scale(image.load("img/gif/2a9n-12.png"), (self.w, self.h))
            elif 25 <= self.frame <= 29:
                self.image = transform.scale(image.load("img/gif/2a9n-13.png"), (self.w, self.h))
            elif 30 <= self.frame <= 34:
                self.image = transform.scale(image.load("img/gif/2a9n-14.png"), (self.w, self.h))
            elif 35 <= self.frame <= 39:
                self.image = transform.scale(image.load("img/gif/2a9n-15.png"), (self.w, self.h))
            elif 40 <= self.frame <= 44:
                self.image = transform.scale(image.load("img/gif/2a9n-16.png"), (self.w, self.h))
            elif 45 <= self.frame <= 49:
                self.image = transform.scale(image.load("img/gif/17.png"), (self.w, self.h))
            elif 50 <= self.frame <= 54:
                self.image = transform.scale(image.load("img/gif/18.png"), (self.w, self.h))
            elif 55 <= self.frame <= 59:
                self.image = transform.scale(image.load("img/gif/19.png"), (self.w, self.h))
            elif 60 <= self.frame <= 64:
                self.image = transform.scale(image.load("img/gif/20.png"), (self.w, self.h))
            elif 65 <= self.frame <= 70:
                self.image = transform.scale(image.load("img/gif/21.png"), (self.w, self.h))

            transform.scale(self.image, (self.w, self.h))

            if self.frame == 70:
                self.rect.x = 100000


    class BG(GameSprite):

        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)

        def go(self):
            self.rect.x -= 20


    class Missile(GameSprite):

        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.speed = 26
            self.counter = 0
            self.launched = None
            self.l = None
            self.f = None
            self.wait = None

        def animate(self):

            if 0 <= self.counter < 5:
                self.image = transform.scale(image.load('img/Rocket1.png'), (self.w, self.h))
            elif 5 <= self.counter < 10:
                self.image = transform.scale(image.load('img/Rocket2.png'), (self.w, self.h))
            elif 10 <= self.counter < 15:
                self.image = transform.scale(image.load('img/Rocket3.png'), (self.w, self.h))
            elif 15 <= self.counter < 20:
                self.image = transform.scale(image.load('img/Rocket4.png'), (self.w, self.h))

            self.counter += 1
            if self.counter >= 20:
                self.counter = 0

        def warning(self):
            if not self.launched:
                self.pos = randint(20, 714)
                warning.play()
                self.l = 0
                self.rect.y = self.pos
            self.launch()

        def launch(self):

            if not self.launched:
                self.i = 0
                self.rect.x = 1340
                self.launched = True
                self.wait = 0
                self.f = 0

            if self.wait == 35:
                if self.i != 75:
                    self.rect.x -= self.speed
                    self.i += 1
                else:
                    self.i = 0
                    self.wait = 0
                    self.launched = False
                    self.l = 1

                if self.f != 1:
                    launch.play()
                    self.f = 1

                self.rect.y = self.pos
                self.animate()
            else:
                self.wait += 1


    class MissileTracer(GameSprite):

        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.speed = 26
            self.counter = 0
            self.launched = None
            self.l = None
            self.f = None
            self.wait = None

        def animate(self):

            if 0 <= self.counter < 5:
                self.image = transform.scale(image.load('img/Rocket1.png'), (self.w, self.h))
            elif 5 <= self.counter < 10:
                self.image = transform.scale(image.load('img/Rocket2.png'), (self.w, self.h))
            elif 10 <= self.counter < 15:
                self.image = transform.scale(image.load('img/Rocket3.png'), (self.w, self.h))
            elif 15 <= self.counter < 20:
                self.image = transform.scale(image.load('img/Rocket4.png'), (self.w, self.h))

            self.counter += 1
            if self.counter >= 20:
                self.counter = 0

        def warning(self):
            if not self.launched:
                self.rect.y = barry.rect.y
                warning.play()
                self.l = 0
            self.launch()

        def launch(self):

            if not self.launched:
                self.i = 0
                self.rect.x = 1340
                self.launched = True
                self.wait = 0
                self.f = 0

            if self.wait == 35:
                if self.i != 75:
                    self.rect.x -= self.speed
                    self.i += 1
                else:
                    self.i = 0
                    self.wait = 0
                    self.launched = False
                    self.l = 1

                if self.f != 1:
                    launch.play()
                    self.f = 1

                self.animate()
            else:
                self.wait += 1


    class Bullets(GameSprite):

        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.x = True

        def shoot(self):
            j = randint(-15, 10)
            if self.x:
                self.rect.x = barry.rect.x + 23.5 + j
                self.x = False
            else:
                self.rect.x -= 3


    class Elektrik(GameSprite):
        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.rect.x = 1400
            self.rect.y = randint(21, 718)

        def place(self):
            self.rect.x -= 22

            if self.rect.x <= -150:
                Elektrik_list.remove(self)


    class Koin(GameSprite):
        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.fall = 0
            self.orientation = "positive"
            self.l = 0

        def float(self, speed):
            self.rect.y -= self.fall
            self.rect.x -= speed
            if self.fall >= 13:
                self.orientation = "negative"
            elif self.fall <= -13:
                self.orientation = "positive"
                self.fall += 0.5001

            if self.orientation == "positive":
                self.fall += 0.5
            elif self.orientation == "negative":
                self.fall -= 0.5

            if self.rect.x <= -150:
                self.l = 0
                self.rect.x = screen_width


    def reset(x, y):
        barry.rect.x = x
        barry.rect.y = y
        barry.fall = 0
        barry.kind = "run"

        bullet.rect.y = 1001

        for missile in missiles:
            missile.l = 1
            missile.launched = False
            missile.f = 1
            missile.i = 0
            missile.wait = 0
            missile.rect.x = 1400
            missile.rect.y = 0
        for electric in Elektrik_list:
            electric.l = 1
            electric.rect.x = 1400
        Elektrik_list.clear()


    class achievement(GameSprite):
        def __init__(self, filename, x, y, w, h):
            super().__init__(filename, x, y, w, h)
            self.rect.x = -400
            self.p = 0
            self.o = 0
            self.orientation = "positive"

        def show(self):
            if self.rect.x != 0 and self.orientation == "positive":
                print("mooving")
                self.rect.x += 10

            else:
                self.p += 1
                if self.orientation == "positive" and self.p == 300:
                    self.orientation = "negative"
                elif self.orientation == "negative" and self.rect.x != -400:
                    self.rect.x -= 10


    # load essential files
    MS_DOS = font.Font("fnt/ModernDOS9x16.ttf", 100)
    MS_DOS_smol = font.Font("fnt/ModernDOS9x16.ttf", 25)


    def text(txt, x, y):
        screen.fill((0, 0, 0))
        screen.blit(loading, (430, 0))
        screen.blit(tmtaw, (475, 720))
        text_surface = MS_DOS_smol.render(txt, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        update_()


    lost = MS_DOS.render("YOU LOST.", True, (0, 0, 0), None)
    disclaimer = MS_DOS.render("DISCLAIMER!!!!", True, (255, 0, 0))
    recreation = MS_DOS_smol.render("THIS IS ONLY A RECREATION, NOT A STOLEN GAME!!!", True, (255, 0, 0))
    halfbrick = MS_DOS_smol.render("ALL RIGHTS RESERVED FOR HALFBRICK STUDIOS!!!", True, (255, 0, 0))
    click = MS_DOS_smol.render("PRESS ANYWHERE TO CONTINUE...", True, (255, 255, 255))
    ext = False
    fac = False
    notfac = False

    while not ext:
        for e in event.get():
            if e.type == QUIT:
                exit()

            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                ext = True

        screen.fill((0, 0, 0))
        screen.blit(disclaimer, (300, 0))
        screen.blit(recreation, (335, 250))
        screen.blit(halfbrick, (345, 515))
        screen.blit(click, (455, 720))
        clock.tick(fps)
        display.update()

    github = MS_DOS_smol.render('Press "G" to redirect to the repository.', True, (255, 255, 255))
    fact_res = MS_DOS_smol.render("if you want to do a factory reset, press 'F'.", True, (255, 255, 255))
    run = True
    while run:
        for e in event.get():
            if e.type == QUIT:
                exit()

            elif e.type == KEYDOWN and e.key == K_g:
                os.system("github.url")

            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                run = False

            elif e.type == KEYDOWN and e.key == K_f:
                try:
                    shutil.rmtree('data/')
                    fac = True
                    run = False
                except FileNotFoundError:
                    notfac = True
                    run = False

        screen.fill((0, 0, 0))
        screen.blit(github, (405, 0))
        screen.blit(fact_res, (350, 350))
        screen.blit(click, (455, 720))
        update_()

    fact = MS_DOS.render("FACTORY RESET COMPLETED.", True, (0, 255, 255))
    notfact = MS_DOS.render("FACTORY RESET FAILED.", True, (200, 0, 0))

    if fac:
        screen.fill((0, 0, 0))
        screen.blit(fact, (40, 350))
        update_()
        sleep(3)
        fac = False
    elif notfac:
        screen.fill((0, 0, 0))
        screen.blit(notfact, (150, 350))
        update_()
        sleep(3)
        notfac = False

    # Load assets and variables

    death1 = False
    death10 = False
    death50 = False
    koin = False

    det_cnt = 0

    ez_koin = False

    loading = MS_DOS.render("LOADING...", True, (255, 255, 255))
    tmtaw = MS_DOS_smol.render("THIS MIGHT TAKE A WHILE...", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(loading, (430, 0))
    screen.blit(tmtaw, (475, 720))
    update_()

    text("snd/Warning.mp3", 525, 360)
    sleep(0.15)
    warning = mixer.Sound("snd/Warning.mp3")
    text("snd/Launch.mp3", 525, 360)
    launch = mixer.Sound("snd/Launch.mp3")
    text("data/", 525, 360)

    basepath = os.getcwd()
    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)):
            if entry.find("data") != -1:
                print("Found data folder: " + entry)
            else:
                try:
                    os.mkdir("data/")
                except OSError:
                    pass

    for file in os.listdir(basepath + "/data"):
        if os.path.isfile(os.path.join(basepath + "/data", file)):
            if file.find("death1") != -1:
                death1 = True
            elif file.find("death10") != -1:
                death10 = True
            elif file.find("death50") != -1:
                death50 = True
            elif file.find("koin") != -1:
                koin = True

    text("snd/Theme.mp3", 525, 360)
    theme = mixer.Sound("snd/Theme.mp3")
    text("snd/Explode.mp3", 525, 360)
    explode = mixer.Sound('snd/Explode.mp3')
    text("snd/Elektrik.wav", 525, 360)
    Elektric = mixer.Sound("snd/Elektrik.wav")
    Game = True
    m = 0
    a = 0

    text("ez = MS_DOS_smol.render", 525, 360)
    ez = MS_DOS_smol.render("You need help...", True, (255, 255, 255))
    text("ig = MS_DOS_smol.render", 525, 360)
    ig = MS_DOS_smol.render("I guess I have to increase the chances of the koin....", True, (255, 255, 255))
    text("help = MS_DOS_smol.render", 525, 360)
    help = MS_DOS_smol.render("You need help, don't you?", True, (255, 255, 255))
    text("lhelp = MS_DOS_smol.render", 525, 360)
    lhelp = MS_DOS_smol.render("If you need help, tap 'H'.", True, (255, 255, 255))
    text("ihelp = MS_DOS_smol.render", 525, 360)
    ihelp = MS_DOS_smol.render("That will decrease the chances of the obstacles appearing.", True, (255, 255, 255))
    text("usure = MS_DOS.render", 525, 360)
    usure = MS_DOS.render("ARE YOU SURE???", True, (150, 0, 0))
    text("usure2 = MS_DOS_smol.render", 525, 360)
    usure2 = MS_DOS_smol.render("If you click, you will continue.", True, (150, 0, 0))
    text("usure3 = MS_DOS_smol.render", 525, 360)
    usure3 = MS_DOS_smol.render('If you tap "h", then you will continue easily.', True, (150, 0, 0))
    text("pause = MS_DOS.render", 525, 360)
    pause = MS_DOS.render("PAUSED", True, (255, 255, 255))

    text("img/Fly1.png", 525, 360)
    text("img/Fly2.png", 525, 360)
    text("img/Fly3.png", 525, 360)
    text("img/Fly4.png", 525, 360)
    text("img/FlyFall.png", 525, 360)
    text("img/Walk1.png", 525, 360)
    text("img/Walk2.png", 525, 360)
    text("img/Walk3.png", 525, 360)
    text("img/Walk4.png", 525, 360)
    barry = Barry("img/Walk1.png", 20, 675, 64, 74)

    text('img/Missile_target.png', 525, 360)
    target = 'img/Missile_Target.png'
    text("img/Koin.png", 525, 360)
    koin = Koin("img/Koin.png", screen_width, 470, 80, 80)
    text("img/booster.png", 525, 360)
    booster = Koin("img/booster.png", screen_width, 470, 110, 110)
    text("img/Floor.png", 525, 360)
    floor = GameSprite("img/floor.png", 0, 718, screen_width, 50)
    text("img/Roof.png", 525, 360)
    roof = GameSprite("img/roof.png", 0, 0, screen_width, 40)
    text("pepe-gif.gif", 525, 360)
    pepo = GameSprite("pepe-gif.gif", 616, 384, 408, 384)
    text("img/pepo_shock.png", 525, 360)
    pepo_shock = GameSprite("img/pepo_shock.png", 0, 336, 440, 432)
    text("img/pepo_cry.png", 525, 360)
    pepo_cry = GameSprite("img/pepo_cry.png", 0, screen_height - 421, 500, 421)
    text("img/pepo_disappointed.png", 525, 360)
    pepo_disappointed = GameSprite("img/disappointed_pepo.png", 0, screen_height - 550, 550, 550)
    text("img/Missile_Target.png", 525, 360)
    missile = MissileTracer(target, 0, 0, 93, 34)
    text("img/Rocket1.png", 525, 360)
    missile2 = Missile(target, 0, 0, 93, 34)
    text("img/Rocket2.png", 525, 360)
    missile3 = Missile(target, 0, 0, 93, 34)
    text("img/Rocket3.png", 525, 360)
    text("img/Rocket4.png", 525, 360)

    text("img/bg.jpg", 525, 360)
    bg = BG("img/bg.jpg", 0, 0, 2740, 1000)
    text("img/bg_rvrs.jpg", 525, 360)
    bg_rvrs = BG("img/bg_rvrs.jpg", 2740, 0, 2740, 1000)

    bgs = [bg, bg_rvrs]

    text("img/[explosions].png", 525, 360)
    explosion = Explosion("img/gif/2a9n-8.png", 0, 0, 1000, 1000)

    missiles = [missile, missile2, missile3]

    text("img/bullet.png", 525, 360)
    bullet = Bullets("img/Bullet.png", 500, 450, 10, 45)

    bullets = [bullet]

    Elektrik_list = []
    powerup = False
    times = 0
    stage = "run"
    diff = "normal"

    text("img/1.bmp", 525, 360)
    deth1 = achievement("img/1.bmp", -400, 0, 400, 269)
    text("img/10.bmp", 525, 360)
    deth10 = achievement("img/10.bmp", -400, 0, 400, 269)
    text("img/50.bmp", 525, 360)
    deth50 = achievement("img/50.bmp", -400, 0, 400, 269)
    text("img/koin.bmp", 525, 360)
    pepo_koin = achievement("img/koin.bmp", -400, 0, 400, 269)

    warning.set_volume(0.1)
    launch.set_volume(0.1)
    theme.set_volume(0.1)
    explode.set_volume(0.1)
    Elektric.set_volume(0.1)

    while Game:
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif stage == "lost" and e.type == MOUSEBUTTONDOWN and e.button == 1:
                reset(20, 675)
                stage = "run"
            elif e.type == KEYDOWN and e.key == K_o:
                times = 9
                det_cnt = 9
            elif e.type == KEYDOWN and e.key == K_5:
                times = 49
                det_cnt = 49
            elif e.type == KEYDOWN and e.key == K_p:
                powerup = True
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                stage = "pause"
            elif stage == "pause" and e.type == MOUSEBUTTONDOWN and e.button == 1:
                warning.set_volume(0.5)
                launch.set_volume(0.5)
                theme.set_volume(0.5)
                explode.set_volume(0.5)
                Elektric.set_volume(0.5)
                stage = "run"
            elif e.type == KEYDOWN and e.key == K_r:
                booster.l = 1

        if stage == "run":
            if m == 0:
                theme.play()
                m = 1
            screen.fill((100, 100, 100))
            if bg.rect.x == -2740:
                bg.rect.x = 2740
            elif bg_rvrs.rect.x == -2740:
                bg_rvrs.rect.x = 2740
            bg.reset()
            bg.go()
            bg_rvrs.reset()
            bg_rvrs.go()

            floor.reset()
            roof.reset()
            barry.animate()
            barry.move()
            barry.reset()

            for bullet in bullets:
                bullet.reset()
                bullet.rect.y += 25

            if ez_koin:
                koin_rand = (1, 500)
                booster_rand = (1, 1500)
            else:
                koin_rand = randint(1, 1000)
                booster_rand = randint(1, 1500)

            if koin_rand == 500 and not powerup:
                koin.l = 1

            if koin.l == 1:
                koin.reset()
                koin.float(10)
                if sprite.collide_rect(barry, koin):
                    powerup = True
                    koin.l = 0
                    try:
                        open("data/koin", "x")
                        pepo_koin.o = 1
                        ez_koin = True
                    except FileExistsError:
                        pass

            elif koin.l == 0:
                koin.rect.x = 1366
                koin.rect.y = 460
                koin.fall = 0

            if booster.l == 1:
                booster.reset()
                booster.float(20)
                if sprite.collide_rect(barry, booster):
                    powerup = True
                    booster.l = 0
                    try:
                        open("data/booster", "x")
                        pepo_koin.o = 1
                        ez_koin = True
                    except FileExistsError:
                        pass

            if booster_rand == 1500:
                booster.l = 1

            lnch = randint(1, 225)
            if missile.l == 0:
                for missile in missiles:
                    missile.warning()
                    missile.reset()
                    if not powerup and sprite.collide_rect(barry, missile):
                        stage = "lost"
                        explode.play()
                        times += 1
                        det_cnt += 1
                    if powerup and sprite.collide_rect(barry, missile):
                        powerup = False
                        reset(barry.rect.x, barry.rect.y)

            for elektrik in Elektrik_list:
                if elektrik.l == 0:
                    elektrik.reset()
                    elektrik.place()
                    if not powerup and sprite.collide_rect(barry, elektrik):
                        stage = "lost"
                        Elektric.play()
                        times += 1
                        det_cnt += 1
                    if powerup and sprite.collide_rect(barry, elektrik):
                        powerup = False
                        Elektrik_list.remove(elektrik)
                        reset(barry.rect.x, barry.rect.y)

            if diff == "normal":
                if lnch == 70 or lnch == 80 or lnch == 90:
                    elektrik = Elektrik("img/elektrik.png", 1376, 0, 282, 68)
                    elektrik.l = 0
                    Elektrik_list.append(elektrik)

                elif lnch == 10 or lnch == 20 or lnch == 30:
                    elektrik = Elektrik("img/elektrik_vert.png", 1376, 0, 68, 282)
                    elektrik.l = 0
                    Elektrik_list.append(elektrik)

                elif lnch == 35 or lnch == 45 or lnch == 55:
                    for missile in missiles:
                        missile.l = 0
            else:
                if lnch == 70:
                    elektrik = Elektrik("img/elektrik.png", 1376, 0, 282, 68)
                    elektrik.l = 0
                    Elektrik_list.append(elektrik)

                elif lnch == 10:
                    elektrik = Elektrik("img/elektrik_vert.png", 1376, 0, 68, 282)
                    elektrik.l = 0
                    Elektrik_list.append(elektrik)

                elif lnch == 35:
                    for missile in missiles:
                        missile.l = 0

            for bullet in bullets:
                if sprite.collide_rect(bullet, floor):
                    bullets.remove(bullet)

            explosion.reset()
            explosion.explode()


        elif stage == "lost":
            while times == 10 or times == 11 or times == 12:
                screen.fill((25, 25, 25))
                pepo.reset()
                screen.blit(help, (500, 0))
                screen.blit(lhelp, (500, 150))
                screen.blit(ihelp, (290, 300))
                for e in event.get():
                    if e.type == QUIT:
                        exit()
                    if e.type == KEYDOWN and e.key == K_h:
                        diff = "less"
                        times = 14
                    elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                        times = 13

                if deth10.o == 1:
                    deth10.reset()
                    deth10.show()

                if pepo_koin.o == 1:
                    pepo_koin.reset()
                    pepo_koin.show()
                update_()

            while times == 13:
                screen.fill((25, 25, 25))
                pepo_shock.reset()
                screen.blit(usure, (280, 0))
                screen.blit(usure2, (475, 200))
                screen.blit(usure3, (400, 400))
                for e in event.get():
                    if e.type == QUIT:
                        exit()

                    elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                        reset(20, 675)
                        times = 14
                    elif e.type == KEYDOWN and e.key == K_h:
                        diff = "less"
                        times = 14

                if deth10.o == 1:
                    deth10.reset()
                    deth10.show()

                if pepo_koin.o == 1:
                    pepo_koin.reset()
                    pepo_koin.show()
                update_()

            while times == 50 or times == 51 or times == 52 or times == 53:
                screen.fill((0, 0, 0))
                pepo_cry.reset()
                screen.blit(ez, (550, 0))
                screen.blit(click, (455, 720))
                for e in event.get():
                    if e.type == QUIT:
                        exit()

                    elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                        reset(20, 675)
                        times = 54

                if deth50.o == 1:
                    deth50.reset()
                    deth50.show()

                if pepo_koin.o == 1:
                    pepo_koin.reset()
                    pepo_koin.show()
                update_()
            while times == 54:
                screen.fill((25, 25, 25))
                pepo_disappointed.reset()
                screen.blit(ig, (250, 0))
                screen.blit(click, (455, 720))
                for e in event.get():
                    if e.type == QUIT:
                        exit()

                    elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                        reset(20, 675)
                        times = 55
                        ez_koin = True

                if deth50.o == 1:
                    deth50.reset()
                    deth50.show()

                if pepo_koin.o == 1:
                    pepo_koin.reset()
                    pepo_koin.show()
                update_()
            else:
                screen.fill((100, 0, 0))
                screen.blit(lost, (440, 330))

        elif stage == "pause":
            screen.fill((0, 0, 0))
            screen.blit(pause, (425, 330))
            screen.blit(click, (455, 720))
            warning.set_volume(0)
            launch.set_volume(0)
            theme.set_volume(0)
            explode.set_volume(0)
            Elektric.set_volume(0)
            for e in event.get():
                if e.type == QUIT:
                    exit()
            update_()

        if det_cnt == 1 or det_cnt == 2 or det_cnt == 3:
            try:
                open("data/death1", "x")
                deth1.o = 1
                deth1.orientation = "positive"
            except FileExistsError:
                pass

        elif det_cnt == 10 or det_cnt == 11 or det_cnt == 12:
            try:
                open("data/death10", "x")
                deth10.o = 1
                deth10.orientation = "positive"
            except FileExistsError:
                pass

        elif det_cnt == 50 or det_cnt == 51 or det_cnt == 52:
            try:
                open("data/death50", "x")
                deth50.o = 1
                deth50.orientation = "positive"
            except FileExistsError:
                pass

        if deth1.o == 1:
            deth1.reset()
            deth1.show()

        if deth10.o == 1:
            deth10.reset()
            deth10.show()

        if deth50.o == 1:
            deth50.reset()
            deth50.show()

        if pepo_koin.o == 1:
            pepo_koin.reset()
            pepo_koin.show()
        update_()
except:
    pass