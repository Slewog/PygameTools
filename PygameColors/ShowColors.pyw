from pyperclip import copy
from sys import exit
import pygame as pg



GAP = 10
SIZE_X = 40
SIZE_Y = 35
y_offset = GAP
x_offset = GAP

screen_w = 0
screen_h = 0
screen_name = "Pygame Colors"

color_str_list = [color for color in pg.colordict.THECOLORS]
color_amount = len(color_str_list) - 1
color_list:list['Color'] = []


class Color:
    border_color = pg.Color('teal')

    def __init__(self, x: int, y: int, color: str) -> None:
        self.rect = pg.Rect(x, y, SIZE_X, SIZE_Y)
        self.color = pg.Color(color)
        self.color_name = color
        self.name_formatted = f"{screen_name} - {color}"
    
    def draw(self, display:pg.Surface) -> None:
        pg.draw.rect(display, self.color, self.rect)
        pg.draw.rect(display, self.border_color, self.rect, width=3, border_radius=2)

    def copy_name(self) -> None:
        copy(self.color_name)
    
    def hovered(self, mouse_pos:tuple[int, int]) -> bool:
        if self.rect.collidepoint(mouse_pos):
            return True
        
        return False


# Create all colors and calcule window size.
idx = 0
for y in range(20):
    if idx <= color_amount:
        for x in range(35):
            color_list.append(
                Color(x_offset, y_offset, color_str_list[idx])
            )
            x_offset += SIZE_X + GAP
            idx += 1

        y_offset += SIZE_Y + GAP

        if screen_w == 0: screen_w += x_offset

        x_offset = GAP
screen_h = y_offset

screen = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption(screen_name)
clock = pg.time.Clock()

screen.fill('thistle1')
for color in color_list:
    color.draw(screen)
pg.display.update()

while True:
    mouse_left_clicked, title_updated = False, False

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()

        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            mouse_left_clicked = not mouse_left_clicked

    mouse_pos = pg.mouse.get_pos()
    current_screen_name = pg.display.get_caption()[0]
    
    for color in color_list:
        if color.hovered(mouse_pos):
            title_updated = not title_updated
            
            if current_screen_name != color.name_formatted:
                current_screen_name = color.name_formatted
                pg.display.set_caption(color.name_formatted)

            if mouse_left_clicked:
                color.copy_name()
                mouse_left_clicked = not mouse_left_clicked
         
    if not title_updated and current_screen_name != screen_name:
        pg.display.set_caption(screen_name)
    
    clock.tick(15)