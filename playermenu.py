import pygame
from PIL import Image
import glob


class Menu:
    def __init__(self, name):
        self.active = False
        self.selected = -1
        self.counter = 0
        self.name = name
        self.base = pygame.image.load(relative + "menus\\" + self.name + "\\base.png")
        try:
            self.winpos = nospaces(open(relative + "menus\\" + self.name + "\\pos.txt").readlines()[0]).split(",")
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

    def show(self, pos=("a", "b")):
        if pos != ("a" ,"b"):
            self.winpos = pos
        self.active = True

    def update(self, pos=("a", "b"), events=(), mousestate=(0, 0, 0)):
        if self.active:
            if pos != ("a", "b"):
                self.winpos = pos

            hidewin = False
            toshow = blankimage
            mousepos = pygame.mouse.get_pos()
            for z in range(0, len(self.info)):
                if self.info[z] in self.buttons and self.info[z].iscolliding(mousepos, self.winpos):
                    toshow = self.info[z]
                    if mousestate[0]:
                        self.info[z].pressed = True
                        if self.info[z].name == "button1":
                            hidewin = True

                if self.info[z] in self.txtboxes and self.info[z].iscolliding(mousepos, self.winpos) and mousestate[0] and not self.info[z].selected:
                    self.selected = z
                    self.info[z].selected = True
                    self.counter = 20
                    self.info[z].blink()

                elif self.info[z] in self.txtboxes and not self.info[z].iscolliding(mousepos, self.winpos) and mousestate[0] and self.info[z].selected:
                    self.selected = -1
                    self.info[z].selected = False
                    self.counter = 0
                    self.info[z].txt = self.info[z].txt.strip("|")
                    self.info[z].puttext()
                    self.info[z].drawtxt(self.winpos)

                elif self.info[z] in self.tickboxes:
                    if self.info[z].iscolliding(mousepos, self.winpos):
                        self.info[z].selected = True
                        if mousestate[0]:
                            self.info[z].toggle()
                    else:
                        self.info[z].selected = False

                if self.info[z] in self.txtboxes:
                    if self.info[z].selected and self.counter < 1:
                        self.counter = 20
                        self.info[z].blink()

            if self.counter > 0:
                self.counter -= 1

            if hidewin:
                self.hide()

            for item in events:
                if self.selected != -1 and item.type == pygame.KEYDOWN:
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

            window.blit(self.base, self.winpos)

            if toshow != blankimage:
                toshow.show(self.winpos)

            for z in self.txtboxes:
                z.drawtxt(self.winpos)

            for z in self.tickboxes:
                z.draw(self.winpos)

    def hide(self):
        self.active = False
        self.selected = -1
        if self.buttons[0].pressed:
            global donepressed
            donepressed = self.name


# ------------------------------------------------------------------------------------------------------------


class Button:
    def __init__(self, dims, name, menuname):
        self.name = name
        self.image = pygame.image.load(relative + "menus\\" + menuname + "\\" + name + ".png")
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
        self.font = dims[-3]
        self.maxlen = int(dims[-2])

        self.allowed = dims[-1]
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
            self.allowed = list(dims[-1])

        self.dims = dims[0:-1]
        self.x1 = self.dims[0]
        self.y1 = self.dims[1]
        self.x2 = self.dims[2]
        self.y2 = self.dims[3]
        self.height = self.dims[3] - self.dims[1]
        self.width = self.dims[2] - self.dims[0]
        self.img = Image.new("RGBA", (self.width - 2, self.height - 2), (0, 0, 0, 0))

    def iscolliding(self, position, menupos):
        if self.x1 < position[0] - menupos[0] < self.x2 and self.y1 < position[1] - menupos[1] < self.y2:
            return True
        return False

    def puttext(self, text=""):
        self.img = Image.new("RGBA", (self.width - 5, self.height - 5), (0, 0, 0, 0))
        if text == "":
            text = self.txt
        xpos = 0
        for ba in text:
            if ba == ".":
                character = Image.open(relative + "\\fonts\\" + self.font + "\\punkt.png")
            elif ba == "|":
                character = Image.open(relative + "\\fonts\\" + self.font + "\\line.png")
            elif ba == "$":
                character = Image.open(relative + "\\fonts\\" + self.font + "\\mm.png")
            elif ba == " ":
                character = Image.open(relative + "\\fonts\\" + self.font + "\\a.png")
            else:
                character = Image.open(relative + "\\fonts\\" + self.font + "\\" + ba + ".png")
            if ba != " ":
                self.img.paste(character, (xpos, 0, xpos + character.size[0], character.size[1]), character)
            xpos += character.size[0] + 3
        self.img = self.img.crop(self.img.getbbox())

    def blink(self):
        if self.txt == self.txt.strip("|"):
            self.txt = self.txt + "|"
        else:
            self.txt = self.txt.strip("|")
        self.puttext()

    def drawtxt(self, menupos):
        window.blit(topygame(self.img), (self.x1 + self.width - self.img.size[0] - 2 + menupos[0], self.y1 + 3 + menupos[1]))

    def checklen(self):
        if len(self.txt.strip("|")) > self.maxlen:
            self.txt = self.txt.strip("|")[0:self.maxlen]


# ------------------------------------------------------------------------------------------------------------


class Tickbox:
    def __init__(self, dims, name, menuname):
        self.name = name
        self.checked = False
        self.selected = False
        self.on = pygame.image.load(relative + "\\menus\\" + menuname + "\\" + name + "\\on.png")
        self.off = pygame.image.load(relative + "\\menus\\" + menuname + "\\" + name + "\\off.png")
        self.onselect = pygame.image.load(relative + "\\menus\\" + menuname + "\\" + name + "\\onselect.png")
        self.offselect = pygame.image.load(relative + "\\menus\\" + menuname + "\\" + name + "\\offselect.png")
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
    return pygame.image.fromstring(image.tobytes("raw", "RGBA"), image.size, "RGBA")


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
        txtfile = open(relative + "menus\\" + menuname + "\\" + txtfile)
    else:
        txtfile = open(relative + "menus\\" + menuname + "\\" + txtfile + ".txt")
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


# ------------------------------------------------------------------------------------------------------------

filepath = __file__
relative = ""
cut = 0
for i in range(0, len(filepath)):
    if filepath[i] == "/":
        relative += "\\"
        cut = i + 1
    else:
        relative += filepath[i]
relative = relative[0:cut]

# ------------------------------------------------------------------------------------------------------------

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
# pygame.mixer.music.load(relative + "music//track.wav")
# pygame.mixer.music.play()
# pygame.mixer.music.set_endevent()

blankimage = topygame(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
window = pygame.display.set_mode((1000,598))

donepressed = False
menus = glob.glob(relative + "menus\\*")
for i in range(0, len(menus)):
    menus[i] = Menu(menus[i][len(relative) + 6:])
    if menus[i].name == "mainmenu":
        menus[i].show()

running = True
menuactive = True

bg = pygame.image.load("background.png")
deck = []
for i in range(0,36):
    deck.append(pygame.image.load(relative + "showcards\\board\\" + str(i + i // 9 + 1) + ".png"))
cardselect = 0

while running:
    print(clock.get_fps())
    eventlist = pygame.event.get()
    pos = pygame.mouse.get_pos()

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

    # sorting out all the menus

    menuactive = False
    for i in menus:
        if i.name == "mainmenu" and getobject(i.buttons, "button2").pressed:
            i.hide()
            getobject(menus, "newgame").show()
            getobject(i.buttons, "button2").pressed = False
        elif i.name == "newgame" and getobject(i.buttons, "button1").pressed:
            i.hide()
            getobject(menus, "mainmenu").show()
            getobject(i.buttons, "button1").pressed = False
        if i.active:
            menuactive = True

    # aight we're done with that

    window.blit(bg, (0, 0))
    window.blit(deck[cardselect], (134, 252))

    mousedown = [False, False, False]
    for event in eventlist:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown[event.button - 1] = True

    for i in menus:
        i.update(events=eventlist, mousestate=mousedown)

    pygame.display.update()
    clock.tick(60)

    if donepressed == "mainmenu":
        try:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        except pygame.error:
            pygame.event.clear()
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    for event in eventlist:
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.mixer.music.get_endevent():
        #     pygame.mixer.music.play()
