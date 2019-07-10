from tkinter import Tk, Canvas
import time
import random
import sys, os, pygame
from pygame.locals import *
pygame.init()


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#SOM
som = pygame.mixer.Sound(resource_path('assets/sound/pong_bip.wav'))

#CLASSES
class Vetor():
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __add__(self, v2):
        v3 = Vetor()
        v3.x = v2.x + self.x
        v3.y = v2.y + self.y
        return v3
    
    def __sub__(self, v2):
        v3 = Vetor()
        v3.x = self.x - v2.x
        v3.y = self.y - v2.y
        return v3

    def __mul__(self, esc):
        v3 = Vetor()
        v3.x = self.x * esc
        v3.y = self.y * esc
        return v3
    __rmul__ = __mul__

class Bola():
    def __init__(self, pos = Vetor(), vel = Vetor()):
        self.pos = pos
        self.vel = vel
        self.imagem = tela.create_rectangle(self.pos.x - RAIOX, self.pos.y + RAIOY, self.pos.x + RAIOX, self.pos.y - RAIOY, fill = 'white')
        
    def atualizar(self,dt):
        dp = self.vel * dt
        self.pos += dp
        img_pos = Vetor(tela.coords(self.imagem)[0] + RAIOX, tela.coords(self.imagem)[1] + RAIOY)
        tela.move(self.imagem, self.pos.x - img_pos.x, self.pos.y - img_pos.y)

    def colisao(self):
        if (self.pos.y - RAIOY) < 0 or (self.pos.y + RAIOY)> HEIGHT:
            self.vel.y *= -1
            som.play()
            if self.pos.y < HEIGHT/2:
                self.pos.y = 0 + RAIOY
            if self.pos.y > HEIGHT/2:
                self.pos.y = HEIGHT - RAIOY

    def colisao_bolada(self,player):
        if player.imagem in tela.find_overlapping(self.pos.x - player.lado[0], self.pos.y - RAIOY, self.pos.x + player.lado[0], self.pos.y + RAIOY):
            self.vel.x *= -1
            som.play()
            if player.pos.x > WIDTH/2:
                self.pos.x = player.pos.x - player.lado[0] - RAIOX - 1
            if player.pos.x < WIDTH/2:
                self.pos.x = player.pos.x + player.lado[0] + RAIOX + 1



class Player():
    def __init__(self, x):
        self.pos = Vetor(x,HEIGHT/2)
        self.vel = Vetor()
        self.lado = (LADOX, LADOY)
        self.score = 0
        self.imagem = tela.create_rectangle(self.pos.x - self.lado[0], self.pos.y + self.lado[1], self.pos.x + self.lado[0], self.pos.y - self.lado[1], fill = 'white')
        
    def atualizar(self,dt):
        dp = self.vel * dt
        self.pos += dp

        img_pos = Vetor(tela.coords(self.imagem)[0] + self.lado[0], tela.coords(self.imagem)[1] + self.lado[1])
        tela.move(self.imagem, self.pos.x - img_pos.x, self.pos.y - img_pos.y)

    def colisao(self):
        if (self.pos.y - self.lado[1]) < 0:
            self.pos.y = 0 + self.lado[1]
        if (self.pos.y + self.lado[1])> HEIGHT:
            self.pos.y = HEIGHT - self.lado[1]

janela = Tk()
janela.title('Do Pong ao Portal')

#VARIÁVEIS GLOBAIS
WIDTH = 800
HEIGHT = 600

RAIOX = WIDTH/80
RAIOY = HEIGHT/60

LADOX = WIDTH/128
LADOY = HEIGHT/16

VEL_JOGADOR = 370
SPEED = 400

GAME_DURATION = 30

tempo = [0.0, time.time()]
gameendtimer = time.time() + GAME_DURATION
countdowntext = ''
i = 0

win_message = ''
restart_message = ''

first_exec = True
running = True

def desaparecer():
    bola.pos.x= random.randint(100,700)
    bola.pos.y = random.randint(100,500)
    janela.after(5000,desaparecer)


def animar():
    global running
    if running == True:
        tempo[0] = tempo[1]
        tempo[1] = time.time()
        dt = tempo[1] - tempo[0]

        objetos[2].colisao_bolada(objetos[0])
        objetos[2].colisao_bolada(objetos[1])
        for ob in objetos:
            ob.colisao()
        for ob in objetos:
            ob.atualizar(dt)
    janela.after(1,animar)

def gamecontrol():
    global running, score, gameendtimer
    
    if running == True:
        if bola.pos.x < 0 or bola.pos.x > WIDTH:
            if bola.pos.x < 0:
                player2.score += 1
            else:
                player1.score += 1
            
            tela.delete(score)
            del score
            score = tela.create_text(WIDTH/2, HEIGHT/10, fill = "white", justify = "center", font = ("Calibri", 70), text = (str(player1.score) + "     " + str(player2.score)))
            respawn()

        if time.time() >= gameendtimer:
            gameover()

    janela.after(1,gamecontrol)

def gameover():
    global running, win_message, restart_message, first_exec
    running = False

    if first_exec == False:
        if player1.score > player2.score:
            winnermsg = "PLAYER 1 WINS!"
        elif player2.score > player1.score:
            winnermsg = "PLAYER 2 WINS!"
        else:
            winnermsg = "TIE!"
        win_message = tela.create_text(WIDTH/2, HEIGHT/2, fill = "white", justify = "center", font = ("Calibri", 70), text = winnermsg)

    first_exec = False
    restart_message = tela.create_text(WIDTH/2, (3 * HEIGHT)/4, fill = "white", justify = "center", font = ("Calibri", 40), text = "PRESS ENTER TO PLAY")

def restartgame():
    global countdowntext, running, win_message, restart_message, i, tempo, gameendtimer, player1, player2, objetos, score

    if i == 0:
        tela.delete(player1.imagem)
        tela.delete(player2.imagem)
        objetos.remove(player1)
        objetos.remove(player2)
        del player1
        del player2

        player1 = Player(WIDTH/64)
        player2 = Player(WIDTH - WIDTH/64)
        objetos.append(player1)
        objetos.append(player2)

        tela.delete(score)
        del score
        score = tela.create_text(WIDTH/2, HEIGHT/10, fill = "white", justify = "center", font = ("Calibri", 70), text = (str(player1.score) + "     " + str(player2.score)))

        
        respawn()
        tela.delete(win_message)
        tela.delete(restart_message)
        
        countdowntext = tela.create_text(WIDTH/2, HEIGHT/2, fill = "white", justify = "center", font = ("Calibri", 70), text = '3')
        tela.after(1000, restartgame)

    if i == 1:
        tela.delete(countdowntext)
        countdowntext = tela.create_text(WIDTH/2, HEIGHT/2, fill = "white", justify = "center", font = ("Calibri", 70), text = '2')
        tela.after(1000, restartgame)

    if i == 2:
        tela.delete(countdowntext)
        countdowntext = tela.create_text(WIDTH/2, HEIGHT/2, fill = "white", justify = "center", font = ("Calibri", 70), text = '1')
        tela.after(1000, restartgame)

    if i == 3:
        tela.delete(countdowntext)
        countdowntext = tela.create_text(WIDTH/2, HEIGHT/2, fill = "white", justify = "center", font = ("Calibri", 70), text = 'START!')
        tela.after(300, restartgame)

    if i == 4:
        tela.delete(countdowntext)
        tempo = [0.0, time.time()]
        gameendtimer = time.time() + GAME_DURATION
        i = -1
        running = True
    
    i += 1

def respawn():
    global bola, directions
    tela.delete(bola.imagem)
    objetos.remove(bola)    
    del bola

    v_unitario = Vetor((random.randint(5,10) * directions[random.randint(0,1)]),random.randint(2,6))
    v_unitario *= 1/((v_unitario.x ** 2 + v_unitario.y ** 2) ** 0.5)
    bola = Bola(Vetor(WIDTH/2, RAIOY + 1), v_unitario * SPEED)
    objetos.append(bola)

#CONTROLES
def input_up(event):
    global running
    if running == True:
        #PLAYER1
        if event.char == 'W' or event.char == 'w':
            player1.vel.y = 0
        if event.char == 'S' or event.char == 's':
            player1.vel.y = 0
        #PLAYER2
        if event.keysym == 'Up':
            player2.vel.y = 0
        if event.keysym == 'Down':
            player2.vel.y = 0
    
def input_down(event):
    global running, countdowntimer, i
    if running == True:
        #PLAYER1
        if event.char == 'W' or event.char == 'w':
            player1.vel.y = -1 * VEL_JOGADOR
        if event.char == 'S' or event.char == 's':
            player1.vel.y = VEL_JOGADOR

        #PLAYER2
        if event.keysym == 'Up':
            player2.vel.y = -1 * VEL_JOGADOR
        if event.keysym == 'Down':
            player2.vel.y = VEL_JOGADOR

    if running == False and i == 0:
        if event.keysym == 'Return':
            restartgame()
    

#background
tela = Canvas(janela,width = WIDTH, height = HEIGHT, bg = 'black')
tela.pack()
linha = tela.create_rectangle(WIDTH/2 - WIDTH/128, 0, WIDTH/2 + WIDTH/128, HEIGHT, fill = 'white')

#bola
directions = (1,-1)
v_unitario =  Vetor((random.randint(5,10) * directions[random.randint(0,1)]),random.randint(2,6))
v_unitario *= 1/((v_unitario.x ** 2 + v_unitario.y ** 2) ** 0.5)
bola = Bola(Vetor(WIDTH/2, RAIOY + 1), v_unitario * SPEED)

#JOGADORES
player1 = Player(WIDTH/64)
player2 = Player(WIDTH - WIDTH/64)

#ELEMENTOS DE TELA
score = tela.create_text(WIDTH/2, HEIGHT/10, fill = 'white', justify = "center", font = ("Calibri", 70), text = (str(player1.score) + "     " + str(player2.score)))

#OBJECTOS
objetos = [player1, player2, bola]

#MAIN LOOP
janela.bind_all('<KeyPress>', input_down)
janela.bind_all('<KeyRelease>', input_up)
gameover()
gamecontrol()
desaparecer()
animar()
janela.mainloop()
