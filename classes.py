# Import pygame with abbreviated alias
from typing import Any
import pygame as pg

class Element(pg.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # self.rect = rect

class Item(Element):
    def __init__(self, image):
        super().__init__(image)


class Movable_object(Element):
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

class Projectile(Movable_object):
    def __init__(self, image):
        super().__init__(image)

    def update(self):
        pass

class Platform(Item)
    def __init__(self, image):
        super().__init__(image)
    
    def update(self):
        pass