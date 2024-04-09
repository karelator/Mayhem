# Import pygame with abbreviated alias
import pygame as pg

class Item(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # self.rect = rect

class Movable_object(Item):
    def __init__(self, image):
        super().__init__(image)

    def update(self):
        pass

class Player(Movable_object):
    def __init__(self, image):
        super().__init__(image)

    def update(self):
        pass

class Asteroid(Movable_object):
    def __init__(self, image):
        super().__init__(image)

    def update(self):
        pass

