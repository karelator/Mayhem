# Import pygame with abbreviated alias
import pygame as pg

# Function to scale a image object so it covers the display without distortion
def scale_to_cover(img_obj, x, y):
    # If taller than original ratio
    if x / y <= img_obj.get_width() / img_obj.get_height():
        new_img = pg.transform.scale(img_obj, (y *  (img_obj.get_width() / img_obj.get_height()), y))
    # If wider than original ratio
    else:
        new_img = pg.transform.scale(img_obj, (x, x * (img_obj.get_height() / img_obj.get_width())))
    new_img.convert()
    return new_img

# Function to scale a image object so it fits within the display without distortion
def scale_to_fit(img_obj, x, y):
    # If taller than original ratio
    if x / y >= img_obj.get_width() / img_obj.get_height():
        new_img = pg.transform.scale(img_obj, (y *  (img_obj.get_width() / img_obj.get_height()), y))
    # If wider than original ratio
    else:
        new_img = pg.transform.scale(img_obj, (x, x * (img_obj.get_height() / img_obj.get_width())))
    new_img.convert()
    return new_img