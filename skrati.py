import pygame
import random
import noteDetector
import threading
import queue

class Skrat:
    def __init__(self, xTop, yTop, xBot, yBot, midiNo):
        self.xTop = xTop
        self.yTop = yTop
        self.xBot = xBot
        self.yBot = yBot
        self.midiNo = midiNo

    def move(self):
        self.xTop -= 1


pygame.init()
width = 600
height = 600
# Color definition
background = (13, 33, 106)
separator = (132, 142, 179)
stringColor = (75, 75, 75)
#notes = "C C# D D# E F F# G G# A A# H B".split(" ")
notes = "C C# D D# E F F# G G# A A# B".split(" ")
# Location of each note, formatted as [string number, fret number]
# Where high E string is numbered as 1 and low E as 6
# Max fret number is 20
fretboardNotes = {
    "E2": [[6, 0]],
    "F2": [[6, 1]],
    "F#2": [[6, 2]],
    "G2": [[6, 3]],
    "G#2": [[6, 4]],
    "A2": [[6, 5], [5, 0]],
    "A#2": [[6, 6], [5, 1]],
    "B2": [[6, 7], [5, 2]],
    "C3": [[6, 8], [5, 3]],
    "C#3": [[6,9], [5, 4]],
    "D3": [[6, 10], [5, 5], [4, 0]],
    "D#3": [[6, 11], [5, 6], [4, 1]],
    "E3": [[6, 12], [5, 7], [4, 2]],
    "F3": [[6, 13], [5, 8], [4, 3]],
    "F#3": [[6, 14], [5, 9], [4, 4]],
    "G3": [[6, 15], [5, 10], [4, 5], [3, 0]],
    "G#3": [[6, 16], [5, 11], [4, 6], [3, 1]],
    "A3": [[6, 17], [5, 12], [4, 7], [3, 2]],
    "A#3": [[6, 18], [5, 13], [4, 8], [3, 3]],
    "B3": [[6, 19], [5, 14], [4, 9], [3, 4], [2, 0]],
    "C4": [[6, 20], [5, 15], [4, 10], [3, 5], [2, 1]],
    "C#4": [[5, 16], [4, 11], [3, 6], [2, 2]],
    "D4": [[5, 17], [4, 12], [3, 7], [2, 3]],
    "D#4": [[5, 18], [4, 13], [3, 8], [2, 4]],
    "E4": [[5, 19], [4, 14], [3, 9], [2, 5], [1, 0]],
    "F4": [[5, 20], [4, 15], [3, 10], [2, 6], [1, 1]],
    "F#4": [[4, 16], [3, 11], [2, 7], [1, 2]],
    "G4": [[4, 17], [3, 12], [2, 8], [1, 3]],
    "G#4": [[4, 18], [3, 13], [2, 9], [1, 4]],
    "A4": [[4, 19], [3, 14], [2, 10], [1, 5]],
    "A#4": [[4, 20], [3, 15], [2, 11], [1, 6]],
    "B4": [[3, 16], [2, 12], [1, 7]],
    "C5": [[3, 17], [2, 13], [1, 8]],
    "C#5": [[3, 18], [2, 14], [1, 9]],
    "D5": [[3, 19], [2, 15], [1, 10]],
    "D#5": [[3, 20], [2, 16], [1, 11]],
    "E5": [[2, 17], [1, 12]],
    "F5": [[2, 18], [1, 13]],
    "F#5": [[2, 19], [1, 14]],
    "G5": [[2, 20], [1, 15]],
    "G#5": [[1, 16]],
    "A5": [[1, 17]],
    "A#5": [[1, 18]],
    "B5": [[1, 19]],
    "C6": [[1, 20]]
}
minMidi = 40  # Midi value of lowest note (open E = E2)
maxMidi = 84  # Max note C6
notesDict = {notes[i]: i for i in range(len(notes))}
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Glasbeni škrati")
clock = pygame.time.Clock()
stringsFont = pygame.font.Font("bahnschrift.ttf", 32)

# Slika škrata
skratImg = pygame.image.load("skrat.png")
skratImg = pygame.transform.scale(skratImg, (40, 40))


def drawSkrat(skrat):
    gameDisplay.blit(skratImg, (skrat.xTop, skrat.yTop))
    gameDisplay.blit(skratImg, (skrat.xBot, skrat.yBot))


def createNewSkrat(h, w):
    stringSpacing = h / 14
    fretWidth = w / 21
    midi = random.randrange(minMidi, maxMidi)
    note = midiNumberToNoteName(midi)
    string, fret = fretboardNotes[note][random.randrange(0, len(fretboardNotes[note]))]
    print("Creating skrat", note, "at location", string, fret)
    skrat = Skrat(w + 50, (string - 0.5) * stringSpacing,  # Top half of window
                  (fret + 0.125) * fretWidth, h / 2 + (string - 0.5) * stringSpacing,
                  midi)
    return skrat


def midiNumberToNoteName(x):
    octave = int(x / 12) - 1
    note = notes[x % 12]
    return str(note) + str(octave)


def drawNotes():
    font = pygame.font.Font("bahnschrift.ttf", 32)
    for idx in range(len(notes)):
        note = notes[idx]
        textSurface = font.render(note, True, (255,255,255))
        textRect = textSurface.get_rect()
        textRect.center = (idx * (width / len(notes)) + 25, height - 25)
        pygame.draw.rect(gameDisplay, separator, [idx * (width / len(notes)) + 50, 0, 1, height])
        gameDisplay.blit(textSurface, textRect)
    # pygame.display.update()


def drawNotes2():
    w, h = pygame.display.get_surface().get_size()
    fretWidth = w / 21  # Maybe more?
    stringSpacing = h / 14
    # Drawing frets
    for i in range(20):
        pygame.draw.rect(gameDisplay, separator, [(i + 1) * fretWidth, (h + stringSpacing) / 2, 1, h / 2 - stringSpacing])
    # Draw fret markers
    for i in [3, 5, 7, 9, 15, 17, 19]:
        pygame.draw.circle(gameDisplay, separator, [int((i + 0.5) * fretWidth), int(3.5 * stringSpacing + h / 2)], 10)
    pygame.draw.circle(gameDisplay, separator, [int(12.5 * fretWidth), int(1.5 * stringSpacing + h / 2)], 10)
    pygame.draw.circle(gameDisplay, separator, [int(12.5 * fretWidth), int(5.5 * stringSpacing + h / 2)], 10)
    # Drawing strings
    for i in range(6):
        # Top half
        pygame.draw.rect(gameDisplay, separator, [fretWidth / 4, (i + 1) * stringSpacing, w, 2])
        # Bottom half
        pygame.draw.rect(gameDisplay, stringColor, [fretWidth / 4, h / 2 + (i + 1) * stringSpacing, w, 3])
    idx = 0
    for string in ["e", "B", "G", "D", "A", "E"]:
        textSurface = stringsFont.render(string, True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (fretWidth / 6, h / 2 + stringSpacing * (idx + 1))
        gameDisplay.blit(textSurface, textRect)
        textSurface = stringsFont.render(string, True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (fretWidth / 6, stringSpacing * (idx + 1))
        gameDisplay.blit(textSurface, textRect)
        idx += 1


"""def game():
    yChange = 2
    generationCounter = 0
    score = 0
    targets = [createNewSkrat()]
    endGame = False
    noteQ = queue.Queue()
    exitQ = queue.Queue()
    detectorThread = threading.Thread(target=noteDetector.NoteDetector, args=(noteQ, exitQ))
    detectorThread.start()
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 30)
    while not endGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitQ.put(0)
                endGame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    exitQ.put(0)
                    endGame = True
                if event.key == pygame.K_k:
                    yChange += 1
                if event.key == pygame.K_j:
                    yChange -= 1
        gameDisplay.fill(background)
        for target in targets:
            target[1] += yChange
            if target[1] > height:
                targets.remove(target)
                score -= 1
            else:
                drawSkrat(target[0], target[1])
        drawNotes()
        fontSur = font.render("Score: " + str(score), False, (255, 255, 255))
        gameDisplay.blit(fontSur, (10, 10))
        pygame.display.update()
        clock.tick(30)
        generationCounter += 1
        if generationCounter == 60:
            targets.append(createNewSkrat())
            generationCounter = 0
        elif generationCounter % 2 == 0: #== 30:
            if not noteQ.empty():
                detected = notesDict[noteQ.get()]
                #print("Detected note is ", detected, "wanted is", targets[0][2])
                if len(targets) > 0 and detected == targets[0][2]:
                    targets = targets[1:]
                    score += 1
                    print("NOTE", detected, "Hit detected")
    detectorThread.join()
    print("Thread joined")"""


def game2():
    xChange = 2
    generationCounter = 0
    score = 0

    endGame = False
    noteQ = queue.Queue()
    exitQ = queue.Queue()
    pygame.display.set_mode((1200, 600))
    w, h = pygame.display.get_surface().get_size()
    targets = [createNewSkrat(h, w)]
    detectorThread = threading.Thread(target=noteDetector.NoteDetector, args=(noteQ, exitQ))
    detectorThread.start()
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 24)
    while not endGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitQ.put(0)
                endGame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    exitQ.put(0)
                    endGame = True
                if event.key == pygame.K_k:
                    xChange += 1
                if event.key == pygame.K_j:
                    xChange -= 1
        gameDisplay.fill(background)
        drawNotes2()
        for target in targets:
            target.move()
            #if target[1] > height:
            #    targets.remove(target)
            #    score -= 1
            #else:
            drawSkrat(target)
        fontSur = font.render("Score: " + str(score), False, (255, 255, 255))
        gameDisplay.blit(fontSur, (w / 2, 0))
        pygame.display.update()
        clock.tick(30)
        generationCounter += 1
        if generationCounter == 60:
            generationCounter = 0
        elif generationCounter % 2 == 0: #== 30:
            if not noteQ.empty():
                #detected = notesDict[noteQ.get()]
                detected = noteQ.get()
                #print("Detected note is ", detected, "wanted is", targets[0][2])
                if len(targets) > 0 and detected == targets[0].midiNo:
                    targets.append(createNewSkrat(h, w))
                    targets = targets[1:]
                    score += 1
                    print("NOTE", detected, "Hit detected")
    detectorThread.join()
    print("Thread joined")


def menu():
    startMenu = True
    while startMenu:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if width / 2 - 100 < mouse[0] < width / 2 + 100:
                    if 0.25 * height - 50 < mouse[1] < 0.25 * height + 50:
                        #print("Start button clicked")
                        startMenu = False
                    elif 0.75 * height - 50 < mouse[1] < 0.75 * height + 50:
                        #print("Close button")
                        pygame.quit()
                        quit()
        gameDisplay.fill(background)
        pygame.draw.rect(gameDisplay, separator, [width / 2 - 100, 0.25 * height - 50, 200, 100])
        pygame.draw.rect(gameDisplay, separator, [width / 2 - 100, 0.75 * height - 50, 200, 100])
        font = pygame.font.Font("bahnschrift.ttf", 36)
        textSurface = font.render("Start", True, background)
        textRect = textSurface.get_rect()
        textRect.center = (width / 2, 0.25 * height)
        gameDisplay.blit(textSurface, textRect)

        textSurface = font.render("TODO", True, background)
        textRect = textSurface.get_rect()
        textRect.center = (width / 2, 0.75 * height)
        gameDisplay.blit(textSurface, textRect)
        pygame.display.update()
        clock.tick(30)
    # game()
    game2()


# menu()
game2()
pygame.quit()
quit()
