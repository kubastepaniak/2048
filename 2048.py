import sys
import pygame
import random
import copy


class griditem:
    """
    Grid item (single tile) class:
    Attributes: .index -> grid coordinate index
                .rect -> pygame.Rect()
                .value -> tile points value
                .surf -> tile image
                .xy -> tuple with onscreen coordinates
    Methods:    set_rect(spacing) -> assigns the attribute .rect
                double_value() -> doubles the value of a tile
                get_file() -> returns path to the tile's graphic
                set_surf() -> loads tile's image
                set_xy() -> assigns coordinates depending on grid index
    """

    def __init__(self, index):
        self.index = index
        self.rect = None
        self.value = None
        self.surf = None
        self.xy = None

    def set_rect(self, spacing):
        self.rect = pygame.Rect(spacing)

    def double_value(self):
        global score
        self.value = 2*self.value
        score = score + self.value

    def get_file(self):
        return 'graphics/' + str(self.value) + '.bmp'

    def set_surf(self, path=0):
        if path != 0:
            self.surf = pygame.image.load(path)

    def set_xy(self):
        x = self.index // 10
        y = self.index % 10
        for i, value in zip(range(1, 5), range(100, 600, 165)):
            if i == x:
                x = value
            if i == y:
                y = value
        self.xy = (y, x)

    isTaken = False


class text:
    """
    Text class:
    Attributes: -> at initialization sets it's
                   content, size, font, renders surface and sets rect
                -> .surf, .rect can be used for bliting
    """

    def __init__(self, content, color, xy, size=40):
        self.text = content
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.color = color
        self.surf = self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect()
        self.rect.center = xy

    def set_caption(self):
        self.font.render(self.text, True, self.color)


def show_grid():
    """
    Displays the grid with all tiles on the screen
    """

    for i in range(4):
        for j in range(4):
            tile = grid[i][j]
            if tile.isTaken is False:
                pygame.draw.rect(window, color['gridbg'], tile.rect)
            else:
                tile.set_surf(tile.get_file())
                window.blit(tile.surf, tile.rect)


def show_ui():
    """
    Prints on a screen user interface
    """

    scorevalue = text(str(score), color['caption'], (1175, 325))
    window.fill(color['background'])
    window.blit(title.surf, title.rect)
    window.blit(scoretext.surf, scoretext.rect)
    window.blit(scorevalue.surf, scorevalue.rect)
    window.blit(newgametext.surf, newgametext.rect)
    window.blit(quittext.surf, quittext.rect)
    show_grid()


def add_tile():
    """
    Adds a new tile to the free space on the board
    """

    freelist = []
    for i in range(4):
        for j in range(4):
            tile = grid[i][j]
            if tile.isTaken is False:
                freelist.append((i, j))

    rand = random.randint(0, len(freelist)-1)
    i, j = freelist[rand][0], freelist[rand][1]
    tile = grid[i][j]
    tile.isTaken = True

    rand = random.randint(0, 9)
    if rand == 0:
        tile.value = 4
    else:
        tile.value = 2


def shift(direction):
    """
    Shifts all tiles in the game screen in direction
    specified by the input: right, left, up or down.
    Returns True if any tile had moved
    or False if no move was possible
    """

    def change(x):
        """
        Specifies the incrementation or decrementation
        of given index depending on shift direction
        """

        if direction == 'right' or direction == 'down':
            return x-1
        if direction == 'left' or direction == 'up':
            return x+1

    jlist, klist, ilist = [], [], []
    if direction == 'right' or direction == 'down':
        jlist.extend(reversed(range(3)))
        ilist.extend(range(4))
        if direction == 'down':
            swap = ilist
            ilist = jlist
            jlist = swap
    if direction == 'left' or direction == 'up':
        jlist.extend(range(1, 4))
        ilist.extend(range(4))
        if direction == 'up':
            swap = ilist
            ilist = jlist
            jlist = swap

    check = False
    if direction == 'right' or direction == 'left':
        for j in jlist:
            if direction == 'right':
                klist.extend(range(j+1, 4))
            if direction == 'left':
                klist.extend(reversed(range(j)))
            for k in klist:
                for i in ilist:
                    if grid[i][change(k)].isTaken:
                        t1start = copy.deepcopy(grid[i][change(k)])
                        t1end = copy.deepcopy(grid[i][k])
                        t1start.set_surf(t1start.get_file())
                        if t1start.isTaken and not t1end.isTaken:
                            grid[i][change(k)].isTaken = False
                            t1start = moveboxto(t1start, (t1end.rect[0],
                                                          t1end.rect[1]))
                            grid[i][k] = t1start
                            show_grid()
                            check = True
    if direction == 'up' or direction == 'down':
        for i in ilist:
            if direction == 'down':
                klist.extend(range(i+1, 4))
            if direction == 'up':
                klist.extend(reversed(range(i)))
            for k in klist:
                for j in jlist:
                    if grid[change(k)][j].isTaken:
                        t1start = copy.deepcopy(grid[change(k)][j])
                        t1end = copy.deepcopy(grid[k][j])
                        t1start.set_surf(t1start.get_file())
                        if t1start.isTaken and not t1end.isTaken:
                            grid[change(k)][j].isTaken = False
                            t1start = moveboxto(t1start, (t1end.rect[0],
                                                          t1end.rect[1]))
                            grid[k][j] = t1start
                            show_grid()
                            check = True
    return check


def moveboxto(box, loc):
    """
    Moves input object "box" to input location "loc"
    """

    xVec = (loc[0] - box.rect.topleft[0]) / 10
    yVec = (loc[1] - box.rect.topleft[1]) / 10
    if box.rect.topleft[0] < loc[0] and box.rect.topleft[1] == loc[1]:
        direction = 'right'
    elif box.rect.topleft[0] > loc[0] and box.rect.topleft[1] == loc[1]:
        direction = 'left'
    elif box.rect.topleft[1] > loc[1] and box.rect.topleft[0] == loc[0]:
        direction = 'up'
    elif box.rect.topleft[1] < loc[1] and box.rect.topleft[0] == loc[0]:
        direction = 'down'

    while check_condition(box.rect.topleft, loc, direction):
        box.rect = box.rect.move([xVec, yVec])
        window.fill(color['background'])
        show_ui()
        window.blit(box.surf, box.rect)
        pygame.display.flip()
    box.rect.topleft = loc
    return box


def check_condition(box, loc, direction):
    """
    Checks movement boundary conditions
    """

    if direction == 'right':
        if box[0] > loc[0]:
            return False
    if direction == 'left':
        if box[0] < loc[0]:
            return False
    if direction == 'up':
        if box[1] < loc[1]:
            return False
    if direction == 'down':
        if box[1] > loc[1]:
            return False
    return True


def movetextto(text, loc):
    """
    Moves input text to input location "loc"
    """

    xVec = (loc[0] - text.rect.center[0]) / 100

    if loc[0] > text.rect.center[0]:
        while text.rect.center[0] < loc[0]:
            text.rect = text.rect.move([xVec, 0])
            window.fill(color['background'])
            window.blit(text.surf, text.rect)
            pygame.display.flip()
    else:
        while text.rect.center[0] > loc[0]:
            text.rect = text.rect.move([xVec, 0])
            window.fill(color['background'])
            window.blit(text.surf, text.rect)
            pygame.display.flip()
    return text


def merge_possible(direction):
    """
    Returns False if no merge is possible
    in input direction or True if it is
    """

    def change(x):
        """
        Specifies the incrementation or decrementation
        of given index depending on shift direction
        """

        if direction == 'right' or direction == 'down':
            return x-1
        if direction == 'left' or direction == 'up':
            return x+1

    klist = []
    if direction == 'right' or direction == 'down':
        klist.extend(reversed(range(1, 4)))
    if direction == 'left' or direction == 'up':
        klist.extend(range(3))

    if direction == 'right' or direction == 'left':
        for i in range(4):
            for j in klist:
                if (grid[i][j].isTaken and
                   grid[i][change(j)].isTaken and
                   grid[i][j].value == grid[i][change(j)].value):
                    return True
        return False
    if direction == 'up' or direction == 'down':
        for j in range(4):
            for i in klist:
                if (grid[i][j].isTaken and
                   grid[change(i)][j].isTaken and
                   grid[i][j].value == grid[change(i)][j].value):
                    return True
        return False


def merge_where(direction):
    """
    Returns tuple ((x1, y1), (x2, y2)) with coordinates
    of possible merge in given direction
    """

    def change(x):
        """
        Specifies the incrementation or decrementation
        of given index depending on shift direction
        """

        if direction == 'right' or direction == 'down':
            return x-1
        if direction == 'left' or direction == 'up':
            return x+1

    klist = []
    if direction == 'right' or direction == 'down':
        klist.extend(reversed(range(1, 4)))
    if direction == 'left' or direction == 'up':
        klist.extend(range(3))

    if direction == 'right' or direction == 'left':
        for i in range(4):
            for j in klist:
                if (grid[i][j].isTaken and
                   grid[i][change(j)].isTaken and
                   grid[i][j].value == grid[i][change(j)].value):
                    return ((i, change(j)), (i, j))
    if direction == 'up' or direction == 'down':
        for j in range(4):
            for i in klist:
                if (grid[i][j].isTaken and
                   grid[change(i)][j].isTaken and
                   grid[i][j].value == grid[change(i)][j].value):
                    return ((change(i), j), (i, j))


def merge(blocks):
    """
    Merges two blocks into one with doubled value
    """

    first, second = blocks[0], blocks[1]
    firstid = (first[0]+1)*10 + first[1]+1
    secondid = (second[0]+1)*10 + second[1]+1
    copiedfirst, copiedsecond = griditem(0), griditem(0)

    copiedfirst = copy.deepcopy(grid[first[0]][first[1]])
    copiedsecond = copy.deepcopy(grid[second[0]][second[1]])
    copiedfirst.index, copiedsecond.index = firstid, secondid
    copiedfirst.set_xy()
    copiedsecond.set_xy()
    copiedfirst.set_surf(copiedsecond.get_file())

    grid[first[0]][first[1]].isTaken = False
    moveboxto(copiedfirst, copiedsecond.xy)
    grid[second[0]][second[1]].double_value()


def keyaction(key):
    """
    Executes commands for input key.
    """

    if key == pygame.K_q:
        sys.exit()
    if key == pygame.K_n:
        newgame()

    direction = controls[key]

    if shift(direction) or merge_possible(direction):
        while merge_possible(direction):
            merge(merge_where(direction))
        shift(direction)
        add_tile()


def newgame():
    """
    Sets up game start state and returns to welcome screen
    """

    global score, title, scoretext, state
    score = 0
    for i in range(4):
        for j in range(4):
            grid[i][j].isTaken = False
            grid[i][j].value = 2
    title.rect.center = (700, 225)
    scoretext.rect.center = (1050, 325)
    state = 'game'
    welcome_screen()
    add_tile()
    add_tile()


def welcome_screen():
    """
    Display of welcome screen
    """

    global title
    window.fill(color['background'])
    window.blit(title.surf, title.rect)
    window.blit(guide.surf, guide.rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    title = movetextto(title, (1090, 225))


def success():
    """
    Returns true if the win condition is satisfied,
    otherwise returns False
    """

    for i in range(4):
        for j in range(4):
            if grid[i][j].value == 2048:
                return True
    return False


def fail():
    """
    Returns true if the game failed, otherwise failse
    """

    counter = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j].isTaken:
                counter = counter + 1

    if (not merge_possible('right') and not merge_possible('left') and
       not merge_possible('up') and not merge_possible('down') and
       counter == 16):
        return True
    return False


def success_screen():
    """
    Display of the success screen
    """

    global title, scorevalue, scoretext, score
    if not init:
        pygame.time.delay(500)
        title = movetextto(title, (700, 255))
        scorevalue = text(str(score), color['caption'], (785, 325))
        scoretext.rect.center = (640, 325)
    items = [title, scoretext, scorevalue, wintext, quittext, newgametext]
    window.fill(color['background'])
    for i in range(len(items)):
        window.blit(items[i].surf, items[i].rect)


def fail_screen():
    """
    Display of the fail screen
    """

    global title, scorevalue, scoretext, score
    if not init:
        pygame.time.delay(500)
        title = movetextto(title, (700, 255))
        scorevalue = text(str(score), color['caption'], (785, 325))
        scoretext.rect.center = (640, 325)
    items = [title, scoretext, scorevalue, failtext, quittext, newgametext]
    window.fill(color['background'])
    for i in range(len(items)):
        window.blit(items[i].surf, items[i].rect)


def gamestate(p):
    """
    Executes given game state
    """
    global state, init
    if p == 'game':
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyaction(event.key)
        show_ui()
        pygame.display.flip()
        if success():
            init = False
            state = 'win'
        if fail():
            init = False
            state = 'fail'

    if state == 'win':
        success_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_n:
                    newgame()
                    init = True

    if state == 'fail':
        fail_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_n:
                    newgame()
                    init = True


def showtaken():
    """
    Prints in the console the grid with isTaken attribute of each cell
    """

    for i in range(4):
        a = []
        for j in range(4):
            a.append(grid[i][j].isTaken)
        print(a)
    print("/")


def showobj(x):
    """
    Prints in the console attributes of input "tile" object
    """

    a = []
    a.extend([x.index, x.rect, x.xy, x.surf, x.value, x.isTaken])
    print(a)


pygame.init()
window = pygame.display.set_mode((1400, 850))
arena = window.get_rect()

color = {'caption': (85, 55, 0),
         'background': (230, 200, 150),
         'gridbg': (200, 150, 90)}

controls = {pygame.K_RIGHT: 'right',
            pygame.K_LEFT: 'left',
            pygame.K_DOWN: 'down',
            pygame.K_UP: 'up',
            pygame.K_n: 'newgame'}

# tiles declaration and grid setup
square = (150, 150)

a1, a2, a3, a4 = griditem(11), griditem(12), griditem(13), griditem(14)
b1, b2, b3, b4 = griditem(21), griditem(22), griditem(23), griditem(24)
c1, c2, c3, c4 = griditem(31), griditem(32), griditem(33), griditem(34)
d1, d2, d3, d4 = griditem(41), griditem(42), griditem(43), griditem(44)

grid = ([a1, a2, a3, a4],
        [b1, b2, b3, b4],
        [c1, c2, c3, c4],
        [d1, d2, d3, d4])

for i, yconst in zip(range(4), range(100, 600, 165)):
    for j, value in zip(range(4), range(100, 600, 165)):
        grid[i][j].set_rect(((value, yconst), square))
        grid[i][j].xy = (value, yconst)

score = 0
# texts setup
title = text('2048', color['caption'], (700, 225), 125)
scoretext = text('Score:', color['caption'], (1050, 325))
scorevalue = text(str(score), color['caption'], (1175, 325))
guide = text('Use arrow keys to merge tiles and get 2048!',
             color['caption'], (700, 450))
wintext = text('Congratulations! You have completed 2048 puzzle!',
               color['caption'], (700, 450))
failtext = text('You failed! No space left and no merging possible. Try again',
                color['caption'], (700, 450))
newgametext = text('Press "N" to start new game', color['caption'],
                   (1090, 500), 30)
quittext = text('Press "Q" to quit the game', color['caption'],
                (1090, 550), 30)


# main game
state = 'game'
init = True
newgame()

while True:
    gamestate(state)
