import pygame
from PIL import Image
import glob
import sys
from random import randint


class Diceroller:
    def __init__(self, blitpos, number, distance):
        self.stoppoints = [1, 8, 15, 23, 30, 37]

        if isinstance(blitpos[0], int):
            self.x = blitpos[0]
            self.y = blitpos[1]
        else:
            self.x = False
            self.blitpos = blitpos
        self.number = number
        self.distance = distance
        self.counter = 0
        self.rolled = False
        self.slowrounds = []
        self.state = []
        self.results = []
        for zza in range(0, self.number):
            self.slowrounds.append(False)
            self.state.append(False)
            self.results.append(0)
        self.frames = glob.glob(relative + "assets\\board\\dice\\frames\\*.png")
        for zza in range(0, len(self.frames)):
            self.frames[zza] = pygame.image.load(self.frames[zza]).convert_alpha()
        self.stopframes = []
        dark = glob.glob(relative + "assets\\board\\dice\\stopped\\*dark.png")
        light = glob.glob(relative + "assets\\board\\dice\\stopped\\*light.png")
        for zza in range(0, 6):
            self.stopframes.append([pygame.image.load(dark[zza]).convert_alpha(), pygame.image.load(light[zza]).convert_alpha()])

    def update(self):
        for zza in range(0, self.number):
            if not self.state[zza]:
                if x:
                    window.blit(self.frames[self.counter], [self.x + self.distance * zza, self.y])
                else:
                    window.blit(self.frames[self.counter], self.blitpos[zza])
            else:
                if x:
                    window.blit(self.stopframes[self.results[zza] - 1][(self.counter // 21) % 2], [self.x + self.distance * zza, self.y])
                else:
                    window.blit(self.stopframes[self.results[zza] - 1][(self.counter // 21) % 2], self.blitpos[zza])
        self.counter += 1
        if self.counter == 43:
            self.counter = 0
            for zza in range(0, len(self.slowrounds)):
                if self.slowrounds[zza] != 0:
                    self.slowrounds[zza] -= 1

        for zza in range(0, len(self.results)):
            if self.results[zza] != 0 and self.counter == self.stoppoints[self.results[zza] - 1] and not self.state[zza] and self.slowrounds[zza] == 0:
                self.state[zza] = "stop"
            elif self.counter == self.stoppoints[self.results[zza] - 1] and self.state[zza] == "stop" and self.slowrounds[zza] is False:
                self.state[zza] = False
                self.results[zza] = 0

    def roll(self, statepos="all"):
        if statepos == "all":
            for zza in range(0, len(self.results)):
                self.results[zza] = randint(1, 6)
                self.slowrounds[zza] = randint(0, 2)
        else:
            self.results[statepos] = randint(1, 6)
            self.slowrounds[statepos] = randint(0, 3)
        self.rolled = True

    def reset(self, statepos="all"):
        if statepos == "all":
            for zza in range(0, len(self.results)):
                self.slowrounds[zza] = False
        else:
            self.slowrounds[statepos] = False
        self.rolled = False


class Setinfo:
    def __init__(self):
        self.setcomps = []
        self.setcomps.append((1, 3))
        self.setcomps.append((6, 8, 9))
        self.setcomps.append((11, 13, 14))
        self.setcomps.append((16, 18, 19))
        self.setcomps.append((21, 23, 24))
        self.setcomps.append((26, 27, 29))
        self.setcomps.append((31, 32, 34))
        self.setcomps.append((37, 39))
        self.setcomps.append((12, 38))
        self.setcomps.append((5, 15, 25, 35))

        self.housecosts = [100, 150, 300, 300, 450, 450, 600, 400]

        self.houseblitpoints = []
        self.houseblitpoints.append([[882, 531], [780, 531]])
        self.houseblitpoints.append([[627, 531], [525, 531], [474, 531]])
        self.houseblitpoints.append([[457, 480], [457, 378], [457, 327]])
        self.houseblitpoints.append([[457, 225], [457, 123], [457, 72]])
        self.houseblitpoints.append([[474, 3], [576, 3], [627, 3]])
        self.houseblitpoints.append([[729, 3], [780, 3], [882, 3]])
        self.houseblitpoints.append([[933, 72], [933, 123], [933, 225]])
        self.houseblitpoints.append([[933, 378], [933, 480]])

        self.propertycosts = []
        for zzm in range(0, 40):
            self.propertycosts.append(0)

        # this for loop is just changing all of the property costs to proper ones
        for zzm in range(0 ,1):
            self.propertycosts[1] = 60
            self.propertycosts[3] = 60
            self.propertycosts[5] = 200
            self.propertycosts[6] = 100
            self.propertycosts[8] = 100
            self.propertycosts[9] = 120
            self.propertycosts[11] = 140
            self.propertycosts[12] = 150
            self.propertycosts[13] = 140
            self.propertycosts[14] = 150
            self.propertycosts[15] = 200
            self.propertycosts[16] = 180
            self.propertycosts[18] = 180
            self.propertycosts[19] = 200
            self.propertycosts[21] = 220
            self.propertycosts[23] = 220
            self.propertycosts[24] = 240
            self.propertycosts[25] = 200
            self.propertycosts[26] = 260
            self.propertycosts[27] = 260
            self.propertycosts[28] = 150
            self.propertycosts[29] = 280
            self.propertycosts[31] = 300
            self.propertycosts[32] = 300
            self.propertycosts[34] = 320
            self.propertycosts[35] = 200
            self.propertycosts[37] = 350
            self.propertycosts[39] = 400

    def gethousecolour(self, space=-1, setvar=-1):
        if setvar != -1:
            if setvar != 7:
                space = setvar * 5 + 1
            else:
                space = 37

        tempcolour2 = ""
        if space in self.setcomps[0]:
            tempcolour2 = "9f5830"
        elif space in self.setcomps[1]:
            tempcolour2 = "29bfff"
        elif space in self.setcomps[2]:
            tempcolour2 = "c885c4"
        elif space in self.setcomps[3]:
            tempcolour2 = "ff9b00"
        elif space in self.setcomps[4]:
            tempcolour2 = "ff0000"
        elif space in self.setcomps[5]:
            tempcolour2 = "e6e600"
        elif space in self.setcomps[6]:
            tempcolour2 = "3f8837"
        elif space in self.setcomps[7]:
            tempcolour2 = "334b97"

        if tempcolour2 == "":
            return "error"
        return hextorgb(tempcolour2)

    def gethotelcolour(self, space=-1, setvar=-1):
        if setvar != -1:
            if setvar != 7:
                space = setvar * 5 + 1
            else:
                space = 37

        tempcolour3 = self.gethousecolour(space)
        tempcolour3 = rgbtohsl(tempcolour3[0], tempcolour3[1], tempcolour3[2])
        return hsltorgb((tempcolour3[0] - 20) % 360, tempcolour3[1], tempcolour3[2])


class Player:
    def __init__(self, colour, name):
        self.name = name
        self.jail = False
        self.colour = colour
        self.money = 1500
        self.cards = []
        self.sets = []
        self.place = 0
        self.img = pygame.image.load(relative + "assets\\player\\piece.png")
        colourmask = pygame.Surface(self.img.get_size())
        colourmask.fill(self.colour)
        self.img.blit(colourmask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.coords = (0, 0)


class Gamestate:
    def __init__(self, players, name, bidding, freeparking):
        self.name = name
        self.bidding = bidding
        self.freeparking = freeparking
        self.players = players
        self.playerturn = 0
        self.sets = [0, 0, 0, 0, 0, 0, 0, 0]
        self.cards = []
        self.mortgaged = []
        for za in range(1, 40):
            if za not in [2, 4, 7, 17, 22, 33, 36, 38]:
                self.cards.append(za)
        for za in range(0, len(self.players)):
            self.players[za].coords = [(938, 531), (948, 531), (958, 531), (968, 531), (978, 531), (988, 531), (988, 541), (988, 551), (988, 561)][za]
            # putting the players on start
        self.houseimages = []
        for za in range(0, 8):
            self.houseimages.append(0)
        self.updatehouses()

    def updateplayerpos(self):
        positions = []
        for zz in self.players:
            tilespot = 0
            for zza in positions:
                if zz.place == zza[0]:
                    tilespot = zza[1] + 1
            positions.append([zz.place, tilespot])

        for zz in range(0, len(positions)):
            playerx = 70 + (((- self.players[zz].place) % 10) - 1) * 51
            if self.players[zz].place // 10 == 3:
                playerx = 546 - playerx

            if self.players[zz].place in [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]:  # cards with regular piece placement
                if positions[zz][1] in list(range(0, 3)):  # top 3 spots
                    playery = 547
                    if positions[zz][1] == 0:
                        playerx += 21
                    elif positions[zz][1] == 1:
                        playerx += 11
                    else:
                        playerx += 31
                elif positions[zz][1] in list(range(3, 7)):  # middle 4 spots
                    playery = 557
                    if positions[zz][1] == 3:
                        playerx += 6
                    elif positions[zz][1] == 4:
                        playerx += 36
                    elif positions[zz][1] == 5:
                        playerx += 16
                    else:
                        playerx += 26
                else:  # bottom 2 spots
                    playery = 567
                    if positions[zz][1] == 7:
                        playerx += 11
                    else:
                        playerx += 31
            elif self.players[zz].place % 10 == 5:  # trains
                if positions[zz][1] in list(range(0, 3)):  # top 3 spots
                    playery = 532
                    if positions[zz][1] == 0:
                        playerx += 21
                    elif positions[zz][1] == 1:
                        playerx += 11
                    else:
                        playerx += 31
                elif positions[zz][1] in list(range(3, 5)):  # top middle 2 spots
                    playery = 538
                    if positions[zz][1] == 3:
                        playerx += 2
                    else:
                        playerx += 40
                elif positions[zz][1] in list(range(5, 7)):  # bottom middle 2 spots
                    playery = 548
                    if positions[zz][1] == 5:
                        playerx += 2
                    else:
                        playerx += 40
                else:
                    playery = 558
                    if positions[zz][1] == 7:
                        playerx += 2
                    else:
                        playerx += 40
            elif self.players[zz].place % 10 == 0 and self.players[zz].place != 40:  # corners
                if self.players[zz].place == 0:  # go
                    if positions[zz][1] in list(range(0, 6)):  # top 6 spots
                        playery = 531
                        playerx = positions[zz][1] * 10 + 938
                    else:  # others
                        playerx = 988
                        playery = (positions[zz][1] - 6) * 10 + 541
                elif self.players[zz].place == 10:  # visiting
                    if positions[zz][1] in list(range(0, 5)):  # left 5 spots
                        playerx = 408
                        playery = positions[zz][1] * 10 + 533
                    else:  # others
                        playery = 583
                        playerx = 408 + 10 * (positions[zz][1] - 5)
                elif self.players[zz].place == 20:  # free parking
                    if positions[zz][1] in list(range(0, 2)):  # left ones
                        playerx = 405
                        playery = 48 + 10 * positions[zz][1]
                    elif positions[zz][1] in list(range(2, 4)):  # bottom left ones
                        playery = 58
                        playerx = 415 + 10 * (positions[zz][1] - 2)
                    elif positions[zz][1] in list(range(4, 6)):  # right ones
                        playerx = 460
                        playery = 48 + 10 * (positions[zz][1] - 4)
                    elif positions[zz][1] in list(range(6, 8)):  # bottom right ones
                        playery = 58
                        playerx = 450 - 10 * (positions[zz][1] - 6)
                    else:
                        playerx = 405
                        playery = 19
                else:  # go to jail
                    if positions[zz][1] == 0:  # top
                        playerx = 986
                        playery = 6
                    elif positions[zz][1] in list(range(1, 3)):  # top left
                        playerx = 971 - 8 * (positions[zz][1] - 1)
                        playery = 7 + 8 * (positions[zz][1] - 1)
                    elif positions[zz][1] in list(range(3, 5)):  # top right
                        playerx = 985 - 8 * (positions[zz][1] - 3)
                        playery = 21 + 8 * (positions[zz][1] - 3)
                    elif positions[zz][1] in list(range(5, 7)):  # bottom left
                        playerx = 945 - 8 * (positions[zz][1] - 5)
                        playery = 33 + 8 * (positions[zz][1] - 5)
                    else:  # bottom right
                        playerx = 959 - 8 * (positions[zz][1] - 7)
                        playery = 47 + 8 * (positions[zz][1] - 7)
            elif self.players[zz].place in [7, 22, 36]:  # chance
                if positions[zz][1] == 0:
                    playerx += 20
                    playery = 541
                elif positions[zz][1] in list(range(1, 3)):
                    playery = 531
                    playerx += 1 + 39 * ((positions[zz][1] + 1) % 2)
                else:
                    playery = 548 + 10 * ((- positions[zz][1]) % 3)
                    playerx += 1 + 39 * ((positions[zz][1] + 1) % 2)
            elif self.players[zz].place in [2, 17, 33]:  # chest
                if positions[zz][1] in list(range(0, 2)):  # middle 2
                    playery = 578
                    playerx += 8 + 25 * (positions[zz][1] % 2)
                elif positions[zz][1] in list(range(2, 4)):  # bottom 2
                    playery = 586
                    playerx += 1 + 39 * ((positions[zz][1] - 2) % 2)
                elif positions[zz][1] in list(range(4, 6)):  # middle top 2
                    playery = 570
                    playerx += 1 + 14 * ((positions[zz][1] - 4) % 2)
                elif positions[zz][1] == 6:
                    playerx += 40
                    playery = 570
                elif positions[zz][1] == 7:
                    playerx += 1
                    playery = 538
                else:
                    playerx += 9
                    playery = 531
            elif self.players[zz].place == 4:  # income tax
                if positions[zz][1] == 0:
                    playery = 553
                    playerx += 21
                elif positions[zz][1] in list(range(1, 3)):
                    playery = 553
                    playerx += 10 + 22 * ((positions[zz][1] - 1) % 2)
                elif positions[zz][1] in list(range(3, 5)):
                    playery = 561
                    playerx += 3 + 36 * ((positions[zz][1] - 1) % 2)
                elif positions[zz][1] in list(range(5, 7)):
                    playery = 545
                    playerx += 3 + 36 * ((positions[zz][1] - 1) % 2)
                else:
                    playery = 586
                    playerx += 1 + 39 * ((positions[zz][1] - 1) % 2)
            elif self.players[zz].place == 12:  # electric company
                if positions[zz][1] == 0:
                    playerx += 21
                    playery = 536
                elif positions[zz][1] in list(range(1, 3)):
                    playerx += 5 + 32 * ((positions[zz][1] + 1) % 2)
                    playery = 532
                elif positions[zz][1] in list(range(3, 5)):
                    playerx += 4 + 34 * ((positions[zz][1] + 1) % 2)
                    playery = 544
                elif positions[zz][1] in list(range(5, 7)):
                    playerx += 7 + 28 * ((positions[zz][1] + 1) % 2)
                    playery = 556
                else:
                    playerx += 9 + 24 * ((positions[zz][1] + 1) % 2)
                    playery = 566
            elif self.players[zz].place == 28:  # water works
                if positions[zz][1] == 0:
                    playerx += 20
                    playery = 531
                elif positions[zz][1] in list(range(1, 3)):
                    playerx += 10 + 20 * ((positions[zz][1] + 1) % 2)
                    playery = 531
                elif positions[zz][1] in list(range(3, 5)):
                    playerx += 2 + 36 * ((positions[zz][1] + 1) % 2)
                    playery = 538
                elif positions[zz][1] in list(range(5, 7)):
                    playerx += 2 + 10 * ((positions[zz][1] + 1) % 2)
                    playery = 568
                else:
                    playerx += 28 + 10 * ((positions[zz][1] + 1) % 2)
                    playery = 568
            elif self.players[zz].place == 38:  # super tax
                if positions[zz][1] == 0:
                    playerx += 21
                    playery = 554
                elif positions[zz][1] in list(range(1, 5)):
                    playerx += 4 + 34 * ((positions[zz][1] + 1) % 2)
                    playery = 544 + 10 * int(positions[zz][1] > 2)
                elif positions[zz][1] in list(range(5, 7)):
                    playerx += 7 + 28 * ((positions[zz][1] + 1) % 2)
                    playery = 567
                else:
                    playerx += 1 + 39 * ((positions[zz][1] + 1) % 2)
                    playery = 586

            else:
                if positions[zz][1] in list(range(0, 4)):
                    playerx = 431 + 19 * (positions[zz][1] % 2)
                    playery = 541 + 19 * int(positions[zz][1] > 1)
                elif positions[zz][1] in list(range(4, 8)):
                    playerx = 421
                    playery = 532 + 10 * (positions[zz][1] - 4)
                else:
                    playerx = 429
                    playery = 570

            if self.players[zz].place % 10 != 0 and self.players[zz].place < 40:
                if self.players[zz].place // 10 == 0:  # bottom
                    self.players[zz].coords = (playerx + 402, playery)
                elif self.players[zz].place // 10 == 1:  # left
                    self.players[zz].coords = (((- playery) % 598) - 8 + 402 - 1, playerx)
                elif self.players[zz].place // 10 == 3:  # right
                    self.players[zz].coords = (
                    playery + 402, 590 - playerx + 102 * ((self.players[zz].place % 10) - 5) - 3)
                else:  # top
                    self.players[zz].coords = (playerx + 102 * ((self.players[zz].place % 10) - 5) + 402, playery - 528)
                # note - this maths was annoying
            else:
                self.players[zz].coords = (playerx, playery)

    def displayplayers(self):
        for zz in self.players:
            window.blit(zz.img, zz.coords)

    def updatehouses(self):
        for setvar in range(0, len(self.sets)):
            if self.sets[setvar] != 0 and self.sets[setvar] != 5:
                self.houseimages[setvar] = pygame.image.load(relative + "assets\\board\\house" + str(self.sets[setvar]) + ".png")
                colourmask = pygame.Surface([10, 12])
                colourmask.fill(setinfo.gethousecolour(setvar=setvar))
                colourmask.set_alpha(100)
                for zf in range(0, self.sets[setvar]):
                    self.houseimages[setvar].blit(colourmask, (zf * 12, 0))
            elif self.sets[setvar] == 5:
                if setvar in [4, 5]:
                    self.houseimages[setvar] = pygame.image.load(relative + "assets\\board\\tophotel.png")
                else:
                    self.houseimages[setvar] = pygame.image.load(relative + "assets\\board\\hotel.png")
                colourmask = pygame.Surface(self.houseimages[setvar].get_size())
                colourmask.fill(setinfo.gethotelcolour(setvar=setvar))
                colourmask.set_alpha(100)
                self.houseimages[setvar].blit(colourmask, (0, 0))
            else:
                self.houseimages[setvar] = blankimage

            if setvar in [2, 3] and self.sets[setvar] != 0:
                self.houseimages[setvar] = pygame.transform.rotate(self.houseimages[setvar], -90)
            elif setvar in [6, 7] and self.sets[setvar] != 0:
                self.houseimages[setvar] = pygame.transform.rotate(self.houseimages[setvar], 90)

    def displayhouses(self):
        setspos = -1
        for setvar in self.sets:
            setspos += 1
            if setspos not in [4, 5]:
                for za in setinfo.houseblitpoints[setspos]:
                    if setvar == 5:
                        if setspos in [0, 1]:
                            window.blit(self.houseimages[setspos], (za[0], za[1] - 13))
                        elif setspos in [2, 3]:
                            window.blit(self.houseimages[setspos], (za[0], za[1]))
                        else:
                            window.blit(self.houseimages[setspos], (za[0] - 13, za[1] + 35))
                    else:
                        if setspos in [6, 7]:
                            window.blit(self.houseimages[setspos], [za[0], za[1] + 48 - setvar * 12])
                        else:
                            window.blit(self.houseimages[setspos], za)
            else:
                for za in setinfo.houseblitpoints[setspos]:
                    if setvar == 5:
                        window.blit(self.houseimages[setspos], (za[0] + 35, za[1] - 3))
                    else:
                        window.blit(self.houseimages[setspos], (za[0] + 48 - setvar * 12, za[1]))


class Menu:
    def __init__(self, name):
        self.active = False
        self.selected = -1
        self.counter = 0
        self.name = name
        self.base = pygame.image.load(relative + "assets\\menus\\" + self.name + "\\base.png").convert_alpha()
        try:
            self.winpos = nospaces(open(relative + "assets\\menus\\" + self.name + "\\pos.txt").readlines()[0]).split(",")
        except FileNotFoundError:
            self.winpos = ["0", "0"]
        for z in range(0, len(self.winpos)):
            self.winpos[z] = int(self.winpos[z])
        self.x1 = self.winpos[0]
        self.y1 = self.winpos[1]
        self.info = readmenu("menuinfo.txt", self.name)
        self.buttons = []
        self.txtboxes = []
        self.tickboxes = []
        self.toblit = []
        for z in range(0, len(self.info)):
            if "button" in self.info[z].name:
                self.buttons.append(self.info[z])
            elif "txtbox" in self.info[z].name:
                self.txtboxes.append(self.info[z])
            elif "tickbox" in self.info[z].name:
                self.tickboxes.append(self.info[z])
        self.x2 = self.x1 + toImage(self.base).size[0]
        self.y2 = self.y1 + toImage(self.base).size[1]
        self.dims = toImage(self.base).size

    def show(self, position=("a", "b")):
        if position != ("a" ,"b"):
            self.winpos = position
        self.active = True

    def update(self, position=("a", "b"), events=(), mousestate=(0, 0, 0)):
        if self.active:
            if position != ("a", "b"):
                self.winpos = position

            hidewin = False
            toshow = blankimage
            mousepos = pygame.mouse.get_pos()

            window.blit(self.base, self.winpos)

            for z in self.toblit:
                window.blit(z[0], z[1])
            self.toblit = []

            for z in range(0, len(self.info)):
                if self.info[z] in self.buttons and self.info[z].iscolliding(mousepos, self.winpos):
                    toshow = self.info[z]
                    if mousestate[0]:
                        self.info[z].pressed = True
                        if self.info[z].name == "button1":
                            hidewin = True

                elif self.info[z] in self.txtboxes:
                    if self.info[z].editable:
                        if self.info[z].iscolliding(mousepos, self.winpos) and mousestate[0] and not self.info[z].selected:
                            self.selected = z
                            self.info[z].selected = True
                            self.counter = 20
                            self.info[z].blink()
                        elif not self.info[z].iscolliding(mousepos, self.winpos) and mousestate[0] and self.info[z].selected:
                            self.selected = -1
                            self.info[z].selected = False
                            self.counter = 0
                            self.info[z].txt = self.info[z].txt.strip("|")
                            self.info[z].puttext()
                            self.info[z].drawtxt(self.winpos)

                        if self.info[z].selected and self.counter < 1:
                            self.counter = 20
                            self.info[z].blink()

                    self.info[z].drawtxt(self.winpos)

                elif self.info[z] in self.tickboxes:
                    if self.info[z].iscolliding(mousepos, self.winpos):
                        self.info[z].selected = True
                        if mousestate[0]:
                            self.info[z].toggle()
                    else:
                        self.info[z].selected = False

                    self.info[z].draw(self.winpos)

            if self.counter > 0:
                self.counter -= 1

            if hidewin:
                self.hide()

            if self.selected != -1:
                for item in events:
                    if item.type == pygame.KEYDOWN:
                        if item.unicode in self.info[self.selected].allowed:
                            self.info[self.selected].txt = self.info[self.selected].txt.strip("|") + item.unicode
                            self.info[self.selected].checklen()
                            self.info[self.selected].puttext()
                            self.info[self.selected].blink()
                            self.counter = 30
                        elif item.key == 8:
                            self.info[self.selected].txt = self.info[self.selected].txt.strip("|")[0:-1]
                            self.info[self.selected].puttext()
                            self.info[self.selected].blink()
                            self.counter = 30

            if toshow != blankimage:
                toshow.show(self.winpos)

    def hide(self):
        self.active = False
        self.selected = -1
        if self.buttons[0].pressed:
            global donepressed
            donepressed = self.name

    def reset(self):
        for za in self.txtboxes:
            za.txt = ""
            za.puttext()
        for za in self.buttons:
            za.pressed = False
        for za in self.tickboxes:
            za.checked = False


# ------------------------------------------------------------------------------------------------------------


class Button:
    def __init__(self, dims, name, menuname):
        self.name = name
        self.image = pygame.image.load(relative + "assets\\menus\\" + menuname + "\\" + name + ".png").convert_alpha()
        self.pressed = False
        self.dims = dims
        self.x1 = dims[0]
        self.y1 = dims[1]
        self.x2 = dims[2]
        self.y2 = dims[3]
        self.height = dims[3] - dims[1]
        self.width = dims[2] - dims[0]

    def iscolliding(self, position, menupos):
        if self.x1 < position[0] - menupos[0] < self.x2 and self.y1 < position[1] - menupos[1] < self.y2:
            return True
        return False

    def show(self, menupos):
        window.blit(self.image, (self.x1 + menupos[0], self.y1 + menupos[1], self.x2 + menupos[0], self.y2 + menupos[1]))


# ------------------------------------------------------------------------------------------------------------


class Txtbox:
    def __init__(self, dims, name):
        self.name = name
        self.txt = ""
        self.selected = False
        self.font = dims[-5]
        self.maxlen = int(dims[-4])

        self.allowed = dims[-3]
        if self.allowed == "int":
            self.allowed = []
            for ba in range(0, 10):
                self.allowed.append(str(ba))
        elif self.allowed == "abc":
            self.allowed = []
            self.allowed.append(" ")
            for ba in range(97, 123):
                self.allowed.append(chr(ba))
        elif self.allowed in ["1a", "a1"]:
            self.allowed = []
            self.allowed.append(" ")
            for ba in range(97, 123):
                self.allowed.append(chr(ba))
            for ba in range(0, 10):
                self.allowed.append(str(ba))
        else:
            self.allowed = list(dims[-3])

        self.editable = dims[-2]
        if "y" in self.editable:
            self.editable = True
        else:
            self.editable = False
        self.align = dims[-1]
        self.dims = dims[0:4]
        self.x1 = self.dims[0]
        self.y1 = self.dims[1]
        self.x2 = self.dims[2]
        self.y2 = self.dims[3]
        self.height = self.dims[3] - self.dims[1]
        self.width = self.dims[2] - self.dims[0]
        self.img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

    def iscolliding(self, position, menupos):
        if self.x1 < position[0] - menupos[0] < self.x2 and self.y1 < position[1] - menupos[1] < self.y2:
            return True
        return False

    def puttext(self, text=""):
        self.img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        if text == "":
            text = self.txt
        else:
            self.txt = text
        xpos = 0
        for ba in text:
            if ba == ".":
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\punkt.png")
            elif ba == "|":
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\line.png")
            elif ba == "$":
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\mm.png")
            elif ba == " ":
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\a.png")
            elif ba == "'":
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\apostraphe.png")
            else:
                character = Image.open(relative + "assets\\fonts\\" + self.font + "\\" + ba + ".png")
            if ba != " ":
                self.img.paste(character, (xpos, 0, xpos + character.size[0], character.size[1]), character)
            xpos += character.size[0] + 3
        self.img = self.img.crop(self.img.getbbox())

    def blink(self):
        if self.editable:
            if self.txt == self.txt.strip("|"):
                self.txt = self.txt + "|"
            else:
                self.txt = self.txt.strip("|")
            self.puttext()

    def drawtxt(self, menupos):
        if self.align == "r":
            window.blit(topygame(self.img), (self.x1 + self.width - self.img.size[0] + menupos[0] - 1, self.y1 + menupos[1]))
        elif self.align == "l":
            window.blit(topygame(self.img), (self.x1 + menupos[0], self.y1 + menupos[1]))
        else:
            window.blit(topygame(self.img), (self.x1 + self.width // 2 - self.img.size[0] // 2 + menupos[0], self.y1 + menupos[1]))

    def checklen(self):
        if len(self.txt.strip("|")) > self.maxlen:
            self.txt = self.txt.strip("|")[0:self.maxlen]


# ------------------------------------------------------------------------------------------------------------


class Tickbox:
    def __init__(self, dims, name, menuname):
        self.name = name
        self.checked = False
        self.selected = False
        self.on = pygame.image.load(relative + "assets\\menus\\" + menuname + "\\" + name + "\\on.png").convert_alpha()
        self.off = pygame.image.load(relative + "assets\\menus\\" + menuname + "\\" + name + "\\off.png").convert_alpha()
        self.onselect = pygame.image.load(relative + "assets\\menus\\" + menuname + "\\" + name + "\\onselect.png").convert_alpha()
        self.offselect = pygame.image.load(relative + "assets\\menus\\" + menuname + "\\" + name + "\\offselect.png").convert_alpha()
        self.dims = dims[0:4]
        self.x1 = dims[0]
        self.y1 = dims[1]
        self.x2 = dims[2]
        self.y2 = dims[3]
        self.height = dims[3] - dims[1]
        self.width = dims[2] - dims[0]

    def iscolliding(self, position, menupos):
        if self.x1 < position[0] - menupos[0] < self.x2 and self.y1 < position[1] - menupos[1] < self.y2:
            return True
        return False

    def toggle(self):
        self.checked = not self.checked

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def draw(self, menupos):
        if self.selected:
            if self.checked:
                window.blit(self.onselect, (self.x1 + menupos[0], self.y1 + menupos[1]))
            else:
                window.blit(self.offselect, (self.x1 + menupos[0], self.y1 + menupos[1]))
        else:
            if self.checked:
                window.blit(self.on, (self.x1 + menupos[0], self.y1 + menupos[1]))
            else:
                window.blit(self.off, (self.x1 + menupos[0], self.y1 + menupos[1]))


# ------------------------------------------------------------------------------------------------------------


def topygame(image):
    return (pygame.image.fromstring(image.tobytes("raw", "RGBA"), image.size, "RGBA")).convert_alpha()


def toImage(image):
    return Image.frombytes("RGBA", image.get_size(), pygame.image.tostring(image, "RGBA", False))


def nospaces(string):
    product = []
    for a in string:
        if a != " ":
            product.append(a)
    return "".join(product)


def getcontent(string):
    start = False
    end = False
    for aa in range(0, len(string)):
        if string[aa] == "(":
            start = aa
        elif string[aa] == ")":
            end = aa
    if not start or not end:
        return
    return string[start + 1:end]


def getname(string):
    point = False
    for ab in range(0, len(string)):
        if string[ab] == "=":
            point = ab
            break
    if not point:
        return
    return string[0:point]


def readmenu(txtfile, menuname):
    if ".txt" in txtfile:
        txtfile = open(relative + "assets\\menus\\" + menuname + "\\" + txtfile)
    else:
        txtfile = open(relative + "assets\\menus\\" + menuname + "\\" + txtfile + ".txt")
    txtfile = txtfile.readlines()
    data = []
    for ac in range(0, len(txtfile)):
        line = nospaces(txtfile[ac])
        if txtfile[ac][0] == "#":
            pass
        if txtfile[ac][0:6] == "txtbox":
            content = getcontent(line)
            content = content.split(",")
            for ad in range(0, 4):
                content[ad] = int(content[ad])
            data.append([getname(line), content])
        elif txtfile[ac][0:6] == "button":
            content = getcontent(line)
            content = content.split(",")
            for ad in range(0, 4):
                content[ad] = int(content[ad])
            data.append([getname(line), content])
        elif txtfile[ac][0:7] == "tickbox":
            content = getcontent(line)
            content = content.split(",")
            for ad in range(0, 4):
                content[ad] = int(content[ad])
            data.append([getname(line), content])

    for ae in range(0, len(data)):
        if "txtbox" in data[ae][0]:
            data[ae] = Txtbox(data[ae][1], data[ae][0])
        elif "button" in data[ae][0]:
            data[ae] = Button(data[ae][1], data[ae][0], menuname)
        elif "tickbox" in data[ae][0]:
            data[ae] = Tickbox(data[ae][1], data[ae][0], menuname)

    return data


def getobject(tosearch, term):
    for af in tosearch:
        if af.name == term:
            return af
    return


def getfromname(tosearch, term):
    for af in tosearch:
        if af[0] == term:
            return af
    return


def hextorgb(hexvalue):
    rgbvalue = []
    try:
        if hexvalue[0] == "#":
            hexvalue = hexvalue[1:]
    except IndexError:
        return 190, 235, 238
    hexvalue = hexvalue.lower()
    temp = 0
    for ag in range(0, 6):
        multiplier = ((ag + 1) % 2) * 15 + 1
        try:
            temp += int(hexvalue[ag]) * multiplier
        except ValueError:
            temp += (ord(hexvalue[ag]) - 87) * multiplier
        if multiplier == 1:
            rgbvalue.append(temp)
            temp = 0
    rgbvalue.append(255)
    return rgbvalue


def absolute(num):
    if num < 0:
        return - num
    return num


def hsltorgb(h, s, l):
    c = (1 - absolute(2 * l - 1)) * s
    n = c * (1 - absolute((h / 60) % 2 - 1))
    m = l - c / 2
    if 0 <= h < 60:
        rgb = (c, n, 0)
    elif 60 <= h < 120:
        rgb = (n, c, 0)
    elif 120 <= h < 180:
        rgb = (0, c, n)
    elif 180 <= h < 240:
        rgb = (0, n, c)
    elif 240 <= h < 300:
        rgb = (n, 0, c)
    else:
        rgb = (c, 0, n)
    return round((rgb[0]+m)*255), round((rgb[1]+m)*255), round((rgb[2]+m)*255), 255


def rgbtohsl(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    maximum = max([r, g, b])
    minimum = min([r, g, b])
    delta = maximum - minimum

    l = (maximum + minimum) / 2

    if delta == 0:
        h = 0
    elif maximum == r:
        h = 60 * (((g - b) / delta) % 6)
    elif maximum == g:
        h = 60 * ((b - r) / delta + 2)
    elif maximum == b:
        h = 60 * ((r - g) / delta + 4)

    if delta == 0:
        s = 0
    else:
        s = (delta / (1 - absolute(2 * l - 1)))

    return round(h), round(s * 100) / 100, round(l * 100) / 100


def everyitem(listtosearch, item):
    for gfh in listtosearch:
        if item != gfh:
            return False
    return True


# ------------------------------------------------------------------------------------------------------------

filepath = __file__
relative = ""
cut = 0
executable = True
for i in range(0, len(filepath)):
    if filepath[i] == "/" or filepath[i] == "\\":
        relative += "\\"
        cut = i + 1
        executable = False
    else:
        relative += filepath[i]
if executable:
    filepath = sys.executable
    relative = ""
    cut = 0
    for i in range(0, len(filepath)):
        if filepath[i] == "/" or filepath[i] == "\\":
            relative += "\\"
            cut = i + 1
        else:
            relative += filepath[i]

relative = relative[0:cut]

relative = "G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\"

# ------------------------------------------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
# pygame.mixer.music.load(relative + "music//track.wav")
# pygame.mixer.music.play()
# pygame.mixer.music.set_endevent()

window = pygame.display.set_mode((1000,598))# , pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
blankimage = topygame(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))

donepressed = False
menus = glob.glob(relative + "assets\\menus\\*")
for i in range(0, len(menus)):
    menus[i] = Menu(menus[i][len(relative) + 13:])
    if menus[i].name == "mainmenu":
        menus[i].show()
        menuactive = True

skip = 0
for i in range(0, len(menus)):
    if menus[skip].name != "overlay":
        menus.append(menus.pop(skip))
    else:
        skip = 1

running = True
setinfo = Setinfo()

bg = pygame.image.load(relative + "assets\\background.png").convert_alpha()
deck = []
setimgs = []
for i in range(0,36):
    deck.append(pygame.image.load(relative + "assets\\board\\" + str(i + i // 9 + 1) + ".png").convert_alpha())
for i in range(0, 8):
    setimgs.append(pygame.image.load(relative + "assets\\sets\\" + str(i) + ".png").convert_alpha())

overlays = glob.glob(relative + "assets\\board\\overlays\\*")
for i in range(0, len(overlays)):
    overlays[i] = [overlays[i][len(relative) + 22:-4], pygame.image.load(overlays[i]).convert_alpha()]


cardselect = 0
playernumber = 0
doubles = 0
playerlist = []
gameinfo = ""
counter = 0
moved = False
destination = -1
cardviewcurrent = 0
buildsetcurrent = 0
dicerollers = Diceroller((616, 264), 2, 120)


while running:
    eventlist = pygame.event.get()
    pos = pygame.mouse.get_pos()

    # if clock.get_fps() < 55 and clock.get_fps() != 0.0:
    #     print(clock.get_fps())

    if 403 < pos[0] < 998 and 2 < pos[1] < 595 and not menuactive:
        # if in boardspace and there's no menu up
        if not (471 < pos[0] < 930 and 69 < pos[1] < 528):
            # if not in middle boardspace
            if pos[1] > 529 and 471 < pos[0] < 930:
                cardselect = 8 - (pos[0] - 471) // 51
            elif 403 < pos[0] < 470 and 528 > pos[1] > 70:
                cardselect = 17 - (pos[1] - 69) // 51
            elif pos[1] < 68 and 471 < pos[0] < 930:
                cardselect = 18 + (pos[0] - 471) // 51
            elif 931 < pos[0] and 528 > pos[1] > 70:
                cardselect = 27 + (pos[1] - 69) // 51

    window.blit(bg, (0, 0))
    window.blit(deck[cardselect], (134, 252))

    if gameinfo != "":

        # diceroller logic

        if everyitem(dicerollers.state, "stop"):
            counter += 1
            if counter == 60:
                counter = 0
                if destination == -1 and not gameinfo.players[gameinfo.playerturn].jail:
                    destination = (gameinfo.players[gameinfo.playerturn].place + dicerollers.results[0] + dicerollers.results[1]) % 40
                elif destination == -1 and gameinfo.players[gameinfo.playerturn].jail and dicerollers.results[0] == dicerollers.results[1]:
                    gameinfo.players[gameinfo.playerturn].jail = False
                    destination = (10 + dicerollers.results[0] + dicerollers.results[1]) % 40
                elif destination == -1 and gameinfo.players[gameinfo.playerturn].jail and dicerollers.results[0] != dicerollers.results[1]:
                    gameinfo.players[gameinfo.playerturn].jail -= 1
                    if gameinfo.players[gameinfo.playerturn].jail == 0:
                        gameinfo.players[gameinfo.playerturn].jail = False

        if counter % 20 == 0 and destination != -1 and gameinfo.players[gameinfo.playerturn].place != destination and not moved:
            gameinfo.players[gameinfo.playerturn].place = (gameinfo.players[gameinfo.playerturn].place + 1) % 40
            gameinfo.updateplayerpos()

        if destination == gameinfo.players[gameinfo.playerturn].place:
            counter = 0
            destination = -1
            moved = True
            if dicerollers.results[0] == dicerollers.results[1] and doubles < 3:
                doubles += 1
                if doubles == 3:
                    gameinfo.players[gameinfo.playerturn].place = 40
                    gameinfo.players[gameinfo.playerturn].jail = 3
                    gameinfo.updateplayerpos()
                else:
                    moved = False
                    dicerollers.reset()

        # end

        if cardselect + 1 * (cardselect // 10 + 1) in gameinfo.mortgaged:
            window.blit(getfromname(overlays, "mortgaged")[1], (144, 340))  # that maths in the end is for the correction of the deck variable, as it doesn't contain corners

        gameinfo.displayplayers()
        gameinfo.displayhouses()

    mousedown = [False, False, False, False, False]
    for event in eventlist:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown[event.button - 1] = True

    # sorting out all the menus

    menuactive = False
    for i in menus:
        if i.name == "mainmenu" and getobject(i.buttons, "button2").pressed:
            i.hide()
            getobject(menus, "newgame").show()
            menuactive = True
            getobject(i.buttons, "button2").pressed = False
        elif i.name == "newgame":
            if getobject(i.buttons, "button1").pressed:
                i.hide()
                getobject(menus, "mainmenu").show()
                menuactive = True
                getobject(i.buttons, "button1").pressed = False
            elif getobject(i.buttons, "button2").pressed:
                i.hide()
                getobject(i.buttons, "button2").pressed = False
                try:
                    playernumber = int(getobject(i.txtboxes, "txtbox1").txt.strip("|"))
                except ValueError:
                    playernumber = 4
                playertotal = playernumber
                gamename = getobject(i.txtboxes, "txtbox2").txt.strip("|")
                bidrule = getobject(i.tickboxes, "tickbox1").checked
                parkrule = getobject(i.tickboxes, "tickbox2").checked
        elif i.name == "playersettings":
            if i.active:
                for x in i.buttons:
                    if x.pressed:
                        if x.name == "button11":
                            if getobject(i.txtboxes, "txtbox2").txt == "":
                                playerlist.append(Player(hextorgb(getobject(i.txtboxes, "txtbox3").txt), "player " + str(playertotal - playernumber)))
                            else:
                                try:
                                    playerlist.append(Player(hextorgb(getobject(i.txtboxes, "txtbox3").txt), getobject(i.txtboxes, "txtbox2").txt))
                                except IndexError:
                                    playerlist.append(Player(hextorgb("beebee"),getobject(i.txtboxes, "txtbox2").txt))
                        else:
                            if (30 + (int(x.name[6:]) - 3) * 40) % 360 == 70:
                                tempcolour = hsltorgb(60, 0.8, 0.5)
                                # getting a much nicer yellow
                            else:
                                tempcolour = hsltorgb((30 + (int(x.name[6:]) - 3) * 40) % 360, 0.8, 0.5)
                            if getobject(i.txtboxes, "txtbox2").txt == "":
                                playerlist.append(Player(tempcolour, "player " + str(playertotal - playernumber)))
                            else:
                                playerlist.append(Player(tempcolour, getobject(i.txtboxes, "txtbox2").txt))
                        i.hide()
                        break

                if len(playerlist) == playertotal:
                    gameinfo = Gamestate(playerlist, gamename, bidrule, parkrule)
                    if gameinfo.players[gameinfo.playerturn].name[-1] == "s":
                        getobject(getobject(menus, "overlay").txtboxes, "txtbox1").puttext(gameinfo.players[gameinfo.playerturn].name + "'")
                    else:
                        getobject(getobject(menus, "overlay").txtboxes, "txtbox1").puttext(gameinfo.players[gameinfo.playerturn].name + "'s")
                    getobject(getobject(menus, "overlay").txtboxes, "txtbox2").puttext("$" + str(gameinfo.players[gameinfo.playerturn].money))

            if playernumber > 0 and not i.active:
                playernumber -= 1
                i.reset()
                i.txtboxes[0].puttext(str(playertotal - playernumber))
                i.show()
                menuactive = True
        elif i.name == "cardview" and i.active:
            for x in i.buttons:
                if x.name == "button2" and x.pressed:
                    x.pressed = False
                    try:
                        cardviewcurrent = (cardviewcurrent - 1) % len(gameinfo.players[gameinfo.playerturn].cards)
                    except ZeroDivisionError:
                        selectedcard = blankimage

                elif x.name == "button3" and x.pressed:
                    x.pressed = False
                    try:
                        cardviewcurrent = (cardviewcurrent + 1) % len(gameinfo.players[gameinfo.playerturn].cards)
                    except ZeroDivisionError:
                        selectedcard = blankimage

                elif x.name == "button4" and x.pressed:
                    x.pressed = False
                    i.hide()
                    getobject(menus, "build").show()

                elif x.name == "button5" and x.pressed:
                    x.pressed = False
                    if selectedcard != blankimage:
                        if gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent] not in gameinfo.mortgaged:
                            gameinfo.players[gameinfo.playerturn].money += setinfo.propertycosts[gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent]] // 2
                            gameinfo.mortgaged.append(gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent])
                        else:
                            if gameinfo.players[gameinfo.playerturn].money >= round((setinfo.propertycosts[gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent]] // 2) * 1.1):
                                gameinfo.players[gameinfo.playerturn].money -= round((setinfo.propertycosts[gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent]] // 2) * 1.1)
                                gameinfo.mortgaged.remove(gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent])

                try:
                    selectedcard = deck[gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent] - 1 * (gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent] // 10 + 1)]  # that maths in the end is for the correction of the deck variable, as it doesn't contain corners
                except IndexError:
                    selectedcard = blankimage
                i.toblit.append([selectedcard, (i.x1 + 273, i.y1 + 123)])
                if selectedcard != blankimage:
                    if gameinfo.players[gameinfo.playerturn].cards[cardviewcurrent] in gameinfo.mortgaged:
                        i.toblit.append([getfromname(overlays, "mortgaged")[1], (i.x1 + 283, i.y1 + 211)])
        elif i.name == "build" and i.active:
            for x in i.buttons:
                if x.name == "button2" and x.pressed:
                    x.pressed = False
                    try:
                        buildsetcurrent = (buildsetcurrent - 1) % len(gameinfo.players[gameinfo.playerturn].sets)
                    except ZeroDivisionError:
                        selectedcard = blankimage
                elif x.name == "button3" and x.pressed:
                    x.pressed = False
                    try:
                        buildsetcurrent = (buildsetcurrent + 1) % len(gameinfo.players[gameinfo.playerturn].sets)
                    except ZeroDivisionError:
                        selectedcard = blankimage

                elif x.name == "button4" and x.pressed:
                    if gameinfo.players[gameinfo.playerturn].money >= setinfo.housecosts[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] and len(gameinfo.players[gameinfo.playerturn].sets) != 0 and gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] < 5:
                        gameinfo.players[gameinfo.playerturn].money -= setinfo.housecosts[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]]
                        gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] += 1
                    x.pressed = False
                    gameinfo.updatehouses()
                elif x.name == "button5" and x.pressed:
                    if len(gameinfo.players[gameinfo.playerturn].sets) != 0 and gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] > 0:
                        gameinfo.players[gameinfo.playerturn].money += round(setinfo.housecosts[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] * 0.9)
                        gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] -= 1
                    x.pressed = False
                    gameinfo.updatehouses()

            try:
                selectedcard = setimgs[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]]
            except IndexError:
                selectedcard = blankimage
            i.toblit.append([selectedcard, (i.x1 + 273, i.y1 + 123)])

            if len(gameinfo.players[gameinfo.playerturn].sets) != 0:
                if gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] == 0:
                    temptext2 = "zero houses"
                elif gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] == 1:
                    temptext2 = "one house"
                elif gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] == 2:
                    temptext2 = "two houses"
                elif gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] == 3:
                    temptext2 = "three houses"
                elif gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] == 4:
                    temptext2 = "four houses"
                else:
                    temptext2 = "one hotel"
                if gameinfo.sets[gameinfo.players[gameinfo.playerturn].sets[buildsetcurrent]] in [1, 5]:
                    temptext = "there is"
                else:
                    temptext = "there are"
            else:
                temptext = ""
                temptext2 = ""
            if getobject(i.txtboxes, "txtbox2").txt != temptext2:
                getobject(i.txtboxes, "txtbox1").puttext(temptext)
                getobject(i.txtboxes, "txtbox2").puttext(temptext2)

        if i.name == "overlay" and i.active:
            for x in i.buttons:
                if x.name == "button2" and x.pressed:
                    gameinfo.players[gameinfo.playerturn].cards = [1, 3, 5, 15, 25]
                    cardviewcurrent = 0
                    getobject(menus, "cardview").show()
                    x.pressed = False
                elif x.name == "button3" and x.pressed:
                    gameinfo.players[gameinfo.playerturn].sets = [0, 1, 2, 3, 4, 6]
                    buildsetcurrent = 0
                    getobject(menus, "build").show()
                    x.pressed = False
                elif x.name == "button5" and x.pressed and not dicerollers.rolled:
                    dicerollers.roll()
                    x.pressed = False

            if getobject(i.txtboxes, "txtbox2").txt != "$" + str(gameinfo.players[gameinfo.playerturn].money):
                getobject(i.txtboxes, "txtbox2").puttext("$" + str(gameinfo.players[gameinfo.playerturn].money))

        if i.active and i.name != "overlay":
            menuactive = True

    if not menuactive and not getobject(menus, "overlay").active:
        getobject(menus, "overlay").show()

    if not menuactive:
        dicerollers.update()

    for i in menus:
        i.update(events=eventlist, mousestate=mousedown)

    # aight we're done with that

    pygame.display.update()
    clock.tick(60)

    if donepressed == "mainmenu":
        getobject(menus, "mainmenu").show()
        try:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        except pygame.error:
            pygame.event.clear()
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    for event in eventlist:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                toImage(window).save("screenshot.png")
        # elif event.type == pygame.mixer.music.get_endevent():
        #     pygame.mixer.music.play()
