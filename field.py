from conditions import Cond
from field_random_generator import generator


class game_field:
    def __init__(self, width: int = 10, height: int = 10, field=None):
        if not field:
            self._width, self.height = width, height
            self.game_map, self.health = generator.generate_map(width, height)
        else:
            self.game_map = field
            self.health = self.get_health_count()
            self._width, self.height = len(self.game_map), len(self.game_map)
        self.size = (self._width, self.height)

    def shoot(self, x: int, y: int):
        if 0 <= x < self._width and 0 <= y < self.height:
            if self.game_map[x][y] == Cond.HEALTHY:
                self.game_map[x][y] = Cond.HURT
                self.health -= 1
            elif self.game_map[x][y] != Cond.HURT:
                self.game_map[x][y] = Cond.MISS

    def get_health_count(self):
        h = 0
        for i in self.game_map:
            for j in i:
                if j == Cond.HEALTHY:
                    h += 1
        return h

    def game_is_lost(self):
        return self.health == 0

    def __str__(self):
        s = ''
        for i in range(self._width):
            s += ' '.join(map(str, map(int, self.game_map[i]))) + '\n'
        return s

