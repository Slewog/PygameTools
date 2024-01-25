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

pg.init()


class ColorRect:
    border_color = pg.Color('teal')

    def __init__(self, x: int, y: int, color: str) -> None:
        self.rect = pg.Rect(x, y, SIZE_X, SIZE_Y)
        self.color = pg.Color(color)
        self.color_name = color
        self.name_formatted = f"{screen_name} - {color}"
    
    def draw(self, display:pg.Surface) -> None:
        pg.draw.rect(display, self.color, self.rect)
        pg.draw.rect(display, self.border_color, self.rect, width=3, border_radius=2)

    def copy_name(self):
        copy(self.color_name)
    
    def hovered(self, mouse_pos:tuple[int, int]) -> tuple[bool, str]:
        if self.rect.collidepoint(mouse_pos):
            return True
        
        return False


color_list:list[pg.Color] = [color for color in pg.colordict.THECOLORS]
color_amount = len(color_list) - 1
rect_clr_list:list[ColorRect] = []

idx = 0
for y in range(20):
    if idx <= color_amount:
        for x in range(35):
            rect_clr_list.append(ColorRect(x_offset, y_offset, color_list[idx]))

            x_offset += SIZE_X + GAP
            idx += 1
        
        y_offset += SIZE_Y + GAP

        if screen_w == 0:
            screen_w += x_offset
        x_offset = GAP

screen_h = y_offset

screen = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption(screen_name)
clock = pg.time.Clock()

screen.fill('black') # 'thistle1' or 'black'
for color_rect in rect_clr_list:
    color_rect.draw(screen)
pg.display.update()

while True:
    mouse_left_clicked = False

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()

        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            mouse_left_clicked = not mouse_left_clicked

    mouse_pos = pg.mouse.get_pos()
    title_updated = False
    current_screen_name = pg.display.get_caption()[0]
    
    for color_rect in rect_clr_list:
        if color_rect.hovered(mouse_pos):
            title_updated = True
            rect_hovered_name = color_rect.name_formatted

            if current_screen_name != rect_hovered_name:
                current_screen_name = color_rect.name_formatted
                pg.display.set_caption(rect_hovered_name)

            if mouse_left_clicked:
                color_rect.copy_name()
                mouse_left_clicked = not mouse_left_clicked
         
    if not title_updated and current_screen_name != screen_name:
        pg.display.set_caption(screen_name)
    
    title_updated = False
    
    clock.tick(15)