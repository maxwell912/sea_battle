import curses
from field import game_field
from conditions import Cond


def window_set(size):
    curses.curs_set(0)
    curses.resize_term(size[0] + 5, (size[1] + 2) * 2)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)


def draw_game(scr, fields, cursor):
    _draw_field(scr, fields[0], (0, fields[0].size[1] + 2), cursor, 1)
    _draw_field(scr, fields[1], (0, 0), cursor, 0)
    scr.refresh()


def _draw_field(scr, field: game_field,
                field_position, cursor_position, mode):
    x0, y0 = field_position
    size = field.size
    if mode == 1:
        scr.addstr(x0, y0, 'You')
    else:
        scr.addstr(x0, y0, "Bot")
    scr.addstr(x0 + 1, y0, 'HP: ' + str(field.health))
    x0 += 2
    _draw_rectangle(scr, (x0, y0), (x0 + size[0] + 1, y0 + size[1] + 1))
    x0, y0 = x0 + 1, y0 + 1
    cur_color = 1

    def draw_symbol(s, x, y):
        draw_with_color(scr, (x0 + x, y0 + y), s, cur_color)

    for x1, i in enumerate(field.game_map):
        for y1, j in enumerate(i):
            if [x1, y1] == cursor_position and mode == 0:
                cur_color = 2
            if j == Cond.HEALTHY and mode == 1:
                draw_symbol('O', x1, y1)
            elif j == Cond.MISS:
                draw_symbol('#', x1, y1)
            elif j == Cond.HURT:
                draw_symbol('X', x1, y1)
            else:
                draw_symbol(' ', x1, y1)
            cur_color = 1


def draw_with_color(scr, position, string, color):
    scr.attron(curses.color_pair(color))
    scr.addstr(*position, string)
    scr.attroff(curses.color_pair(color))


def refresh_screen(scr):
    scr.refresh()


def clear_screen(scr):
    scr.clear()


def _draw_rectangle(scr, position1, position2):
    for k in ((*position1, position1[0], position2[1]),
              (*position1, position2[0], position1[1]),
              (position1[0], position2[1], *position2),
              (position2[0], position1[1], *position2)):
        for i in range(k[0], k[2] + 1):
            for j in range(k[1], k[3] + 1):
                draw_with_color(scr, (i, j), ' ', 3)
