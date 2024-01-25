import argparse

import keyboardlayout as kl
import keyboardlayout.pygame as klp
import pygame as pg

from button import Button, BTN_CLICKED

grey = pg.Color('grey')
dark_grey = ~pg.Color('grey')

def get_keyboard(
    layout_name: kl.LayoutName,
    key_size: int,
    key_info: kl.KeyInfo
) -> klp.KeyboardLayout:
    keyboard_info = kl.KeyboardInfo(
        position=(0 if layout_name == kl.LayoutName.QWERTY else 15, 0),
        padding=2,
        color=~grey
    )
    letter_key_size = (key_size, key_size)  # width, height
    keyboard_layout = klp.KeyboardLayout(
        layout_name,
        keyboard_info,
        letter_key_size,
        key_info
    )
    return keyboard_layout

def run_until_user_closes_window(
    screen: pg.Surface,
    keyboard: klp.KeyboardLayout,
    key_size: int,
    released_key_info: kl.KeyInfo,
):
    pressed_key_info = kl.KeyInfo(
        margin=14,
        color=pg.Color('red'),
        txt_color=pg.Color('white'),
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//16, key_size//10)
    )

    center_x = screen.get_width() // 2
    
    buttons = [
        Button(
            (center_x - 125, keyboard.rect.bottom + 35),
            {'text': "AZERTY", 'action': "change_layout", 'target_layout': "azerty"}
        ),
        Button(
            (center_x + 50, keyboard.rect.bottom + 35),
            {'text': "QWERTY", 'action': "change_layout", 'target_layout': "qwerty"}
        ),
    ]

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
                break
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.hovered:
                        button.click()
                        break

            if event.type == BTN_CLICKED:
                layout = kl.LayoutName.QWERTY if event.target_layout == "qwerty" else kl.LayoutName.AZERTY_LAPTOP

                if keyboard.layout_name != layout:
                    pg.display.set_caption(f"Keyboard Layout - {
                        'QWERTY' if event.target_layout == 'qwerty' else 'AZERTY FR' 
                    }")
                    keyboard = get_keyboard(layout, key_size, released_key_info)

                    y_offset = -6 if layout == kl.LayoutName.QWERTY else 6
                    for button in buttons:
                        button.update_y_pos(y_offset)

            key = keyboard.get_key(event)
            if key is None:
                continue

            if event.type == pg.KEYDOWN:
                keyboard.update_key(key, pressed_key_info)
            elif event.type == pg.KEYUP:
                keyboard.update_key(key, released_key_info)
    
        screen.fill(grey)
        keyboard.draw(screen)
        mouse_pos = pg.mouse.get_pos()
        for button in buttons: button.render(screen, mouse_pos)
        pg.display.update()

    pg.display.quit()
    pg.quit()


def keyboard_example(layout_name: kl.LayoutName):
    pg.init()
    # block events that we don't want
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT, pg.MOUSEBUTTONDOWN, BTN_CLICKED])

    key_size = 60
    key_info = kl.KeyInfo(
        margin=15,
        color=grey,
        txt_color=dark_grey,
        txt_font=pg.font.SysFont('Arial', key_size//4),
        txt_padding=(key_size//16, key_size//10)
    )
    keyboard = get_keyboard(layout_name, key_size, key_info)

    screen = pg.display.set_mode(
        (keyboard.rect.width, keyboard.rect.height + 70))
    screen.fill(pg.Color('black'))
    pg.display.set_caption('Keyboard Layout - QWERTY')

    keyboard.draw(screen)
    pg.display.update()
    run_until_user_closes_window(screen, keyboard, key_size, key_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'layout_name',
        nargs='?',
        type=kl.LayoutName,
        default=kl.LayoutName.QWERTY,
        help='the layout_name to use'
    )
    args = parser.parse_args()
    keyboard_example(args.layout_name)