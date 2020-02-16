from conditions import Cond


class generator:
    @staticmethod
    def generate_map(width: int, height: int):
        import random as r
        field = [[Cond.EMPTY] * height for _ in range(width)]
        max_ship_size, health_count = generator.get_max_ship_size(width * height)

        for size in range(1, max_ship_size + 1):
            x, y = r.randint(0, width - 1), r.randint(0, height - 1)
            for _ in range(max_ship_size + 1 - size):
                while not generator.ship_set(field, (width, height), (x, y), size):
                    x, y = r.randint(0, width - 1), r.randint(0, height - 1)
        return field, health_count

    @staticmethod
    def get_max_ship_size(field_size):
        cur_size = 1
        health = 1
        ship_cell_count = field_size // 5 + 1
        while True:
            s = 0
            for i in range(1, cur_size + 2):
                s += i * (cur_size + 2 - i)
            if s >= ship_cell_count:
                break
            else:
                health = s
                cur_size += 1
        return cur_size, health

    @staticmethod
    def ship_set(field, field_size, position, size) -> bool:
        import random
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for direction in directions:
            res = generator.try_to_set(field, field_size, position, size, direction)
            if res:
                return True
        return False

    @staticmethod
    def try_to_set(field, field_size, position, size, direction) -> bool:
        x, y = position[0], position[1]
        width, height = field_size[0], field_size[1]
        if not 0 <= y + direction[1] * size <= height:
            return False
        if not 0 <= x + direction[0] * size < width:
            return False
        x1, x2 = min(x, x + direction[0] * (size - 1)), max(x, x + direction[0] * (size - 1))
        y1, y2 = min(y, y + direction[1] * (size - 1)), max(y, y + direction[1] * (size - 1))
        if generator.space_is_clear(field, (x1, y1), (x2, y2)):
            for i in range(max(0, x1 - 1), min(x2 + 2, width)):
                for j in range(max(y1 - 1, 0), min(y2 + 2, height)):
                    field[i][j] = Cond.BUSY
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    field[i][j] = Cond.HEALTHY
            return True
        return False

    @staticmethod
    def space_is_clear(field, position1, position2):
        res = True
        for i in range(position1[0], position2[0] + 1):
            for j in range(position1[1], position2[1] + 1):
                if field[i][j] == Cond.BUSY or field[i][j] == Cond.HEALTHY:
                    res = False
        return res