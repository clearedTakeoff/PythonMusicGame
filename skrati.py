import pygame
import random
import noteDetector
import threading
import queue
import math
import pyaudio
import os
import pygame_textinput
import json

class Skrat:
    def __init__(self, xTop, yTop, xBot, yBot, midiNo, string, fret):
        self.xTop = xTop
        self.yTop = yTop
        self.xBot = xBot
        self.yBot = yBot
        self.midiNo = midiNo
        self.string = string
        self.fret = fret

    def move(self):
        self.xTop -= 3

class skratGame:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        # Color definition
        self.background = (13, 33, 106)
        self.separator = (132, 142, 179)
        self.stringColor = (75, 75, 75)
        self.selected = (90, 103, 146)
        self.notes = "C C# D D# E F F# G G# A A# B".split(" ")
        self.deviceIndex = 1
        # Location of each note, formatted as [string number, fret number]
        # Where high E string is numbered as 1 and low E as 6
        # Max fret number is 24
        self.fretboardNotes = {
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
            "C6": [[1, 20]],
            "C#6": [[1, 21]],
            "D6": [[1, 22]],
            "D#6": [[1, 23]],
            "E6": [[1, 24]]
        }
        self.songDir = {}
        self.highScores = {}
        tmpFilenames = os.listdir("leaderboards")
        for f in os.listdir("songs"):
            file = open("songs/" + f, "r", encoding="utf-8")
            title = file.readline().strip()
            self.songDir[title] = "songs/" + f
            if f in tmpFilenames:
                file2 = open("leaderboards/" + f, "r")
                self.highScores[f] = json.loads(file2.read())
                file2.close()
            else:
                file2 = open("leaderboards/" + f, "w")
                self.highScores[f] = [[],[]]
                file2.write(json.dumps(self.highScores[f]))
                file2.close()
            file.close()
        f = "random.txt"
        if f in tmpFilenames:
            file2 = open("leaderboards/" + f, "r")
            self.highScores[f] = json.loads(file2.read())
            file2.close()
        else:
            file2 = open("leaderboards/" + f, "w")
            self.highScores[f] = [[], []]
            file2.write(json.dumps(self.highScores[f]))
            file2.close()
        print(self.highScores)
        self.minMidi = 40  # Midi value of lowest note (open E = E2)
        self.maxMidi = 84  # Max note C6
        self.notesDict = {self.notes[i]: i for i in range(len(self.notes))}
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        wrongNotes = []
        pygame.display.set_caption("Glasbeni škrati")
        self.clock = pygame.time.Clock()
        self.stringsFont = pygame.font.Font("bahnschrift.ttf", 32)

        # Slika škrata
        self.skratImg = pygame.image.load("skrat.png")
        self.skratImg = pygame.transform.scale(self.skratImg, (40, 40))
        #self.songChoice()
        self.menu()

    def drawSkrat(self, skrat):
        self.gameDisplay.blit(self.skratImg, (skrat.xTop, skrat.yTop))

    def createNewSkrat(self, h, w, string=None, fret=None, midiNote=None):
        stringSpacing = h / 14
        fretWidth = w / 21
        if midiNote is None:
            midi = random.randrange(self.minMidi, self.maxMidi)
        else:
            midi = midiNote
        note = self.midiNumberToNoteName(midi)
        if string is None and fret is None:
            string, fret = self.fretboardNotes[note][random.randrange(0, len(self.fretboardNotes[note]))]
        else:
            string = int(string)
            fret = int(fret)
        skrat = Skrat(w + 50, (string - 0.5) * stringSpacing,  # Top half of window
                      (fret + 0.125) * fretWidth, h / 2 + (string - 0.5) * stringSpacing,
                      midi, string, fret)
        return skrat

    def midiNumberToNoteName(self, x):
        octave = int(x / 12) - 1
        note = self.notes[x % 12]
        return str(note) + str(octave)

    def noteNameToMidiNumber(self, x):
        return (int(x[-1]) - 1) * 12 + 24 + self.notes.index(x[:-1])

    def distanceBetweenNotes(self, note1, note2):
        return math.sqrt((note1[0] - note2[0]) ** 2 + (note1[1] - note2[1]) ** 2)

    def readInputNotes(self, file):
        songNotes = []
        startingPos = []
        f = open(file, "r")
        title = f.readline()  # Discard first line - title of the song
        for line in f:
            l = line.strip().split(",")
            if len(l) > 1:
                startingPos.append(l[1])
                startingPos.append(l[2])
            else:
                songNotes.append(l[0])
        return title, startingPos, songNotes

    def closestWrongNote(self, notePos, playedNote):
        possibleLocations = self.fretboardNotes[playedNote]
        distance = 999
        closestNote = None
        for pos in possibleLocations:
            d = self.distanceBetweenNotes(notePos, pos)
            if d < distance:
                distance = d
                closestNote = pos
        return closestNote

    def closestNextNote(self, notePos, nextNote):
        possibleLocations = self.fretboardNotes[nextNote]
        distance = 999
        closestNote = None
        for pos in possibleLocations:
            d = self.distanceBetweenNotes(notePos, pos)
            if d < distance:
                distance = d
                closestNote = pos
        return closestNote

    def drawFont(self, font, color, centerX, centerY, text):
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (centerX, centerY)
        self.gameDisplay.blit(textSurface, textRect)

    def drawNotes(self):
        font = pygame.font.Font("bahnschrift.ttf", 22)
        w, h = pygame.display.get_surface().get_size()
        fretWidth = w / 21  # Maybe more?
        stringSpacing = h / 14
        # Draw back arrow
        startX = 5
        startY = 20
        pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX + 10, startY - 15),
                                                               (startX + 10, startY - 7), (startX + 30, startY - 7),
                                                               (startX + 30, startY + 7), (startX + 10, startY + 7),
                                                               (startX + 10, startY + 15)])
        # Drawing frets
        for i in range(20):
            pygame.draw.rect(self.gameDisplay, self.separator, [(i + 1) * fretWidth, (h + stringSpacing) / 2, 1, h / 2 - stringSpacing])
        # Draw fret markers
        for i in [3, 5, 7, 9, 15, 17, 19]:
            pygame.draw.circle(self.gameDisplay, self.separator, [int((i + 0.5) * fretWidth), int(3.5 * stringSpacing + h / 2)], 10)
            self.drawFont(font, self.separator, int((i + 0.5) * fretWidth), h / 2, str(i))
        pygame.draw.circle(self.gameDisplay, self.separator, [int(12.5 * fretWidth), int(1.5 * stringSpacing + h / 2)], 10)
        pygame.draw.circle(self.gameDisplay, self.separator, [int(12.5 * fretWidth), int(5.5 * stringSpacing + h / 2)], 10)
        self.drawFont(font, self.separator, (12.5 * fretWidth), h / 2, "12")
        # Drawing strings
        for i in range(6):
            # Top half
            pygame.draw.rect(self.gameDisplay, self.separator, [fretWidth / 4, (i + 1) * stringSpacing, w, 2])
            # Bottom half
            pygame.draw.rect(self.gameDisplay, self.stringColor, [fretWidth / 4, h / 2 + (i + 1) * stringSpacing, w, 3])
        idx = 0
        for string in ["e", "B", "G", "D", "A", "E"]:
            self.drawFont(self.stringsFont, (255, 255, 255), fretWidth / 6,  h / 2 + stringSpacing * (idx + 1), string)
            self.drawFont(self.stringsFont, (255, 255, 255), fretWidth / 6, stringSpacing * (idx + 1), string)
            idx += 1

    # Mode 0 = random notes, mode 1 = playing a song
    def game2(self, mode=0, filename=None):
        xChange = 2
        generationCounter = 0
        score = 0
        endGame = False
        noteQ = queue.Queue()
        exitQ = queue.Queue()
        pygame.display.set_mode((1200, 600))
        w, h = pygame.display.get_surface().get_size()
        noteSequence = []
        noteCounter = 0
        title = None
        if mode == 1 and filename is not None:
            title, startingPos, noteSequence = self.readInputNotes(filename)
            noteCounter = 1
            targets = [self.createNewSkrat(h, w, startingPos[0], startingPos[1],
                                           self.noteNameToMidiNumber(noteSequence[0]))]
        else:
            targets = [self.createNewSkrat(h, w)]
        detectorThread = threading.Thread(target=noteDetector.NoteDetector, args=(noteQ, exitQ, self.deviceIndex))
        detectorThread.start()
        pygame.font.init()
        font = pygame.font.Font("bahnschrift.ttf", 24)
        noteFont = pygame.font.Font("bahnschrift.ttf", 22)
        xDetected = yDetected = 0
        lastNote = None
        detectedWrong = None
        while not endGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitQ.put(0)
                    endGame = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        noteQ.put(targets[0].midiNo)
                    elif event.key == pygame.K_k:
                        xChange += 1
                    elif event.key == pygame.K_j:
                        xChange -= 1
                    elif event.key == pygame.K_BACKSPACE:
                        exitQ.put(0)
                        endGame = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 5 < x < 35 and 5 < y < 35:
                        exitQ.put(0)
                        endGame = True
            self.gameDisplay.fill(self.background)
            self.drawNotes()
            for target in targets:
                target.move()
                #if target[1] > self.height:
                #    targets.remove(target)
                #    score -= 1
                #else:
                self.drawSkrat(target)
            pygame.draw.circle(self.gameDisplay, (255, 0, 0), [int(targets[0].xBot + 22), int(targets[0].yBot + 25)],
                               int(w/62))
            # Wrong circle draw
            if xDetected > 0 and yDetected > 0:
                pygame.draw.circle(self.gameDisplay, (255, 120, 0), [int(xDetected + 22), int(yDetected)], int(w / 62))
                self.drawFont(noteFont, (255, 255, 255), int(xDetected + 22), int(yDetected),
                              detectedWrong[:-1])
            self.drawFont(noteFont, (255, 255, 255), int(targets[0].xBot + 22), int(targets[0].yBot + 25),
                          self.midiNumberToNoteName(targets[0].midiNo)[:-1])
            fontSur = font.render("Score: " + str(score), False, (255, 255, 255))
            self.gameDisplay.blit(fontSur, (w / 2, 0))
            generationCounter += 1
            if generationCounter == 60:
                generationCounter = 0
            elif generationCounter % 2 == 0:  # == 30:
                if not noteQ.empty():
                    detected = noteQ.get()
                    if len(targets) > 0 and detected == targets[0].midiNo:
                        if mode == 0:
                            targets.append(self.createNewSkrat(h, w))
                        else:
                            if noteCounter == len(noteSequence):
                                exitQ.put(0)
                                break
                            nextLoc = self.closestNextNote([targets[0].string, targets[0].fret],
                                                           noteSequence[noteCounter])
                            targets.append(self.createNewSkrat(h, w, nextLoc[0], nextLoc[1],
                                                               self.noteNameToMidiNumber(noteSequence[noteCounter])))
                            noteCounter += 1
                        targets = targets[1:]
                        score += 1
                        xDetected = yDetected = 0
                        lastNote = detected
                    else:
                        if detected != lastNote and detected >= 40:
                            detectedWrong = self.midiNumberToNoteName(detected)
                            wrongNote = self.closestWrongNote([targets[0].string, targets[0].fret],
                                                              detectedWrong)
                            xDetected = (wrongNote[1] + 0.125) * (w / 21)
                            yDetected = h / 2 + wrongNote[0] * (h / 14)
                            # print("Looking for", self.midiNumberToNoteName(targets[0].midiNo), "got",
                                  # self.midiNumberToNoteName(detected), "at", wrongNote)
            pygame.display.update()
            self.clock.tick(30)
        detectorThread.join()
        print("Thread joined")
        pygame.display.set_mode((self.width, self.height))
        if score > 0:
            if mode == 1:
                self.highScore(filename.split("/")[1], score)
            else:
                self.highScore("random.txt", score)

    def highScore(self, title=None, score=10):
        runLoop = True
        textinput = pygame_textinput.TextInput(font_family="bahnschrift.ttf",text_color=(255,255,255))
        pygame.display.set_mode((600, 600))
        font = pygame.font.Font("bahnschrift.ttf", 32)
        leaderFont = pygame.font.Font("bahnschrift.ttf", 24)
        smallFont = pygame.font.Font("bahnschrift.ttf", 16)
        while runLoop:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    runLoop = False
            if textinput.update(events):
                runLoop = False
            self.gameDisplay.fill(self.background)
            self.drawFont(font, self.separator, 300, 200, "Vpiši svoje ime")
            self.gameDisplay.blit(textinput.get_surface(), (300, 250))
            pygame.display.update()
            self.clock.tick(30)
        name = textinput.get_text()
        runLoop = True
        leaderboard = self.highScores[title]
        ind = 0
        if len(leaderboard[0]) > 0:
            while ind < len(leaderboard[0]) and leaderboard[1][ind] > score:
                ind += 1
            leaderboard[0].insert(ind, name)
            leaderboard[1].insert(ind, score)
        else:
            leaderboard[0].append(name)
            leaderboard[1].append(score)
        file = open("leaderboards/" + title, "w")
        file.write(json.dumps(leaderboard))
        file.close()
        self.highScores[title] = leaderboard
        if ind <= 9:
            while runLoop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runLoop = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 10 < x < 80 and 30 < y < 70:  # Back button
                            runLoop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
                            runLoop = False
                self.gameDisplay.fill(self.background)
                self.drawFont(font, (255, 255, 255), 300, 20, "Lestvica najboljših")
                vertOffset = 100
                length = len(leaderboard[0])
                # Back arrow
                startX = 10
                startY = 50
                pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX + 20, startY - 20),
                                                                       (startX + 20, startY - 10),
                                                                       (startX + 70, startY - 10),
                                                                       (startX + 70, startY + 10),
                                                                       (startX + 20, startY + 10),
                                                                       (startX + 20, startY + 20)])
                self.drawFont(smallFont, self.background, 50, startY, "Nazaj")
                for i in range(10):
                    if i >= length:
                        self.drawFont(leaderFont, (255, 255, 255), 300, vertOffset + i * 40,
                                      str(i + 1) + ". ---- 0")
                    else:
                        self.drawFont(leaderFont, (255, 255, 255), 300, vertOffset + i * 40,
                                      str(i + 1) + ". " + leaderboard[0][i] + " " + str(leaderboard[1][i]))
                pygame.display.update()
                self.clock.tick(30)

    def practiceMode(self):
        xChange = 2
        generationCounter = 0
        score = 0
        endGame = False
        noteQ = queue.Queue()
        exitQ = queue.Queue()
        pygame.display.set_mode((1200, 600))
        w, h = pygame.display.get_surface().get_size()
        #targets = [createNewSkrat(h, w)]
        detectorThread = threading.Thread(target=noteDetector.NoteDetector, args=(noteQ, exitQ, self.deviceIndex))
        detectorThread.start()
        pygame.font.init()
        noteFont = pygame.font.Font("bahnschrift.ttf", 22)
        detectedLocations = []
        noteName = None
        lastNote = None
        while not endGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitQ.put(0)
                    endGame = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        targets.append(self.createNewSkrat(h, w))
                        targets = targets[1:]
                    elif event.key == pygame.K_k:
                        xChange += 1
                    elif event.key == pygame.K_j:
                        xChange -= 1
                    elif event.key == pygame.K_BACKSPACE:
                        exitQ.put(0)
                        endGame = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 5 < x < 35 and 5 < y < 35:
                        exitQ.put(0)
                        endGame = True
            self.gameDisplay.fill(self.background)
            self.drawNotes()
            # for target in targets:
                # target.move()
                #if target[1] > self.height:
                #    targets.remove(target)
                #    score -= 1
                #else:
                # drawSkrat(target)
            #pygame.draw.circle(self.gameDisplay, (255, 0, 0), [int(targets[0].xBot + 22), int(targets[0].yBot + 25)], int(w/62))
            # Wrong circle draw
            if len(detectedLocations) > 0:
                for location in detectedLocations:
                    xDetected = location[1] * (w / 21)
                    yDetected = h / 2 + location[0] * (h / 14)
                    pygame.draw.circle(self.gameDisplay, (255, 120, 0), [int(xDetected + 28), int(yDetected)], int(w / 62))
                    self.drawFont(noteFont, (255, 255, 255), int(xDetected + 28), int(yDetected), noteName[:-1])
            generationCounter += 1
            if generationCounter == 60:
                generationCounter = 0
            elif generationCounter % 2 == 0:  # == 30:
                if not noteQ.empty():
                    detected = noteQ.get()
                    # if len(targets) > 0 and detected == targets[0].midiNo:
                        # targets.append(createNewSkrat(h, w))
                        # targets = targets[1:]
                        # score += 1
                        # xDetected = yDetected = 0
                        # lastNote = detected
                        # print("NOTE", detected, "Hit detected")
                    if detected != lastNote:
                        #wrongNote = closestWrongNote([targets[0].string, targets[0].fret], midiNumberToNoteName(detected))
                        noteName = self.midiNumberToNoteName(detected)
                        detectedLocations = self.fretboardNotes[noteName]
                        # xDetected = wrongNote[1] * (w / 21)
                        # yDetected = h / 2 + wrongNote[0] * (h / 14)
                        # print("Looking for", midiNumberToNoteName(targets[0].midiNo), "got", midiNumberToNoteName(detected),
                              # "at", wrongNote)
            pygame.display.update()
            self.clock.tick(30)
        detectorThread.join()
        print("Thread joined")
        pygame.display.set_mode((self.width, self.height))

    def menu(self):
        startMenu = True
        print("Device index", self.deviceIndex)
        while startMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.width / 2 - 175 < mouse[0] < self.width / 2 + 175:
                        if 0.2 * self.height - 50 < mouse[1] < 0.2 * self.height + 50:
                            self.game2(0)
                        elif 0.4 * self.height - 50 < mouse[1] < 0.4 * self.height + 50:
                            #self.game2(1)
                            self.songChoice()
                        elif 0.6 * self.height - 50 < mouse[1] < 0.6 * self.height + 50:
                            self.practiceMode()
                        elif 0.8 * self.height - 50 < mouse[1] < 0.8 * self.height + 50:
                            self.inputChoice()
            self.gameDisplay.fill(self.background)
            pygame.draw.rect(self.gameDisplay, self.separator, [self.width / 2 - 175, 0.2 * self.height - 50, 350, 100])
            pygame.draw.rect(self.gameDisplay, self.separator, [self.width / 2 - 175, 0.4 * self.height - 50, 350, 100])
            pygame.draw.rect(self.gameDisplay, self.separator, [self.width / 2 - 175, 0.6 * self.height - 50, 350, 100])
            pygame.draw.rect(self.gameDisplay, self.separator, [self.width / 2 - 175, 0.8 * self.height - 50, 350, 100])
            font = pygame.font.Font("bahnschrift.ttf", 36)
            self.drawFont(font, self.background, self.width / 2, 0.2 * self.height, "Naključen način")

            self.drawFont(font, self.background, self.width / 2, 0.4 * self.height, "Zaigraj melodijo")

            self.drawFont(font, self.background, self.width / 2, 0.6 * self.height, "Prosta igra")

            self.drawFont(font, self.background, self.width / 2, 0.8 * self.height, "Izberi vhod")

            pygame.display.update()
            self.clock.tick(30)
        # game()
        self.game2()

    def inputChoice(self):
        p = pyaudio.PyAudio()
        devices = []
        for i in range(p.get_host_api_info_by_index(0).get("deviceCount")):
            if p.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels") > 0:
                # print("Input " + str(i) + " - " + p.get_device_info_by_host_api_device_index(0, i).get("name"))
                devices.append(p.get_device_info_by_host_api_device_index(0, i).get("name"))
        p.terminate()
        font = pygame.font.Font("bahnschrift.ttf", 20)
        smallFont = pygame.font.Font("bahnschrift.ttf", 16)
        runLoop = True
        while runLoop:
            k = 1 / (len(devices) + 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.width / 2 - 175 < mouse[0] < self.width / 2 + 175:
                        for i in range(len(devices)):
                            if (i + 1) * k * self.height - 50 < mouse[1] < (i + 1) * k * self.height + 50:
                                self.deviceIndex = i
                                runLoop = False
                                break
                    elif 10 < mouse[0] < 80 and 30 < mouse[1] < 70:  # Back button
                        runLoop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        runLoop = False
            self.gameDisplay.fill(self.background)
            # Back arrow
            startX = 10
            startY = 50
            pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX + 20, startY - 20),
                                                                   (startX + 20, startY - 10),
                                                                   (startX + 70, startY - 10),
                                                                   (startX + 70, startY + 10),
                                                                   (startX + 20, startY + 10),
                                                                   (startX + 20, startY + 20)])
            self.drawFont(smallFont, self.background, 50, startY, "Nazaj")
            for i in range(len(devices)):
                if i == self.deviceIndex:
                    color = self.selected
                else:
                    color = self.separator
                pygame.draw.rect(self.gameDisplay, color,
                                 [self.width / 2 - 175, (i + 1) * k * self.height - 50, 350, 100])
                self.drawFont(font, self.background, self.width / 2, (i + 1) * k * self.height, devices[i])
            pygame.display.update()
        self.menu()

    def songChoice(self):
        songs = list(self.songDir.keys())
        loopRun = True
        index = 0
        font = pygame.font.Font("bahnschrift.ttf", 34)
        smallerFont = pygame.font.Font("bahnschrift.ttf", 26)
        evenSmallerFont = pygame.font.Font("bahnschrift.ttf", 16)
        while loopRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.width / 2 - 60 < y < self.width / 2 + 60:
                        if 10 < x < 70:
                            index -= 1  # Next song
                        elif self.width - 10 > x > self.width - 70:
                            index += 1  # Previous song
                        index %= len(songs)
                    elif 10 < x < 80 and 30 < y < 70:  # Back button
                        loopRun = False
                    elif self.width / 2 - 175 < x < self.width / 2 + 175 and self.height - 125 < y < self.height - 25:
                        self.game2(1, self.songDir[songs[index]])  # Start button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        index -= 1
                        index %= len(songs)
                    elif event.key == pygame.K_RIGHT:
                        index += 1
                        index %= len(songs)
                    elif event.key == pygame.K_RETURN:
                        self.game2(1, self.songDir[songs[index]])
                    elif event.key == pygame.K_BACKSPACE:
                        loopRun = False

            startX = 10
            startY = self.height / 2
            self.gameDisplay.fill(self.background)
            # Arrows left right
            pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX + 40, startY - 60),
                                                                   (startX + 60, startY - 60), (startX + 20, startY),
                                                                   (startX + 60, startY + 60),
                                                                   (startX + 40, startY + 60)])
            startX = self.width - 10
            pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX - 40, startY - 60),
                                                                   (startX - 60, startY - 60), (startX - 20, startY),
                                                                   (startX - 60, startY + 60),
                                                                   (startX - 40, startY + 60)])
            # Back arrow
            startX = 10
            startY = 50
            pygame.draw.polygon(self.gameDisplay, self.separator, [(startX, startY), (startX + 20, startY - 20),
                                                                   (startX + 20, startY - 10),
                                                                   (startX + 70, startY - 10),
                                                                   (startX + 70, startY + 10),
                                                                   (startX + 20, startY + 10),
                                                                   (startX + 20, startY + 20)])
            self.drawFont(evenSmallerFont, self.background, 50, startY, "Nazaj")
            pygame.draw.rect(self.gameDisplay, self.separator, [self.width / 2 - 175, self.height - 125, 350, 100])
            self.drawFont(font, self.background, self.width / 2, self.height - 75, "Začetek")

            self.drawFont(smallerFont, self.separator, self.width / 2, 50, "Izberi poljubno melodijo")

            self.drawFont(font, (255, 255, 255), self.width / 2, self.height / 2, songs[index])

            pygame.display.update()


if __name__ == "__main__":
    s = skratGame()
    #menu()
    #s.inputChoice()
    #game2(1)
    #practiceMode()
    pygame.quit()
