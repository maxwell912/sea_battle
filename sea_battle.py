from drawer import drawer
from field import game_field
import curses
import argparse
import pickle


def get_bot_shot_sequence(borders):
    s = set()
    for i in range(borders[0]):
        for j in range(borders[1]):
            s.add((i, j))
    while len(s) != 0:
        yield s.pop()


def save_game(fields):
    with open('save', 'wb') as save:
        pickle.dump(fields, save)


def load_game(file):
    with open(file, 'rb') as save:
        return pickle.load(save)


def start_game(scr, size, save_file):
    drawer.window_set(size)

    if save_file == '':
        player_field = game_field(*size)
        bot_field = game_field(*size)
    else:
        fields = load_game(save_file)
        player_field = game_field(field=fields[0])
        bot_field = game_field(field=fields[1])

    cursor = [0, 0]
    drawer.draw_game(scr, (player_field, bot_field), cursor)
    bot_choises = get_bot_shot_sequence(size)

    while True:
        key = scr.getch()
        drawer.clear_screen(scr)
        if key == curses.KEY_UP and cursor[0] > 0:
            cursor[0] -= 1
        elif key == curses.KEY_DOWN and cursor[0] < size[0] - 1:
            cursor[0] += 1
        elif key == curses.KEY_RIGHT and cursor[1] < size[1] - 1:
            cursor[1] += 1
        elif key == curses.KEY_LEFT and cursor[1] > 0:
            cursor[1] -= 1
        elif key == curses.KEY_F5:
            save_game([player_field.game_map, bot_field.game_map])
        elif key == curses.KEY_ENTER or key in [10, 13]:
            bot_field.shoot(*cursor)
            player_field.shoot(*next(bot_choises))
        elif key in [27, 113]:
            break
        drawer.draw_game(scr, (player_field, bot_field), cursor)
        if bot_field.game_is_lost() or player_field.game_is_lost():
            if bot_field.game_is_lost():
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
