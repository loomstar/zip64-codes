
from microbit import *
from random import randrange
import neopixel

def zip_plot(x, y, colour):
    zip_led[x+(y*8)] = (colour[0], colour[1], colour[2])

zip_led = neopixel.NeoPixel(pin0, 64)

class Snake():
    def __init__(self):
        self.length = 2
        self.direction = "down"
        self.head = (4, 4)
        self.tail = []

    def move(self):
        # extend tail
        self.tail.append(self.head)

        # check snake size
        if len(self.tail) > self.length - 1:
            self.tail = self.tail[-(self.length - 1):]
        print
        if self.direction == "left":
            self.head = ((self.head[0] - 1) % 8, self.head[1])
        elif self.direction == "right":
            self.head = ((self.head[0] + 1) % 8, self.head[1])
        elif self.direction == "up":
            self.head = (self.head[0], (self.head[1] - 1) % 8)
        elif self.direction == "down":
            self.head = (self.head[0], (self.head[1] + 1) % 8)

    def grow(self):
        self.length += 1

    def collides_with(self, position):
        return position == self.head or position in self.tail

    def draw(self):
        # draw head
        zip_plot(self.head[0], self.head[1], [5, 30, 20])
        zip_led.show()

        # draw tail
        for dot in reversed(self.tail):
            zip_plot(dot[0], dot[1], [20, 0, 0])
            zip_led.show()

class Fruit():
    def __init__(self):
        # place in a random position on the screen
        self.position = (randrange(0, 8), randrange(0, 8))

    def draw(self):
        zip_plot(self.position[0], self.position[1], [0, 20, 0])
        zip_led.show()

class Game():
    def __init__(self):
        self.player = Snake()
        self.place_fruit()

    def place_fruit(self):
        while True:
            self.fruit = Fruit()
            # check it's in a free space on the screen
            if not self.player.collides_with(self.fruit.position):
                break

    def handle_input(self):
        # change direction? (no reversing)
        if pin8.read_digital() == 0:
            if self.player.direction != "down":
                self.player.direction = "up"
        elif pin12.read_digital() == 0:
            if self.player.direction != "right":
                self.player.direction = "left"
        elif pin13.read_digital() == 0:
            if self.player.direction != "left":
                self.player.direction = "right"
        elif pin14.read_digital() == 0:
            if self.player.direction != "up":
                self.player.direction = "down"

    def update(self):
        # move snake
        self.player.move()

        # game over?
        if self.player.head in self.player.tail:
            self.game_over()

        # nom nom nom
        elif self.player.head == self.fruit.position:
            self.player.grow()
            # space for more fruit?
            if self.player.length < 8 * 8:
                self.place_fruit()
            else:
                self.game_over()

    def score(self):
        return self.player.length - 2

    def game_over(self):
        display.scroll("Score: %s" % self.score())
        reset()

    def draw(self):
        zip_led.clear()
        self.player.draw()
        self.fruit.draw()


game = Game()

# main game loop
while True:
    for t in range (0, 80):
        game.handle_input()
        sleep(5)
        if t == 79:
            game.update()
            game.draw()