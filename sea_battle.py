import drawer
from field import game_field
import curses
import argparse
import pickle
import os
import dataclasses
from keys import Keys


@dataclasses
class Cursor:
    x: int
    y: int


def get_bot_shot_sequence(borders):
    positions = set()
    for i in range(borders[0]):
        for j in range(borders[1]):
            positions.add((i, j))
    while len(positions) != 0:
        yield positions.pop()


def save_game(fields):
    with open('save', 'wb') as save:
        pickle.dump(fields, save)


def load_game(file):
    if not os.path.exists(file):
        return None
    with open(file, 'rb') as save:
        return pickle.load(save)


def start_game(scr, size, save_file):
    drawer.window_set(size)

    field = None
    if not save_file == '':
        field = load_game(save_file)
        if field is not None:
            player_field = game_field(field=field[0])
            bot_field = game_field(field=field[1])
    elif save_file == '' or field is None:
        player_field = game_field(*size)
        bot_field = game_field(*size)

    cursor = Cursor(x=0, y=0)
    drawer.draw_game(scr, (player_field, bot_field), cursor)
    bot_choises = get_bot_shot_sequence(size)

    while True:
        key = scr.getch()
        drawer.clear_screen(scr)
        if key == curses.KEY_UP and cursor.x > 0:
            cursor.x -= 1
        elif key == curses.KEY_DOWN and cursor.x < field.width - 1:
            cursor.x += 1
        elif key == curses.KEY_RIGHT and cursor.y < field.height - 1:
            cursor.y += 1
        elif key == curses.KEY_LEFT and cursor.y > 0:
            cursor.y -= 1
        elif key == curses.KEY_F5:
            save_game((player_field.game_map, bot_field.game_map))
        elif key == curses.KEY_ENTER or key in [Keys.ENTER1, Keys.ESC_KEY2]:
            bot_field.shoot(cursor.x, cursor.y)
            player_field.shoot(*next(bot_choises))
        elif key == Keys.ESC_KEY1 or key == Keys.ESC_KEY2:
            break
        drawer.draw_game(scr, (player_field, bot_field), cursor)
        player_won = bot_field.game_is_lost()
        bot_won = player_field.game_is_lost()
        if bot_won or player_won:
            if player_won:
                s = 'You won'
            else:
                s = 'You lost'
            drawer.clear_screen(scr)
            drawer.draw_with_color(scr, (2, 2), s, 1)
            drawer.refresh_screen(scr)
            scr.getch()
            break


def create_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--width', '-w',
                            help='Game field width',
                            type=int, default=10)
    arg_parser.add_argument('--height', '-hg',
                            help='Game field height',
                            type=int, default=10)
    arg_parser.add_argument('--save', '-s',
                            help='Pickle file with saved map',
                            type=str, default='')
    return arg_parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()

    curses.wrapper(start_game, (namespace.height, namespace.width),
                   namespace.save)
