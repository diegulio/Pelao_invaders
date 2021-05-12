#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
from random import randint
 
# Constantes
WIDTH = 900
HEIGHT = 600
Color = pygame.Color(0,140,60)
color_linea=pygame.Color(0,24,150)
listaEnemigo=[]
x,y = 500,350
velocidad = 5


# ---------------------------------------------------------------------
# Customize your Images and sounds!

# Player
PlayerImage = 'images/pelao.png'
GameOverImage = 'images/go.png'
ShootImage = 'Images/disparo.png'

#Bad guys 


# Bad Diegulio
BadShootImg = 'Images/disparo_m.png'
Bad1Img1 = "images/diego1.png"
Bad1Img2 = "images/diego2.png"
Bad1Sound = 'sound/diego.wav'

# Bad Jirafilla

Bad2Img1 = "images/dani1.png"
Bad2Img2 = "images/dani2.png"
Bad2Sound = 'sound/dani.wav'


# BackgroundSound
BackgroundSound = 'sound/temazo.wav'



# Customize your Sounds!
ShootSound = 'sound/shoot.wav'
GameOverSound = 'sound/go.wav'




 
# Clases
# ---------------------------------------------------------------------
class nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImageJugador = pygame.image.load(PlayerImage)
        self.shoot_sound = pygame.mixer.Sound(ShootSound)
        self.sonidomuerte = pygame.mixer.Sound(GameOverSound)
        self.ImageMuerte = pygame.image.load(GameOverImage)
        #Creamos el rectangulod de la imagen
        self.rect = self.ImageJugador.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT-50
        #Atributos
        self.listaDisparo = []
        self.Vida = True
        
        self.velocidad = 5
        
        
    def derecha(self):
        if self.Vida:   
            self.rect.right+= self.velocidad
            if self.rect.right>WIDTH:
                self.rect.right = WIDTH 
    def izquierda(self):
        if self.Vida:
            self.rect.left -= self.velocidad
            if self.rect.left < 0:
                self.rect.left = 0
            
    def disparar(self,x,y):
        self.shoot_sound.play()
        disparo_ = disparo(x,y,ShootImage,True)
        self.listaDisparo.append(disparo_)
    def aparecer(self,ventana):
        ventana.blit(self.ImageJugador,self.rect)
    def destruccion(self):
        self.sonidomuerte.play()
        self.Vida = False
        self.velocidad = 0
        self.ImageJugador=self.ImageMuerte
        self.listaDisparo=[]
    

class disparo(pygame.sprite.Sprite):
    def __init__(self,x,y,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imageDisparo = pygame.image.load(ruta)
        
        self.rect = self.imageDisparo.get_rect()
        self.rect.left=x
        self.rect.top=y
        
        self.disparoPersonaje = personaje
        self.velocidad = 5
        
    def trayectoria(self):
        if self.disparoPersonaje:
            self.rect.top  = self.rect.top - self.velocidad
        else:
            self.rect.top  = self.rect.top + self.velocidad
        
        
    def aparecer(self,ventana):
        ventana.blit(self.imageDisparo,self.rect)
        
        
class malulo(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagen1,imagen2,nombre):
        pygame.sprite.Sprite.__init__(self)
        self.ImageA = pygame.image.load(imagen1)
        self.ImageB = pygame.image.load(imagen2)
        self.auch= pygame.mixer.Sound(nombre)
        self.ListaImages=[self.ImageA,self.ImageB]
        self.posimg=0
        #Creamos el rectangulod de la imagen
        self.ImageMalulo = self.ListaImages[self.posimg] 
        self.rect = self.ImageMalulo.get_rect()
        self.rect.top=posy
        self.rect.left=posx
        
        #Atributos
        self.listaDisparo = []
    
        
        self.velocidad = 10
        self.rangoDisparo = 2
        self.tiempoCambio=1.0
        
        #atributos movimiento
        self.derecha = True
        self.contador =0
        self.Maxdescenso = self.rect.top+ 40 
        
        self.limiteDerecha=posx + distancia
        self.limiteIzquierda=posx-distancia
        
        self.conquista = False
        
        
    def aparecer(self,ventana):
       self.imagenEnemigo =self.ListaImages[self.posimg]
       ventana.blit(self.imagenEnemigo,self.rect)   

    def cambio(self,tiempo):
        if not(self.conquista):   
            self.__movimientos()
            self.__ataque()
            if self.tiempoCambio-tiempo<10e-8:
                self.posimg+=1
                self.tiempoCambio+=1
                if self.posimg > len(self.ListaImages)-1:
                    self.posimg=0
                    
    def __movimientos(self):
        if self.contador<3:
            self.__movimientoLateral()
        else:
            self.__descenso()
            
    def __descenso(self):
        if self.Maxdescenso == self.rect.top:
            self.contador = 0
            self.Maxdescenso = self.rect.top + 40
        else:
            self.rect.top+=1
            
    def __movimientoLateral(self):
        if self.derecha:
            self.rect.right+=self.velocidad
            if self.rect.right>self.limiteDerecha:
                self.derecha = False
                self.contador+=1
        else:
            self.rect.left-=self.velocidad
            if self.rect.left<self.limiteIzquierda:
                self.derecha = True
    def destruccion(self):
        self.auch.play()
                
            
        
        
    def __ataque(self):
        if randint(0,100) < self.rangoDisparo:
            x,y = self.rect.center
            self.__disparo(x,y)
    def __disparo(self,x,y):
        disparo_ = disparo(x,y,BadShootImg,False)
        self.listaDisparo.append(disparo_)
        
    
      
            
        

# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
def cargarEnemigos():
    enemigo1= malulo(200,0,100,Bad1Img1,Bad1Img2,Bad1Sound)
    enemigo2= malulo(500,0,100,Bad1Img1,Bad1Img2,Bad1Sound)
    enemigo3= malulo(800,0,100,Bad1Img1,Bad1Img2,Bad1Sound)
    
    enemigo1A= malulo(200,-100,100,Bad2Img1,Bad1Img2,Bad2Sound)
    enemigo2A= malulo(500,-100,100,Bad2Img1,Bad1Img2,Bad2Sound)
    enemigo3A= malulo(800,-100,100,Bad2Img1,Bad1Img2,Bad2Sound)
    
    listaEnemigo.extend([enemigo1,enemigo2,enemigo3,enemigo1A,enemigo2A,enemigo3A])
    
def stop():
    for enemigo in listaEnemigo:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
            
        enemigo.conquista= True
    
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juegulio")
    miFuenteSistema = pygame.font.SysFont('Arial',30)
    texto = miFuenteSistema.render('GAME OVER',0,(120,100,40))
    texto_win = miFuenteSistema.render('WENAA GANASTEE',0,(120,100,40))
    cancion = pygame.mixer.Sound(BackgroundSound)
    cancion.play(3)
    Jugando = True #Para saber si gano o perdio
    reloj = pygame.time.Clock() #tiempo
    jugador=nave()
    cargarEnemigos()
    #disparo_jugador=disparo(jugador.rect.centerx/2,jugador.height)
    while True:
        reloj.tick(60) #para controlar os FPS
        tiempo = pygame.time.get_ticks()/1000
        screen.fill(Color)
        jugador.aparecer(screen)
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            if Jugando:
                if eventos.type ==pygame.KEYDOWN: 
                    if eventos.key == K_SPACE:
                        x,y = jugador.rect.center
                        jugador.disparar(x,y)
        if Jugando:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_LEFT] or keys_pressed[K_a]:
                jugador.izquierda()
            if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
                jugador.derecha()
            
    
    #Disparo Jugador
        for proyectil in jugador.listaDisparo:
            proyectil.aparecer(screen)
            proyectil.trayectoria()
            if proyectil.rect.top <50:
                jugador.listaDisparo.remove(proyectil)
            else:
                for enemigo in listaEnemigo:
                    if proyectil.rect.colliderect(enemigo.rect):
                        enemigo.destruccion()
                        listaEnemigo.remove(enemigo)
                        jugador.listaDisparo.remove(proyectil)
    #Disparo Enemigo
        if len(listaEnemigo)>0:
            for enemigo in listaEnemigo:
                enemigo.cambio(tiempo)
                enemigo.aparecer(screen)
                if enemigo.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    Jugando = False
                    stop()
                elif enemigo.rect.bottom>=HEIGHT:
                    Jugando=False
                    stop()
                for proyectil in enemigo.listaDisparo:
                    proyectil.aparecer(screen)
                    proyectil.trayectoria()
                    if proyectil.rect.colliderect(jugador.rect):
                        jugador.destruccion()
                        Jugando=False
                        stop()
                    if proyectil.rect.top >500:
                        enemigo.listaDisparo.remove(proyectil)
                    else:
                        for disparo in jugador.listaDisparo:
                            if proyectil.rect.colliderect(disparo.rect):
                                jugador.listaDisparo.remove(disparo)
                                enemigo.listaDisparo.remove(proyectil)
        elif len(listaEnemigo) == 0:
            stop()
            screen.blit(texto_win,(WIDTH/2,HEIGHT/2))
            
                
        if not(Jugando):
            pygame.mixer.fadeout(3000)
            screen.blit(texto,(WIDTH/2,HEIGHT/2))
            
            
        pygame.display.update()
    return 0

if __name__ == '__main__':
    pygame.init()
    main()