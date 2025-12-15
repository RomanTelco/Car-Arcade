# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 19:52:34 2025

@author: Neo-PC
"""

#Importamos las bibliotecas utilizadas
import pygame
import random
import sys

#%%
#Inicializamos pygame
pygame.init()
    
#%%
#Pantalla principal
Ancho = 800
Alto = 600
screen = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Car Arcade")

#%%
#Colores utlizados
Negro = (0,0,0) 
Blanco = (255,255,255) 
Rojo = (255,0,0) 
Azul = (0,120,255) 
Verde = (0,255,0) 
Amarillo = (255,255,0) 
Gris = (100, 100, 100) 
Gris_Oscuro = (50,50,50) 
Verde_Inicio = (0, 200, 0)
Verde_Flotante = (0, 230, 0)

#%%
#Objetos del videojuego
#Coche Principal
class CochePrincipal(pygame.sprite.Sprite): #Sprite: objeto de pygame
    def __init__(self):
        super().__init__() #Esta funcion llama al constructor de clase padre Sprite
        self.image= pygame.Surface((40,60)) #Superficie de 40x60 pixeles del coche
        self.image.fill(Azul) #Pintamos el coche de azul
        
        #Color del coche principal
        pygame.draw.rect(self.image, Azul, (5,15,30,30)) #Cuerpo
        pygame.draw.circle(self.image, Negro, (10,10),8) #Rueda delantera izquierda
        pygame.draw.circle(self.image, Negro, (30,10),8) #Rueda delantera derecha
        pygame.draw.circle(self.image, Negro, (10,50),8) #Rueda trasera izquierda
        pygame.draw.circle(self.image, Negro, (30,50),8) #Rueda trasera derecha
        
        #Dimensiones del coche y su velocidad
        self.rect = self.image.get_rect()
        self.rect.centerx = Ancho // 2
        self.rect.bottom = Alto - 50
        self.speed = 8
        self.lanes = [Ancho//4, Ancho//2, 3*Ancho//4]
        self.current_lane = 1
        
    #Frames del estado del jugador
    def update(self):
        keys = pygame.key.get_pressed()
            
        #Flecha izquierda, carril izquierdo
        if keys[pygame.K_LEFT] and self.current_lane > 0:
            self.current_lane -= 1
            pygame.time.delay(100)
                
        #Flecha derecha, carril derecho
        if keys[pygame.K_RIGHT] and self.current_lane < 2:
            self.current_lane += 1
            pygame.time.delay(100)   
                
        #Suavizar movimiento
        target_x = self.lanes[self.current_lane]
            
        if abs(self.rect.centerx - target_x) > 2:
            if self.rect.centerx < target_x:
                self.rect.x += min(self.speed, target_x - self.rect.centerx)
            else:
                self.rect.x -= min(self.speed, self.rect.centerx - target_x)
#Coches enemigos                    
class CocheEnemigo(pygame.sprite.Sprite):
    def __init__(self, lane, speed):
        super().__init__()
        self.image = pygame.Surface((40,60))
        #Colores de los coches
        colors = [Verde,Amarillo]
        color = random.choice(colors)
        
        self.image.fill(color)
        pygame.draw.rect(self.image, Verde, (5,15,30,30)) #Cuerpo
        pygame.draw.circle(self.image, Negro, (10,10),8) #Rueda delantera izquierda
        pygame.draw.circle(self.image, Negro, (30,10),8) #Rueda delantera derecha
        pygame.draw.circle(self.image, Negro, (10,50),8) #Rueda trasera izquierda
        pygame.draw.circle(self.image, Negro, (30,50),8) #Rueda trasera derecha
        
    
        self.rect = self.image.get_rect()
        self.lanes = [Ancho//4, Ancho//2, 3*Ancho//4]
        self.rect.centerx = self.lanes[lane]
        self.speed = speed
    
        self.rect.y = -100

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > Alto:
            self.kill()
            
#Carretera
class Carretera:
    def __init__(self):
        self.line_alto = 40
        self.line_ancho = 10
        self.line_brecha = 20
        self.lines = []
        self.speed = 5
        
        #Lineas de carretera iniciales
        for i in range(-self.line_alto, Alto + self.line_alto, self.line_alto + self.line_brecha):
            self.lines.append(i)
            
    def update(self):
        #Las lineas de la carretera se deben mover
        for c in range(len(self.lines)):
            self.lines[c] += self.speed
            if self.lines[c] > Alto + self.line_alto:
                self.lines[c] = -self.line_alto
                
    #Funcion para dibujar la carretera
    def draw(self):
        pygame.draw.rect(screen, Gris_Oscuro, (0, 0, Ancho, Alto))
        
        for i in self.lines:
            pygame.draw.rect(screen, Blanco, (Ancho//2 - self.line_ancho//2, i, self.line_ancho, self.line_alto))
            
        pygame.draw.rect(screen, Blanco, (0, 0, Ancho, 5))
        pygame.draw.rect(screen, Blanco, (0, Alto-5, Ancho, 5))
        
#Botones del juego    
class Boton_Inicio:
    def __init__(self, x, y, ancho, alto, texto, color, color_flotante):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_flotante = color_flotante
        self.color_actual = color
        self.font = pygame.font.Font(None, 48)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color_actual, self.rect, border_radius=15)
        pygame.draw.rect(superficie, Blanco, self.rect, 3, border_radius=15)
        text_surf = self.font.render(self.texto, True, Blanco)
        text_rect = text_surf.get_rect(center=self.rect.center)
        superficie.blit(text_surf, text_rect)
        
    def posicion(self, pos):
        if self.rect.collidepoint(pos):
            self.color_actual = self.color_flotante
            return True
        else:
            self.color_actual = self.color
            return False
        
# Marco para los titulos
class Marco:
    def __init__(self, x, y, ancho, alto, texto, color, tamaño=36):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.font = pygame.font.Font(None, tamaño)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect, border_radius=15)
        pygame.draw.rect(superficie, Blanco, self.rect, 3, border_radius=15)
        text_surf = self.font.render(self.texto, True, Blanco)
        text_rect = text_surf.get_rect(center=self.rect.center)
        superficie.blit(text_surf, text_rect)
#%%     
#Arquitectura del sistema
class Juego:
    def __init__(self):
        self.estado = "menu"
        self.boton_start = Boton_Inicio(Ancho//2 - 100, Alto//2, 200, 60, "START", Verde_Inicio, Verde_Flotante)
        self.marco_titulo = Marco(Ancho//2 - 200, Alto//4 - 40, 400, 80, "CAR ARCADE", Azul, 72)
        self.marco_instruccion1 = Marco(Ancho//2 - 300, Alto//2 + 80, 600, 50, "Flechas <-- --> para dirigir el vehiculo", Gris_Oscuro, 36)
        self.marco_instruccion2 = Marco(Ancho//2 - 250, Alto//2 + 140, 500, 50, "Evita los coches enemigos", Gris_Oscuro, 36)
        self.jugador = CochePrincipal()
        self.all_sprites = pygame.sprite.Group()
        self.coches_enemigos = pygame.sprite.Group()
        self.carretera = Carretera()
        self.all_sprites.add(self.jugador)
        self.puntuacion = 0
        self.trafico_timer = 0 
        self.velocidad_juego = 3
        self.font = pygame.font.Font(None, 36)
        self.titulo_font = pygame.font.Font(None, 72)
        
    
    def mostrar_menu(self):
        self.carretera.draw()
        self.marco_titulo.dibujar(screen)
        self.marco_instruccion1.dibujar(screen)
        self.marco_instruccion2.dibujar(screen)
        #Boton de Inicio
        self.boton_start.dibujar(screen)
        
        
    def trafico(self):
        self.trafico_timer +=1
        if self.trafico_timer >= 60:
            self.trafico_timer = 0
            numero_coches = random.randint(1, 2)
            lanes = random.sample([0, 1, 2], numero_coches)
            for lane in lanes:
                speed = random.randint(3, 6)
                coche_enemigo = CocheEnemigo(lane, speed)
                self.coches_enemigos.add(coche_enemigo)
                self.all_sprites.add(coche_enemigo)
                
    def update(self):
        if self.estado == "jugando":
            self.all_sprites.update()
            self.carretera.update()
            self.trafico()
            if pygame.sprite.spritecollide(self.jugador, self.coches_enemigos, False):
                self.estado = "game_over"
            self.puntuacion += 0.1
            if self.puntuacion % 100 == 0:
                self.velocidad_juego += 0.5
        
    def draw(self):
        screen.fill(Negro)
        
        if self.estado == "menu":
            self.mostrar_menu()
            
        elif self.estado == "jugando":
            self.carretera.draw()
            self.all_sprites.draw(screen)
            score_text = self.font.render(f"Puntuación: {int(self.puntuacion)}", True, Blanco)
            screen.blit(score_text, (10, 10))
            inst_text = self.font.render("Flechas <-- --> para cambio de carril", True, Blanco)
            screen.blit(inst_text, (Ancho//2 - inst_text.get_width()//2, Alto - 40))
        
        elif self.estado == "game_over":
            self.game_over()
        
        
    def game_over(self):
        self.carretera.draw()
        self.all_sprites.draw(screen)
        
        s= pygame.Surface((Ancho, Alto), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER",True, Rojo)
        score_text = self.font.render(f"Puntuacion Final: {int(self.puntuacion)}", True, Blanco)
        restart_text = self.font.render("Presiona R para reiniciar", True, Blanco)
        screen.blit(game_over_text, (Ancho//2 - score_text.get_width()//2, Alto//2 - 50))
        screen.blit(score_text, (Ancho//2 - restart_text.get_width()//2, Alto//2 + 20))
        screen.blit(restart_text, (Ancho//2 - restart_text.get_width()//2, Alto//2 + 60))
    
    def eventos(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.estado == "menu" and self.boton_start.posicion(event.pos):
                self.estado = "jugando"
        
        if event.type == pygame.MOUSEMOTION:
            if self.estado == "menu":
                self.boton_start.posicion(event.pos)
                
        if event.type == pygame.KEYDOWN:
            if self.estado == "game_over" and event.key == pygame.K_r:
                self.__init__()
                self.estado = "jugando"
                    
#%%
#Funcion principal
def main():
    clock = pygame.time.Clock()
    game = Juego()
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.eventos(event)
            
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
    