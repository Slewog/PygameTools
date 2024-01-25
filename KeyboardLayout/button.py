import sys
from os import path
import pygame as pg

from typing import Tuple, NewType
CustomUserEvent = NewType('UserEvent', int)

pg.init()
if not pg.font.get_init():
    pg.font.init()

pg.mixer.init()

MAIN_DIR = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
GUI_FONT = pg.font.SysFont('Arial', 18)
BTN_CLICKED = CustomUserEvent(pg.USEREVENT + 1)

TXT_CLR = ~pg.Color('grey')
TXT_HOVER_CLR = pg.Color('white')
BG_COLOR = pg.Color('grey')
BORDER_COLOR = TXT_CLR

class Button:
    TXT_OFFSET_Y = int(0)
    TXT_OFFSET_X = int(0)
    BORDER_SIZE = int(6)
    BORDER_RADIUS = int(3)
    WIDTH_GAP = int(15)
    HEIGHT_GAP = int(15)

    def __init__(self, pos, data) -> None:
        self.pressed = bool(False)
        self.hovered = bool(False)
        self.click_time = None
        self.data = data

        self.text_surf = GUI_FONT.render(data['text'], True, TXT_CLR)
        self.text_rect = self.text_surf.get_rect(center=(pos[0] + self.TXT_OFFSET_X, pos[1] + self.TXT_OFFSET_Y))

        self.background = pg.Rect(
            pos[0],
            pos[1],
            self.text_rect.width + self.WIDTH_GAP,
            self.text_rect.height + self.HEIGHT_GAP
        )
        self.background.center = pos

        self.border = pg.Rect(
            pos[0],
            pos[1],
            self.background.width + self.BORDER_SIZE,
            self.background.height + self.BORDER_SIZE
        )
        self.border.center = pos
    
    def update_y_pos(self, y_offset: int):
        self.text_rect.y += y_offset
        self.background.y += y_offset
        self.border.y += y_offset
    
    def check_hover(self, mouse_pos: Tuple[int, int]):
        collide = self.border.collidepoint(mouse_pos)

        if not self.hovered and collide:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            self.text_surf = GUI_FONT.render(self.data['text'], True, TXT_HOVER_CLR)
            self.hovered = not self.hovered
                
        if self.hovered and not collide:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.text_surf = GUI_FONT.render(self.data['text'], True, TXT_CLR)
            self.hovered = not self.hovered
    
    def check_click(self):
        if self.click_time is None: return
        
        clicked_time = pg.time.get_ticks() - self.click_time

        if clicked_time >= 200:
            pg.event.post(pg.event.Event(BTN_CLICKED, self.data))
            self.pressed = bool(False)
            self.click_time = None

    def click(self) -> None:
        if not self.hovered or self.pressed: return
        
        self.pressed = not self.pressed
        self.click_time = pg.time.get_ticks()
    
    def render(self, display_surf: pg.Surface, mouse_pos: Tuple[int, int]) -> None:
        self.check_hover(mouse_pos)
        self.check_click()

        pg.draw.rect(display_surf, BORDER_COLOR, self.border, border_radius=self.BORDER_RADIUS)
        pg.draw.rect(display_surf, BG_COLOR, self.background)
        display_surf.blit(self.text_surf, self.text_rect)

