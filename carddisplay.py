import pygame

pygame.init()
clock = pygame.time.Clock()

filepath = __file__[:-15]
relative = ""
for i in range(0, len(filepath)):
    if filepath[i] == "/":
        relative += "\\"
    else:
        relative += filepath[i]

window = pygame.display.set_mode((1000,598))

running = True

bg = pygame.image.load("background.png")
deck = []
for i in range(0,36):
    deck.append(pygame.image.load(relative + r"\showcards\board" + "\\" + str(i) + ".png"))
cardselect = 0

while running:
    pos = pygame.mouse.get_pos()

    if 403 < pos[0] < 998 and 2 < pos[1] < 595:
        # if in boardspace
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
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
