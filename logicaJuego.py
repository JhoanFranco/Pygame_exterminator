import random
import pygame as pg
import time 
import sys
# # importacion de clases creadas para el juego 
from claseMuro import Muro, MuroExplosivo
from claseBarraVida import BarraVida
from claseJugador import Jugador
from  claseEnemigo import Enemigos_morado, Enemigos_verdes
from claseCajasEspeciales import CajasEspeciales

from claseTeclado import TecladoExterminador1, TecladoExterminador2

from claseCronometro import Cronometro
from claseControladorSonido import ControladorSonido

from clasePuntuacion import Puntuacion

# Tamaño pantalla
from mainVariables import ANCHO, ALTO
# FPS
from mainVariables import FPS
# PALETA DE COLORES RGB()
from mainVariables import NEGRO, BLANCO, ROJO, AZUL,VERDE

# imagenes para el juego
fondo = pg.transform.scale(pg.image.load("imagenes/fondos/fondo_cuidad_final.png"), (ANCHO,ALTO))



# Pantalla y clock 
from mainVariables import pantalla
from mainVariables import clock
# es volumen nulo 
from mainVariables import es_volumen_nulo
# controlador de sonifo
from mainVariables import controladorSonido



# el metodo update se llama por  los grupos (Group.update())
# GRUPOS DE SPRITES
sprites_jugador = None
sprites_enemigos = None
sprites_enemigos_verdes = None
sprites_enemigos_morados = None
sprites_balas = None
sprites_balas_grandes = None
sprites_muros = None
sprites_barra_vida = None
sprites_cajas_especiales = None
sprites_muros_explosivos = None

# Crear objetos y añadirlos al grupo de sprite
jugador1 = None
jugador2 = None
barra_v = None

# muros contenedores horizontales
y = None
x = None

# Contador de puntuacion
contador_muerte_enemigos = None
puntuacion = None

# contador para el numero de enemigos
contador_poner_enemigos = None

def numeroJugador(jugador:Jugador):
    if jugador.bool_esJugadorDos == False:
        return(1)
    else:
        return(2)

def iniciarJuego(numeroJugadores):
    # INICIALIZAR LAS VARIABLES PARA EL FUNCIONAMIENTO DEL JUEGO 
    # Pantalla y clock , es volumen nulo  
    global pantalla
    global clock
    global es_volumen_nulo 

    # el metodo update se llama por  los grupos (Group.update())
    # GRUPOS DE SPRITES
    global sprites_jugador
    global sprites_enemigos
    global sprites_enemigos_verdes
    global sprites_enemigos_morados
    global sprites_balas
    global sprites_balas_grandes
    global sprites_muros
    global sprites_barra_vida
    global sprites_cajas_especiales
    global sprites_muros_explosivos

    # Crear objetos y añadirlos al grupo de sprite
    global jugador1
    global jugador2
    global barra_v

    # muros contenedores horizontales
    global y
    global x

    # Contador de puntuacion
    global contador_muerte_enemigos
    global puntuacion

    # contador para el numero de enemigos
    global contador_poner_enemigos

    # controlador de sonido
    global controladorSonido

        
    # Incializar pygame
    pg.init()

    pg.display.set_caption("JUEGO EXTERMINADOR")

    # MUSICA poner en bucle el fondo del juego 
    pg.mixer.music.load("musica/musica_fondo.mp3")# cargar musica python
    # reproducir la musica infinitamente
    pg.mixer.music.play(-1) 

    #icono
    icono = pg.image.load("imagenes\zombies\zombies_morado_der_2.png")
    icono = pg.transform.scale(icono,(20,20))
    pg.display.set_icon(icono)
    # el metodo update se llama por  los grupos (Group.update())
    # GRUPOS DE SPRITES
    sprites_jugador = pg.sprite.Group()
    sprites_enemigos = pg.sprite.Group()
    sprites_enemigos_verdes = pg.sprite.Group()
    sprites_enemigos_morados = pg.sprite.Group()
    sprites_balas = pg.sprite.Group()
    sprites_balas_grandes = pg.sprite.Group()
    sprites_muros = pg.sprite.Group()
    sprites_barra_vida = pg.sprite.Group()
    sprites_cajas_especiales = pg.sprite.Group()
    sprites_muros_explosivos = pg.sprite.Group()

    # Crear objetos y añadirlos al grupo de sprite jugador, teclado, barravida 
    tecladoJuador1 = TecladoExterminador1()
    tecladoJuador2 = TecladoExterminador2()

    jugador1 = Jugador(contadorMunicion_DisparoGrande= 5, contadorMunicion_BarrilExplota= 5 , contadorMunicion_Muros=5, teclado=tecladoJuador1)
    jugador2 = Jugador(contadorMunicion_DisparoGrande= 5, contadorMunicion_BarrilExplota= 5 , contadorMunicion_Muros=5, teclado=tecladoJuador2, esJugadorDos=True)
    
    barra_vidaJugador1 = BarraVida(1)
    barra_vidaJugador2 = BarraVida(2)

    # Añadir los objeto a los grupos de sprites dependiendo de los jugadores
    if(numeroJugadores == 1):
        sprites_jugador.add(jugador1) 
        sprites_barra_vida.add(barra_vidaJugador1)
    else:
        sprites_jugador.add(jugador2, jugador1) 
        sprites_barra_vida.add(barra_vidaJugador1, barra_vidaJugador2)

    # Puntuacion 
    puntuacion = Puntuacion()

    ## Poner muros en el mapa
    # muros contenederes verticales
    y = 40
    x = 730
    for i in range(7):
        y += 20
        if i == 3:
            y += 20
            muro = Muro(x, y)
            sprites_muros.add(muro)
        else:
            muro = Muro(x, y)
            sprites_muros.add(muro)

    # muros contenedores horizontales
    y = 280
    x = 760

    for i in range(5):
        x += 40
        muro = Muro(x, y)
        sprites_muros.add(muro)

    # numero de muertos por enemigo 
    contador_muerte_enemigos = 0
    # poner la puntuacion en 0 
    puntuacion.puntuacion = 0

    # contador para el numero de enemigos
    contador_poner_enemigos = 6

    # creacion de cronometro
    cronometro = Cronometro()
    cronometro.iniciar()

    # muerte de jugador
    boolMuerteJugador1 =  False
    boolMuerteJugador2 =  False

    # termino juego 
    terminoJuego = False
    # frames al terminar el juego 
    framesAlTerminarJuego = 0
    
    #BUCLE DEL JUEGO         
    while True:

        clock.tick(FPS) # velociade de bucle

        # PARA SABER CUANDO TERMINAR EL BUCLE
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            ## PARA COLOCAR PUNTUACION CUANDO TERMINA EL JUEGO 
            if terminoJuego:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN: # si toca la telca enter
                        print("Texto ingresado:", puntuacion.textoIngresadoUsuario)
                        ## PROCESAR UNA NUEVA PUNTUACION
                        puntuacion.procesarUnaNuevaPuntuacion( puntuacion.textoIngresadoUsuario, numeroJugadores, puntuacion.puntuacion, "NoDef")
                        puntuacion.textoIngresadoUsuario = ''
                        pg.mixer.music.stop()
                        pg.mixer.music.load("musica/Music Ever_ Everything Ends Here.mp3")# cargar musica python
                        # reproducir la musica infinitamente
                        pg.mixer.music.play(-1)
                        return("Termino Juego1")
                    elif event.key == pg.K_BACKSPACE: # si toca la tecla de borrar
                        puntuacion.textoIngresadoUsuario = puntuacion.textoIngresadoUsuario[:-1]
                    elif len(puntuacion.textoIngresadoUsuario) < puntuacion.MAX_LETTERS: # sino entonces agregar esa entrada a la var  self.textoIngresadoUsuario
                        puntuacion.textoIngresadoUsuario += event.unicode

                # Renderizar texto ingresado en la pantalla
                font = pg.font.SysFont("Chiller", 70) # crear fuente
                puntuacion.superficieTexto = font.render(puntuacion.textoIngresadoUsuario, True, NEGRO)
                
                # Renderizar guión debajo del texto
                remaining_letters = puntuacion.MAX_LETTERS - len(puntuacion.textoIngresadoUsuario)
                if remaining_letters >= 0:
                    underscore_text = '-' * remaining_letters
                    puntuacion.superficieLineas = font.render(underscore_text, True, NEGRO)
                    # pantalla.blit(puntuacion.superficieLineas, (ANCHO/2, 40))
                


        # OBTENER EL TIEMPO DEL CRONOMETRO
        minutos, segundos, tiempo_milisegundo = cronometro.obtener_tiempo_formateado()
        tiempo_milisegundo = int(tiempo_milisegundo/100)
        # print(minutos)

        
        # CREAR ENEMIGOS CON EL TIEMPO
        if ((segundos == 2 and tiempo_milisegundo < 1) and minutos == 0) or (segundos == 30 and tiempo_milisegundo < 1) or (segundos == 59 and tiempo_milisegundo < 1):
            for i in range(contador_poner_enemigos):
                # Crear objetos de enemigos y añadirlos 
                enemigo_verde = Enemigos_verdes()
                enemigo_morado = Enemigos_morado()
                sprites_enemigos_verdes.add(enemigo_verde)
                sprites_enemigos_morados.add(enemigo_morado)
                sprites_enemigos.add(enemigo_verde)
                sprites_enemigos.add(enemigo_morado)

            contador_poner_enemigos += 2
            time.sleep(1)
    

        # ACTUALIZACION DE SPRITES
            # actualizacion de jugadore 
        if numeroJugadores == 1:
            jugador1.update(jugador1, sprites_balas_grandes, sprites_balas, sprites_muros, sprites_muros_explosivos) # actualizar el sprite jugador1
        else:
            jugador1.update(jugador1, sprites_balas_grandes, sprites_balas, sprites_muros, sprites_muros_explosivos) # actualizar el sprite jugador1
            jugador2.update(jugador2, sprites_balas_grandes, sprites_balas, sprites_muros, sprites_muros_explosivos) # actualizar el sprite jugador1
        sprites_enemigos.update()   # sin argumentos adicionales
        sprites_balas.update()      # sin argumentos adicionales
        sprites_barra_vida.update() # sin argumentos adicionales
        sprites_balas_grandes.update() # sin argumentos adicionales
        sprites_muros.update()      # sin argumentos adicionales
 
        # COLISIONES
        # Ojo para que sean mas precisas se necesita un radio no rectangulo. 
        # colisionSoloUno = pg.sprite.spritecollide(jugador,sprites_enemigos,False,pg.sprite.collide_circle) 
        # colisionesVarios =  pg.sprite.groupcollide(sprites_balas,sprites_enemigos,True,False,) # de esos dos grupos de sprites elimina el segundo


        # COLICION de los enemigos con las balas pequeñas
        for sprite_enemigo in sprites_enemigos:
            colision_balas_enemigo = pg.sprite.spritecollide(sprite_enemigo,sprites_balas,False,pg.sprite.collide_circle)
            if colision_balas_enemigo:
                # ya que sabemos que hubo colicion de un enemigo con alguna bala entonces borramos esa bala
                colision_balas_enemigo = pg.sprite.spritecollide(sprite_enemigo,sprites_balas,True,pg.sprite.collide_circle)
                sprite_enemigo.quitarVida(1) # se le quita vida 

                if sprite_enemigo.vidaEnemigo <= 0:
                    # poner puntos a la puntuacion
                    contador_muerte_enemigos += 1
                    puntuacion.sumarPuntuacion(20) 

        # COLICION balas Grandes con los enemigos
        for sprite_balaGrande in sprites_balas_grandes:
            i = 0
            j = 0
            for sprite_enemigo in sprites_enemigos:
                j += 1
                i += 1 
                comparacion_x = sprite_balaGrande.rect.x  - sprite_enemigo.rect.x
                comparacion_y = sprite_balaGrande.rect.y  - sprite_enemigo.rect.y
                # print(f"la bala grande  {i}: { sprite_balaGrande.rect.x }, {sprite_balaGrande.rect.y}")
                # print(f"el enemigo   {j}: {  sprite_enemigo.rect.x }, {sprite_enemigo.rect.y}")
                # print(comparacion_x)
                # print(comparacion_y)
                if ((comparacion_y >= -30) and (comparacion_y <= 30)) and ((comparacion_x >= -30) and (comparacion_x <= 30)):
                    sprite_enemigo.kill()
                    #poner puntuacion
                    contador_muerte_enemigos += 1
                    puntuacion.sumarPuntuacion(20) 
                else:
                    pass
            
        # COLICION de la bala pequeña con el muro
        for sprite_muro in sprites_muros:
            colision_balas_muros =  pg.sprite.spritecollide(sprite_muro, sprites_balas,False,pg.sprite.collide_circle)
            if colision_balas_muros:
                sprite_muro.golpeMuro(1)
                if sprite_muro.contadorDeVidaMuro <= 0:
                    sprite_muro.update()    # si es <= 0 lo elimina
                    puntuacion.sumarPuntuacion(3)          # poner puntuacion
        
        # COLICION de la bala grande con el muro
        for sprite_muro in sprites_muros:
            colision_balasGrandes_muro =  pg.sprite.spritecollide(sprite_muro,sprites_balas_grandes,False,pg.sprite.collide_circle)
            if colision_balasGrandes_muro:
                sprite_muro.golpeMuro(45)
                if sprite_muro.contadorDeVidaMuro <= 0:
                    sprite_muro.update()    # si es <= 0 lo elimina
                    puntuacion.sumarPuntuacion(3)          # poner puntuacion    



        # # COLICION de los enemigo (zombie verde) con el muro 
        # # COLICION de los  enemigo (zombie verde) con el muro - retroceder al enemigo (zombie verde
        for sprite_muro in sprites_muros:
            for sprite_enemigoVerde in sprites_enemigos_verdes:
                # vamos a ver si el muro tiene colicion con algun enemigo 
                if pg.sprite.collide_circle(sprite_muro,sprite_enemigoVerde):   
                    sprite_muro.golpeMuro(1)
                    # mover el zombie
                    sprite_enemigoVerde.rect.x += -4
                    sprite_enemigoVerde.rect.y += -4
                    # si el muro se quedo sin vida
                    if sprite_muro.contadorDeVidaMuro <= 0:
                        sprite_muro.update()    # si es <= 0 lo elimina
                        puntuacion.sumarPuntuacion(3)         # poner la puntuacion   


        # COLICION del enemigo (zombie morado) con el muro
        # COLICION del enemigo (zombie morado) con el muro - retroceder al enemigo (zombie morado)   
        for sprite_muro in sprites_muros:
            for sprite_enemigoMorado in sprites_enemigos_morados:
                # vamos a ver si el muro tiene colicion con algun enemigo 
                if pg.sprite.collide_circle(sprite_muro,sprite_enemigoMorado):   
                    sprite_muro.golpeMuro(2)
                    # mover el zombie morado
                    sprite_enemigoMorado.rect.x += +5
                    sprite_enemigoMorado.rect.y += +6 # va a ir escalando un poco
                    # si el muro se quedo sin vida
                    if sprite_muro.contadorDeVidaMuro <= 0:
                        sprite_muro.update()    # si es <= 0 lo elimina
                        puntuacion.sumarPuntuacion(3)         # poner la puntuacion   



        # COLICION de los JUGADORES con los enemigos
        #
        for jugadorX in sprites_jugador:
            colision_jugador_enemigos = pg.sprite.spritecollide(jugadorX, sprites_enemigos, False,pg.sprite.collide_circle)
            if colision_jugador_enemigos:
                jugadorX.quitarVida(1)
                jugadorX.activarMusica_dolorjugador() # poner musica en la clase
                # BARRA VIDA
                if jugadorX.bool_esJugadorDos  != True:
                    barra_vidaJugador1.quitarVida(1)
                else:
                    barra_vidaJugador2.quitarVida(1)

                # SI UNO DE LOS JUGADORES NO TIENE VIDA
                if jugadorX.vidaJuagador <= 0:
                    # ver si es el 1 o 2
                    if jugadorX.bool_esJugadorDos  != True:
                        print("perdio jugador 1 ")
                        boolMuerteJugador1 = True
                        jugadorX.BorrarSprite()
                    else:
                        print("perdio jugador 2 ")
                        boolMuerteJugador2 = True
                        jugadorX.BorrarSprite()
                    

        # CAMBIAR SPRITE
        # Cuando un zombie verde nos muerde
        for sprite_enemigo_verde in sprites_enemigos_verdes:
            colicion_enemigoVerde_jugadores = pg.sprite.spritecollide(sprite_enemigo_verde, sprites_jugador, False,pg.sprite.collide_circle)
            if colicion_enemigoVerde_jugadores: # si hay colicion de los enemigos verdes con el jugador
                # cambiando ese estado se cambia de sprite y tambien se coloca sonido de mordida
                sprite_enemigo_verde.cambiarEstadoEstarMordiendo(True) 

        # CAMBIAR SPRITE
        # Cuando un zombie morado nos muerde
        for sprite_enemigo_morado in sprites_enemigos_morados:
            colicion_enemigoMorado_jugadores = pg.sprite.spritecollide(sprite_enemigo_morado, sprites_jugador, False,pg.sprite.collide_circle)
            if colicion_enemigoMorado_jugadores:
                # cambiando ese estado se cambia de sprite y tambien se coloca sonido de mordida
                sprite_enemigo_morado.cambiarEstadoEstarMordiendo(True) 


        # COLICION de barriles explosivos con los ENEMIGOS VERDES (lo escala un poco)
        for sprite_enemigoVerde in sprites_enemigos_verdes:
            # si el enemigo tiene colicion con alguno de los muros
            colicion_enemigoVerde_murosExplosivos = pg.sprite.spritecollide(sprite_enemigoVerde,sprites_muros_explosivos,False,pg.sprite.collide_circle)
            if colicion_enemigoVerde_murosExplosivos:      
                sprite_enemigoVerde.rect.x += -5
                sprite_enemigoVerde.rect.y += -8 # se va ir un poco hacia arriba lo va a escalar

        # COLICION de barriles explosivos con los ENEMIGOS MORADOS (lo escala mucho)
        for sprite_enemigoMorado in sprites_enemigos_morados:
            # vamos a ver si el enemigo tiene colicion con alguno de los muros
            colicion_enemigoMorado_murosExplosivos = pg.sprite.spritecollide(sprite_enemigoMorado,sprites_muros_explosivos,False,pg.sprite.collide_circle)
            if colicion_enemigoMorado_murosExplosivos:      
                sprite_enemigoMorado.rect.x += 30
                sprite_enemigoMorado.rect.y += 10

        # COLICION barril_explosivo con la bala
        for sprite_muroExplosivo in sprites_muros_explosivos:
            colicion_muroExplosivo_balas = pg.sprite.spritecollide(sprite_muroExplosivo,sprites_balas,False,pg.sprite.collide_circle)
            if colicion_muroExplosivo_balas:
                # al actualizar se borran los sprites enemigos que tocan la explosion 
                sprite_muroExplosivo.update(pantalla, sprites_muros_explosivos, sprites_enemigos, es_volumen_nulo=False)
                pg.display.flip() # actualizamos pantalla
                time.sleep(0.5) # paramos un momento el juego 1/2 segundo
                sprite_muroExplosivo.kill()
                puntuacion.sumarPuntuacion(15)

        # COLICION barril_explosivo con la bala grande
        for sprite_muroExplosivo in sprites_muros_explosivos:
            colicion_muroExplosivo_balasGrandes = pg.sprite.spritecollide(sprite_muroExplosivo,sprites_balas_grandes,False,pg.sprite.collide_circle)
            if colicion_muroExplosivo_balasGrandes:
                # al actualizar se borran los sprites enemigos que tocan la explosion 
                sprite_muroExplosivo.update(pantalla, sprites_muros_explosivos, sprites_enemigos, es_volumen_nulo=False)
                pg.display.flip() # actualizamos pantalla
                time.sleep(0.5) # paramos un momento el juego 1/2 segundo
                sprite_muroExplosivo.kill()
                puntuacion.sumarPuntuacion(15)

        # DIBUJAR el fondo de la pantalla
        # Tiene que ser en el bucle porque si no quedan las imagenes represadas
        pantalla.blit(fondo,(0,0)) # imagen, (0,0) no margenes

        # DIBUJAR los grupos de sprites
        sprites_jugador.draw(pantalla) 
        sprites_enemigos.draw(pantalla)
        sprites_balas.draw(pantalla) 
        sprites_muros.draw(pantalla)
        sprites_barra_vida.draw(pantalla)
        sprites_muros_explosivos.draw(pantalla)
        sprites_balas_grandes.draw(pantalla)
        
        
        # CAJAS ESPECIALES (entres segundos 10 y 20)
        if segundos >= 10 and segundos < 20: 
            if segundos == 10 and tiempo_milisegundo < 1:
                caja_esp1 = CajasEspeciales(1) # como es caja de disparo grande sprite(1)
                caja_esp2 = CajasEspeciales(2) # como es caja de muros sprite(2)
                caja_esp1.cambiarPosicionRandom()
                caja_esp2.cambiarPosicionRandom()
                sprites_cajas_especiales.add(caja_esp1, caja_esp2)
                
            else:
                # dibujar las cajas 
                sprites_cajas_especiales.draw(pantalla)
                
                for caja_espx in sprites_cajas_especiales:
                    for jugadorx in sprites_jugador:
                        colicionJugador_cajaEsp = pg.sprite.collide_circle(jugadorx, caja_espx)
                        if colicionJugador_cajaEsp:
                            numeroCaja = caja_espx.numeroCaja
                            cantidadMunicionAumentar = (minutos*2) + 3
                            # aumentar la municion del jugador
                            jugadorx.AumentarMunicionEspecial(numeroCaja, cantidadMunicionAumentar)
                            # borrar la caja 
                            caja_espx.eliminarCaja()     
        # si el tiempo se paso borrar las cajas 
        if segundos == 20 and tiempo_milisegundo < 1:
            sprites_cajas_especiales.empty()
            # for caja_espx in sprites_cajas_especiales:
            #     caja_espx.eliminarCaja()
               
        # CAJAS ESPECIALES (entre segundos 35 y 40)
        if segundos >= 35 and segundos < 40: 
            if segundos == 35 and tiempo_milisegundo < 1:
                caja_esp1 = CajasEspeciales(0) # como es caja de barriles explosivos(0)
                caja_esp2 = CajasEspeciales(2) # como es caja de muros sprite(2)
                caja_esp1.cambiarPosicionRandom()
                caja_esp2.cambiarPosicionRandom()
                sprites_cajas_especiales.add(caja_esp1, caja_esp2)
                
            else:
                # dibujar las cajas 
                sprites_cajas_especiales.draw(pantalla)
                
                for caja_espx in sprites_cajas_especiales:
                    for jugadorx in sprites_jugador:
                        colicionJugador_cajaEsp = pg.sprite.collide_circle(jugadorx, caja_espx)
                        if colicionJugador_cajaEsp:
                            numeroCaja = caja_espx.numeroCaja
                            cantidadMunicionAumentar = (minutos*2) + 5
                            # aumentar la municion del jugador
                            jugadorx.AumentarMunicionEspecial(numeroCaja, cantidadMunicionAumentar)
                            # borrar la caja 
                            caja_espx.eliminarCaja()   
        # si el tiempo se paso borrar las cajas 
        if segundos == 40 and tiempo_milisegundo < 1:
            sprites_cajas_especiales.empty() # eliminar sprites

         
     # CAJAS ESPECIALES (entre segundos 56 y 58)
        if segundos >= 54 and segundos < 59: 
            if segundos == 54 and tiempo_milisegundo < 1:
                caja_esp1 = CajasEspeciales(1) # como es caja de barriles explosivos(1)
                caja_esp2 = CajasEspeciales(2) # como es caja de muros sprite(2)
                caja_esp1.cambiarPosicionRandom()
                caja_esp2.cambiarPosicionRandom()
                sprites_cajas_especiales.add(caja_esp1, caja_esp2)
                
            else:
                # dibujar las cajas 
                sprites_cajas_especiales.draw(pantalla)
                
                for caja_espx in sprites_cajas_especiales:
                    for jugadorx in sprites_jugador:
                        colicionJugador_cajaEsp = pg.sprite.collide_circle(jugadorx, caja_espx)
                        if colicionJugador_cajaEsp:
                            numeroCaja = caja_espx.numeroCaja
                            cantidadMunicionAumentar = (minutos*3) + 3
                            # aumentar la municion del jugador
                            jugadorx.AumentarMunicionEspecial(numeroCaja, cantidadMunicionAumentar)
                            # borrar la caja 
                            caja_espx.eliminarCaja()
                    
                # si el tiempo se paso borrar las cajas 
        if segundos == 59 and tiempo_milisegundo < 1:
            sprites_cajas_especiales.empty() # eliminar sprites
                
        
        # caja especial de vida y revivir
        if segundos >= 30 and segundos < 40 : 
            if segundos == 30 and tiempo_milisegundo < 1:
                caja_esp1 = CajasEspeciales(3) # como es caja de vida
                ## caja_esp1.cambiarPosicionRandom()
                sprites_cajas_especiales.add(caja_esp1)
            else:
                # dibujar las cajas 
                sprites_cajas_especiales.draw(pantalla)
        
                for caja_espx in sprites_cajas_especiales:
                    for jugadorx in sprites_jugador:
                        colicionJugador_cajaEsp = pg.sprite.collide_circle(jugadorx, caja_espx)
                        if colicionJugador_cajaEsp:
                            numeroCaja = caja_espx.numeroCaja
                            cantidadVidaAumentar = (minutos*5) + 20 
                            # aumentar la municion del jugador
                            jugadorx.AumentarMunicionEspecial(numeroCaja, cantidadVidaAumentar)
                            # borrar la caja 
                            caja_espx.eliminarCaja()
                            # Cambiar el contador a la Barra de vida
                            for barraVidax in sprites_barra_vida:
                                if barraVidax.barraVida_Numerojugador == numeroJugador(jugadorx):
                                    barraVidax.aumentarVida(cantidadVidaAumentar) 
        # si el tiempo se paso borrar las cajas 
        if segundos == 40 and tiempo_milisegundo < 1:
            sprites_cajas_especiales.empty() # eliminar sprites
            
        # SONIDO Y CONTROLADOR DE SONIDO
        #Ojo: solo para la musica en bucle(FONDO DEL JUEGO)
        
        controladorSonido.update(pantalla) # mira si se presionaron las teclas de controlador de sonifo 

        #Poner si el volumen es nulo 
        #print(es_volumen_nulo)
        
        imagenes_disparosGrandes =[ 
            pg.image.load("imagenes/disparo_grande/disparo_grande_derecha.png"),
            pg.image.load("imagenes/disparo_grande/disparo_grande_izquierda.png"),
            pg.image.load("imagenes/disparo_grande/disparo_grande_arriba.png"),
            pg.image.load("imagenes/disparo_grande/disparo_grande_abajo.png")
        ]

        imagenes_cajasEspeciales = [
            pg.image.load("imagenes/cajasEspeciales/caja_barril_explota.png"),
            pg.image.load("imagenes/cajasEspeciales/caja_disparo_grande.png"),
            pg.image.load("imagenes/cajasEspeciales/muro_blanco.png")
        ]

    # imprimir en la pantalla el cronometro
        pg.font.init()
        font = pg.font.SysFont("Chiller", 35) # crear fuente
        fuente = pg.font.Font(None,30)  # otra forma de crear fuente
        texto = font.render(f'Tiempo <{minutos}:{segundos}>', 1, NEGRO) # imprimir el
        pantalla.blit(texto, (ANCHO -170, 0))

        # imprimir la puntuacion
        texto = font.render(f" SCORE: 0{puntuacion.puntuacion}",1,BLANCO)
        pantalla.blit(texto, (0, 20))


        # imprimir el nombre del jugador 1
        font = pg.font.SysFont("Chiller", 25)
        texto = font.render(f" JUGADOR 1",1,NEGRO)
        pantalla.blit(texto, (ANCHO -100, 30))

        if numeroJugadores >= 2:
            # imprimir el nombre del jugador 2
            font = pg.font.SysFont("Chiller", 25)
            texto = font.render(f" JUGADOR 2",1,NEGRO)
            pantalla.blit(texto, (ANCHO -100, 150))

        for jugadorx in sprites_jugador:

            if jugadorx.bool_esJugadorDos == False :    
                #imprimir por pantalla a los atributos(balas, poderes, especiales, muros, etc)´
                font = pg.font.SysFont("Chiller", 20)
                pantalla.blit(pg.transform.scale(imagenes_disparosGrandes[1],(20,20)), (ANCHO-80, 90 ))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_balas_disparoGrande}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 90))

                pantalla.blit(pg.transform.scale(imagenes_cajasEspeciales[0],(20,20)), (ANCHO-80, 110))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_barril_explota}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 110))

                pantalla.blit(pg.transform.scale(imagenes_cajasEspeciales[2],(20,20)), (ANCHO-80, 130))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_muros}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 130))
            else:
                AltodeMas = 125
                #imprimir por pantalla a los atributos(balas, poderes, especiales, muros, etc)´
                font = pg.font.SysFont("Chiller", 20)
                pantalla.blit(pg.transform.scale(imagenes_disparosGrandes[1],(20,20)), (ANCHO-80, 90 + AltodeMas))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_balas_disparoGrande}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 90 +AltodeMas ))

                pantalla.blit(pg.transform.scale(imagenes_cajasEspeciales[0],(20,20)), (ANCHO-80, 110 +AltodeMas))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_barril_explota}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 110+AltodeMas))

                pantalla.blit(pg.transform.scale(imagenes_cajasEspeciales[2],(20,20)), (ANCHO-80, 130 +AltodeMas))
                texto=  font.render(f'X {jugadorx.contadorMunicionExterminador_muros}', 1, NEGRO)
                pantalla.blit(texto, (ANCHO -50, 130+AltodeMas))

        # Cuando ya a muerto el jugador
        if boolMuerteJugador1:
            font = pg.font.SysFont("Chiller", 20)
            texto=  font.render("MURIO", 1, NEGRO)
            pantalla.blit(texto, (ANCHO -60, 90))
        if boolMuerteJugador2:
            font = pg.font.SysFont("Chiller", 20)
            texto=  font.render("MURIO", 1, NEGRO)
            pantalla.blit(texto, (ANCHO -60, 90+125))
            
        # cuando ya los dos jugadores estan muertos 
        if numeroJugadores == 1 and boolMuerteJugador1:
            font = pg.font.SysFont("Chiller", 150)
            texto=  font.render("PERDIO", 1, NEGRO)
            pantalla.blit(texto, (ANCHO/2 -200, ALTO/2 -100))
            if framesAlTerminarJuego == 0:
                terminoJuego = True
            framesAlTerminarJuego += 1
            # print(segundos)
        elif boolMuerteJugador1 and boolMuerteJugador2 and numeroJugadores >= 2:
            font = pg.font.SysFont("Chiller", 150)
            texto=  font.render("PERDIERON", 1, NEGRO)
            pantalla.blit(texto, (ANCHO/2 -200, ALTO/2 -100))
            if framesAlTerminarJuego == 0:
                terminoJuego = True
            framesAlTerminarJuego += 1
            # print(segundos)


        if (boolMuerteJugador1 and terminoJuego and framesAlTerminarJuego ==1 and numeroJugadores == 1):
            print("iniciar cronometro")
            cronometro.reiniciar()
            cronometro.iniciar()
            sprites_jugador.empty()
        elif (boolMuerteJugador1 and boolMuerteJugador2 and terminoJuego and framesAlTerminarJuego== 1 and numeroJugadores >= 2):
            print("iniciar cronometro")
            cronometro.reiniciar()
            cronometro.iniciar()
            sprites_jugador.empty()

                
        if terminoJuego:
            puntuacion.imprimirEnPantalla(pantalla)
        
        #actualizar conteniddo de pantalla
        pg.display.flip()

#iniciarJuego(2)

