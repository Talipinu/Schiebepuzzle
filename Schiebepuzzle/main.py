# -*- coding: utf-8 -*-
'''
Created on 14.05.2012

@author: stefan

Die ist die Basisversion mit Minimalfunktionalität.
Hier stehen noch ausführliche Kommentare, später nur noch an den geänderten Stellen 
'''

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.locals import K_DOWN, K_RIGHT, K_LEFT, K_UP, K_SPACE, K_l
from random import randint
    
hoch, rechts, runter, links = 0, 1, 2, 3
aufloesung = 200, 200


def ringtausch(richtung, alterCursor):
    '''
    Diese Funktion tut zwei Dinge:
    - Vertauschen der Bilder
    - Cursor versetzen
    '''
    neuerCursor = alterCursor
        
    if richtung == hoch:
        if alterCursor > 3:
            neuerCursor = alterCursor - 4
    elif richtung == rechts:
        if alterCursor%4 != 3:
            neuerCursor = alterCursor + 1
    elif richtung == runter:
        if alterCursor < 12:
            neuerCursor = alterCursor + 4
    elif richtung == links:
        if alterCursor%4:
            neuerCursor = alterCursor - 1
            
    tEintrag = einzelBilder[alterCursor]
    einzelBilder[alterCursor] = einzelBilder[neuerCursor]
    einzelBilder[neuerCursor] = tEintrag

    return neuerCursor

if __name__ == '__main__':
    # Logdatei anlegen (eigentlich unnötig, nur als Programmierhilfe)
    logdatei = open("logdatei", "w")

    '''
    Vorbereitungen
    '''
    # Fenster einrichten
    pygame.init()
    schirm = pygame.display.set_mode(aufloesung)
    pygame.display.set_caption("Bilderschieber")
 
    tBild = pygame.image.load("pics/meer.png")
    ganzesBild = pygame.transform.scale(tBild, aufloesung).convert()
        
    # Dictionary ( siehe http://tutorial.pocoo.org/datastructures.html#dictionaries)
    # für Einzelbilder vorbereiten
    einzelBilder = {}
    breite, hoehe = int(ganzesBild.get_width()/4), int(ganzesBild.get_height()/4)
    n = 0
    
    '''
    Achtung! Das Dictionary wurde geändert!
    Nun wird neben dem Einzelbild auch seine ursprüngliche Position gespeichert.   
    
    'einzelBilder' sieht zu Beginn jetzt so aus: {0: (Bild0, 0), 1: (Bild1, 1),  2: (Bild2, 2), ...}
    Nachdem es durchgemischt wurde, es es jetzt z.B. so aus: {0: (Bild3, 3), 1: (Bild12, 12), 2: (Bild7, 7), ...}
    
    Anwendungsbeispiele:
        Eingabe                Ausgabe
    
    einzelBilder[2]        (Bild8, 8)
    einzelbilder[2][0]     Bild8
    einzelbilder[2][1]     8
    einzelbilder.keys()    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    einzelbilder.values()  (Bild3, 3), (Bild12, 12), (Bild7, 7), <...>
    einzelbilder.items()   {0: (Bild3, 3), 1: (Bild12, 12), 2: (Bild7, 7), <...>}
    '''        
    # Ganzes Bild in 16 Teile schneiden und diese im Dictionary ablegen
    for j in range(4):
        for i in range(4):
            einzelBilder[n] = (ganzesBild.subsurface(i*breite, j*hoehe, breite, hoehe), n)
            n += 1
            
    # Bild des weißen Kastens laden, Einzelbild rechts unten dadurch ersetzen
    weisserKasten = pygame.image.load("pics/weißerKasten.png").convert()
    # weisserKasten = pygame.image.load("weisserKasten.png").convert()
    einzelBilder[15] = (weisserKasten, 15) 
        
    # Einige Variablen initialisieren
    hauptschleifeAktiv = True
    updateZeit = 0
    cursor = 15
    updateZaehler = 0
    
    # Die logdatei ist nur für euch Programmierer gedacht.
    # Schreibt wie in der nächsten Zeile in diese Datei, um euch ein Objekt anzeigen zu lassen.
    # Der 'write'-Befehl akzeptiert nur strings (Zeichenketten), daher notfalls mit <str(...)> umwandeln!
    #
    # "\n" fängt eine neue Zeile an.  
    logdatei.write(str(einzelBilder.items()) + "\n")
    
    '''
    Hauptschleife
    '''
    while hauptschleifeAktiv:
        # Benutzereingaben abfragen
        for e in pygame.event.get():
            
            # Alle Tastaturcodes unter http://www.pygame.org/docs/ref/key.html
            if e.type == QUIT:
                hauptschleifeAktiv = False
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    cursor = ringtausch(hoch, cursor)
                elif e.key == K_RIGHT:
                    cursor = ringtausch(rechts, cursor)
                elif e.key == K_DOWN:
                    cursor = ringtausch(runter, cursor)
                elif e.key == K_LEFT:
                    cursor = ringtausch(links, cursor)
                elif e.key == K_SPACE:
                    for i in range(100):
                        cursor = ringtausch(randint(0, 4), cursor)
                elif e.key == K_ESCAPE:
                    hauptschleifeAktiv = False

        # Bremse (für feste Aktualisierungsrate) 
        t = pygame.time.get_ticks()
        if t - updateZeit > 25:
            updateZeit = t
            updateZaehler += 1
    
            # Einzelbilder einzeln auf den Schirm malen
            for k, v in einzelBilder.items():
                i = k%4
                j = int(k/4)
                schirm.blit(v[0], (i*breite, j*hoehe))
                        
        # Bildschirm neu zeichnen
        pygame.display.update()

    # Beenden
    logdatei.close()
    pygame.quit()
    sys.exit()