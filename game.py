import pgzrun
import random
import math

current_music = None
WIDTH = 1536
HEIGHT = 1024

game_state = "menu"
sound_on = True
music_playing = False
zombies = []
attack_range = 80
attack_cooldown = 20



wave=1
zombies_per_wave=5

mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2 #take mouse position

menu_buttons = [
    {"label": "Start Game", "pos": (WIDTH // 2, 550), "action": "start"},
    {"label": "Toggle Sound", "pos": (WIDTH // 2, 630), "action": "sound"},
    {"label": "Exit", "pos": (WIDTH // 2, 710), "action": "exit"},
]

def draw_bloodyscreen():
    health_percentage = hero.health / 12

    if health_percentage >= 1:
        return
    elif health_percentage > 0.75:
        screen.blit("bloodyscreen25", (0, 0))
    elif health_percentage > 0.5:
        screen.blit("bloodyscreen50", (0, 0))
    elif health_percentage > 0.25:
        screen.blit("bloodyscreen75", (0, 0))
    else:
        screen.blit("bloodyscreen100", (0, 0))

def start_new_wave():
    global zombies, wave, zombies_per_wave, hero

    zombies = []
    for _ in range(zombies_per_wave):
        x = random.randint(100, WIDTH-100)
        y = random.randint(100, HEIGHT-100)
        zombies.append(Zombie(x, y, random.uniform(1, 3.5)))

    hero.health = 12  # her dalgada can fullensin
    wave += 1
    zombies_per_wave += 2  # her dalgada daha fazla zombi gelsin


class Hero:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 3
        self.direction = "down"
        self.walk_frame = 0
        self.idle_frame = 0
        self.attack_frame = 0
        self.anim_timer = 0
        self.is_attacking = False
        self.attack_cooldown_timer = 0
        self.invincible_timer = 0
        self.health = 12
        self.is_dead = False
        self.is_dying = False
        self.death_frame = 0
        self.death_anim_timer = 0
        ###FRAMES###
        self.death_images = [f"warriordeath{i}" for i in range(1, 6)]


        self.images = {
            "up":    [f"warriorupwalk{i}" for i in range(1, 9)],
            "down":  [f"warriordownwalk{i}" for i in range(1, 9)],
            "left":  [f"warriorleftwalk{i}" for i in range(1, 9)],
            "right": [f"warriorrightwalk{i}" for i in range(1, 9)]
        }

        self.idle_images = [f"warriordownidle{i}" for i in range(1, 6)]

        self.attack_images = {
            "up":    [f"warriorupattack01_{i}" for i in range(1, 7)],
            "down":  [f"warriordownattack01_{i}" for i in range(1, 7)],
            "left":  [f"warriorleftattack01_{i}" for i in range(1, 7)],
            "right": [f"warriorrightattack01_{i}" for i in range(1, 7)]
        }

        self.image = self.images["down"][0]

    def update(self):
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
        self.attack_cooldown_timer = 0  # saldırıları dursun ozbek
        if self.is_dead:
            return

        if self.is_dying:
            self.death_anim_timer += 1
            if self.death_anim_timer % 5 == 0:
                if self.death_frame < len(self.death_images) - 1:
                    self.death_frame += 1
                else:
                    self.is_dead = True
            self.image = self.death_images[self.death_frame]
            return
        
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if self.is_attacking:
            self.anim_timer += 1
            if self.anim_timer % 4 == 0:
                self.attack_frame += 1
                if self.attack_frame >= 6:
                    self.attack_frame = 5
                    self.is_attacking = False
            self.image = self.attack_images[self.direction][self.attack_frame]
            return

        moved = False
        if keyboard.w:
            self.y -= self.speed
            self.direction = "up"
            moved = True
        elif keyboard.s:
            self.y += self.speed
            self.direction = "down"
            moved = True

        if keyboard.a:
            self.x -= self.speed
            self.direction = "left"
            moved = True
        elif keyboard.d:
            self.x += self.speed
            self.direction = "right"
            moved = True

        self.anim_timer += 1

        if moved:
            if self.anim_timer % 2 == 0:
                self.walk_frame = (self.walk_frame + 1) % 8
            self.image = self.images[self.direction][self.walk_frame]
            self.idle_frame = 0
        else:
            if self.anim_timer % 8 == 0:
                self.idle_frame = (self.idle_frame + 1) % 5
            self.image = self.idle_images[self.idle_frame]

    def attack(self):
        if self.attack_cooldown_timer > 0:
            return

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

        self.is_attacking = True
        self.attack_frame = 0
        self.anim_timer = 0
        self.attack_cooldown_timer = attack_cooldown

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Zombie:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.frame = 0
        self.anim_timer = 0
        self.direction = "down"
        self.health = 3
        self.is_hurt = False
        self.hurt_frame = 0
        self.hurt_anim_timer = 0
        self.invincible_timer = 0
        self.is_dead = False
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_timer = 0  # bak şuna iyice arastir
        self.is_dying = False
        self.death_frame = 0
        self.death_anim_timer = 0
        ###FRAMES###
        self.death_images = [f"goblindeath{i}" for i in range(1, 10)]

        self.images = {
            "up":    [f"goblinuprun{i}" for i in range(1, 7)],
            "down":  [f"goblindownrun{i}" for i in range(1, 7)],
            "left":  [f"goblinleftrun{i}" for i in range(1, 7)],
            "right": [f"goblinrightrun{i}" for i in range(1, 7)]
        }

        self.hurt_images = {
            "up":    [f"goblinuphurt{i}" for i in range(1, 5)],
            "down":  [f"goblindownhurt{i}" for i in range(1, 5)],
            "left":  [f"goblinlefthurt{i}" for i in range(1, 5)],
            "right": [f"goblinrighthurt{i}" for i in range(1, 5)]
        }

        self.attack_images = {#1 frame silindi 10 oldu
            "up":    [f"goblinupattack01_{i}" for i in range(1, 11)],
            "down":  [f"goblindownattack01_{i}" for i in range(1, 11)],
            "left":  [f"goblinleftattack01_{i}" for i in range(1, 11)],
            "right": [f"goblinrightattack01_{i}" for i in range(1, 11)]
        }

        self.image = self.images["down"][0]

    def take_damage(self, hero):
        if self.invincible_timer > 0 or self.is_dying:
            return
        self.health -= 1
        self.is_hurt = True
        self.hurt_frame = 0
        self.hurt_anim_timer = 0
        self.invincible_timer = 10
        knockback(self, hero)
        if self.health <= 0:
            self.is_dying = True
            self.is_hurt = False  # hurt iptal


    def update(self, target_x, target_y):
        if self.is_dead:
            return

        if self.is_dying:
            self.death_anim_timer += 1
            if self.death_anim_timer % 5 == 0:
                if self.death_frame < len(self.death_images) - 1:
                    self.death_frame += 1
                else:
                    self.is_dead = True

            self.image = self.death_images[self.death_frame]
            return

    # invincibility-
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    # hurt animasyonu
        if self.is_hurt:
            self.hurt_anim_timer += 1
            if self.hurt_anim_timer % 5 == 0:
                self.hurt_frame += 1
                if self.hurt_frame >= 4:
                    self.is_hurt = False
            self.image = self.hurt_images[self.direction][min(self.hurt_frame, 3)]
            return

    # bak bi şuna
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

    # attack distance
        if distance < 80:
            self.is_attacking = True
        else:
            self.is_attacking = False

        if self.is_attacking:
            self.anim_timer += 1
            if self.anim_timer % 5 == 0:
                self.attack_frame += 1

                if self.attack_frame == 10:
                    if self.attack_timer == 0 and hero.invincible_timer == 0:
                        hero.health -= 1.5
                        hero.invincible_timer = 20
                        self.attack_timer = 1

                if self.attack_frame >= 10:
                    self.attack_frame = 0
                    self.attack_timer = 0

            self.image = self.attack_images[self.direction][self.attack_frame]

    # saldırı yok walk
        else:
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.x += self.speed
                    self.direction = "right"
                else:
                    self.x -= self.speed
                    self.direction = "left"
            else:
                if dy > 0:
                    self.y += self.speed
                    self.direction = "down"
                else:
                    self.y -= self.speed
                    self.direction = "up"

            self.anim_timer += 1
            frame_delay = max(1, int(5 / (self.speed * 0.3)))
            if self.anim_timer % frame_delay == 0:
                self.frame = (self.frame + 1) % 6

            self.image = self.images[self.direction][self.frame]


    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def draw_text(text, center, size=50, color="white"):
    screen.draw.text(text, center=center, fontsize=size, color=color, anchor=("center", "center"))


def draw():
    screen.clear()
    if game_state == "menu":
        screen.blit("main_menu_bg", (0, 0))
        for button in menu_buttons:
            draw_text(button["label"], button["pos"], 40, "white")
        draw_text("Survive until Wave 10!", (WIDTH // 2, 450), 50, "red")
    
    elif game_state == "playing":
        screen.blit("map2", (0, 0))
        for z in zombies:
            z.draw()
        hero.draw()
        draw_text("GAME STARTED!", (WIDTH // 2, 40), 40)

        draw_bloodyscreen()#vincetting

    draw_text(f"Wave: {wave-1}", (WIDTH // 2, 80), 40)
    if game_state == "gameover":
        draw_text("GAME OVER", (WIDTH // 2, HEIGHT // 2), 80, "red")

def update():
    global current_music, game_state

    if not sound_on:
        music.stop()
        current_music = None
        return

    if game_state == "menu" and current_music != "main_menu_theme":
        music.stop()
        music.play("main_menu_theme")
        music.set_volume(1)
        current_music = "main_menu_theme"

    elif game_state == "playing" and current_music != "monsterchasemusic":
        music.stop()
        music.play("monsterchasemusic")
        music.set_volume(1)
        current_music = "monsterchasemusic"

    if game_state == "playing":
        hero.update()

        if hero.is_attacking and hero.attack_frame == 2:
            for z in zombies[:]:
                if check_hit(hero, z):
                    z.take_damage(hero)

        for z in zombies[:]:
            z.update(hero.x, hero.y)
            if z.is_dead:
                zombies.remove(z)
        if game_state == "playing" and not zombies:
            start_new_wave()
        if hero.is_dead:
                game_state = "gameover"
                return

def check_hit(hero, zombie):
    dx = zombie.x - hero.x
    dy = zombie.y - hero.y
    dir_vectors = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    dir_x, dir_y = dir_vectors[hero.direction]
    dot = dx * dir_x + dy * dir_y
    distance = math.hypot(dx, dy)
    return distance < attack_range and dot > 0


def knockback(zombie, hero):
    knock_dist = 20
    if hero.direction == "up":
        zombie.y -= knock_dist
    elif hero.direction == "down":
        zombie.y += knock_dist
    elif hero.direction == "left":
        zombie.x -= knock_dist
    elif hero.direction == "right":
        zombie.x += knock_dist


def on_key_down(key):
    if key == keys.SPACE:
        hero.attack()


def on_mouse_move(pos):
    global mouse_x, mouse_y
    mouse_x, mouse_y = pos


def on_mouse_down(pos):
    global game_state, sound_on, zombies
    if game_state == "menu":
        for button in menu_buttons:
            bx, by = button["pos"]
            if abs(pos[0] - bx) < 150 and abs(pos[1] - by) < 40:
                if button["action"] == "start":
                    game_state = "playing"
                    zombies = [
                        Zombie(200, 300, random.uniform(1, 3.5)),
                        Zombie(800, 500, random.uniform(1, 3.5)),
                        Zombie(1500, 700, random.uniform(1, 3.5)),
                        Zombie(500, 100, random.uniform(1, 3.5)),
                        Zombie(1000, 700, random.uniform(1, 3.5)),
                        Zombie(1400, 700, random.uniform(1, 3.5)),
                    ]
                elif button["action"] == "sound":
                    sound_on = not sound_on
                    if not sound_on:
                        music.stop()
                        current_music = None
                    else:
                        music_playing = False
                        current_music = None
                    print("Sound:", "On" if sound_on else "Off")
                elif button["action"] == "exit":
                    quit()


hero = Hero()

pgzrun.go()
