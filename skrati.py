import pygame
import random

pygame.init()
width = 600
height = 600
# Color definition
background = (13, 33, 106)
separator = (132, 142, 179)
notes = "C C# D D# E F F# G G# A A# H B".split(" ")
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Glasbeni škrati")
clock = pygame.time.Clock()

# Slika škrata
skratImg = pygame.image.load("skrat.png")
skratImg = pygame.transform.scale(skratImg, (40, 40))

def skrat(x, y):
    gameDisplay.blit(skratImg, (x, y))

def createNewSkrat():
    idx = random.randrange(0, len(notes))
    note = notes[idx]
    x = idx * (width / len(notes)) + 7
    y = -50
    return [x, y]

def drawNotes():
    font = pygame.font.Font("bahnschrift.ttf", 32)
    for idx in range(len(notes)):
        note = notes[idx]
        textSurface = font.render(note, True, (255,255,255))
        textRect = textSurface.get_rect()
        textRect.center = (idx * (width / len(notes)) + 25, height - 25)
        pygame.draw.rect(gameDisplay, separator, [idx * (width / len(notes)) + 50, 0, 1, height])
        gameDisplay.blit(textSurface, textRect)
    pygame.display.update()

def game():
    yChange = 3
    generationCounter = 0
    targets = [createNewSkrat()]
    endGame = False
    while not endGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame = True
            if event.type == pygame.KEYUP:
                targets = targets[1:]
                print("Hit detected")
        gameDisplay.fill(background)
        for target in targets:
            target[1] += yChange
            if target[1] > height:
                target[1] = 0
            skrat(target[0], target[1])
        drawNotes()
        pygame.display.update()
        clock.tick(30)
        generationCounter += 1
        if generationCounter == 60:
            targets.append(createNewSkrat())
            generationCounter = 0

game()
pygame.quit()
quit()
