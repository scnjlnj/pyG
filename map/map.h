class Slot():
    x = None
    y = None
    z = None
    choice = None
    finish = None
    tile = None

    def __init__(self, x, y, z=None, choice=None):
        self.x = x
        self.y = y
        self.z = z
        self.choice = choice

    def __repr__(self):
        return f"<Slot:坐标{self.x},{self.y},{self.z}>"

    def is_border(self, x, y):
        return self.x == 0 or self.y == 0 or self.x == x - 1 or self.y == y - 1

    def get_direction_possible_interfaces(self, ind):
        if self.finish:
            return [self.tile.interface[ind]]
        ret = []
        for tile in self.choice:
            ret.append(tile.interface[ind])
        return list(set(ret))

    def refresh_choice(self, interface_info):
        if self.finish:
            return 0
        else:
            for ind, info in enumerate(interface_info):
                temp_s = set(info)
                if "*" in temp_s:
                    temp = []
                    for c in self.choice:
                        if c.interface[ind] != "x":
                            temp.append(c)
                else:
                    temp = []
                    for c in self.choice:
                        if c.interface[ind] == "*":
                            if len(temp_s) == 1 and "x" in temp_s:
                                continue
                            else:
                                temp.append(c)
                        elif c.interface[ind] in temp_s:
                            temp.append(c)
                self.choice = temp
            return len(self.choice)

    def random_confirm(self):
        ind = random.randint(0, len(self.choice) - 1)
        self.tile = self.choice[ind]
        self.finish = True
        self.choice.pop(ind)

    def comfirm_tile(self, tile):
        self.tile = tile
        self.finish = True
        self.choice = []


class Map():
    lenth = None
    width = None
    slots = None
    matrix = None

    def __init__(self, l, w, d=None, choice=None):
        self.lenth = l
        self.width = w
        self.slots = [Slot(x, y, choice=choice) for y in range(l) for x in range(w)]
        self.matrix = [[None for y in range(l)] for x in range(w)]
        for s in self.slots:
            self.matrix[s.x][s.y] = s

    @property
    def shape(self):
        return (self.width, self.lenth)

    @property
    def info(self):
        return self.lenth, self.width, self.slots

    @classmethod
    def create_from_data(cls, d):
        return cls(len(d[0]), len(d), d)

    @classmethod
    def create_from_map(cls, map_obj):
        return cls(*map_obj.info)

    @property
    def finish(self):
        for i in self.slots:
            if i.finish:
                continue
            else:
                return False
        return True

    def choose_lowentropy_slot(self):
        minchoiceslots = []
        min_lenth = float("inf")
        for s in self.slots:
            if s.finish:
                continue
            n = self.refresh_position_choice(s.x, s.y)
            if n == 0:
                raise AllAttemptFail
            else:
                if n == min_lenth:
                    minchoiceslots.append(s)
                elif n > min_lenth:
                    continue
                else:
                    min_lenth = n
                    minchoiceslots = [s]
        return random.choice(minchoiceslots)

    def auto_fill(self):
        while not self.finish:
            s = self.choose_lowentropy_slot()
            s.random_confirm()

    def get_position_slot(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.lenth:
            return self.matrix[x][y]
        else:
            return None

    def get_position_adjacent_slots(self, x, y):
        ret = []
        for xx in (x - 1, x, x + 1):
            for yy in (y - 1, y, y + 1):
                ret.append(self.get_position_slot(xx, yy))
        return ret

    def get_position_interface_info(self, x, y):
        s = self.matrix[x][y]
        if s.finish:
            return None
        else:
            adjacent_slots = self.get_position_adjacent_slots(x, y)
            info = [None] * 9
            for ind, s in enumerate(adjacent_slots):
                info[ind] = s.get_direction_possible_interfaces(INTERFACE_RELATIVE_INDEX[ind])
            return info

    def refresh_position_choice(self, x, y):
        s = self.matrix[x][y]
        interface_info = self.get_position_interface_info(x, y)
        return s.refresh_choice(interface_info)

    def get_border_slots(self):
        return [s for s in self.slots if s.is_border(x=self.width, y=self.lenth)]

    def fill_borders(self, tile):
        border_slots = self.get_border_slots()
        for s in border_slots:
            s.comfirm_tile(tile)

    def show(self, str_out=False):
        if self.finish:
            if str_out:
                self.str_output()
            else:
                stack_img = N.vstack([N.hstack([s.tile.image for s in row]) for row in self.matrix])
                # cv2.imshow("img",stack_img)
                cv2.imwrite("out.png", stack_img)
        else:
            print("Not finish Yet")

    def str_output(self):
        for i in self.matrix:
            for s in i:
                print(s.tile.char_img, end="")
            print("")


class TileResource():
    name = None
    image = None
    char_img = None
    interface = [None] * 9  # 0-8 totally 9 directions , 4 is this tile self
    rotate = [None] * 8  # 0 is unchanged, 1-3 left,right,around, 4 is mirror, 5-7 are left,right,around to mirror

    @classmethod
    def DEFAULT_RESOURCES(cls):
        wall_c = TileResource()
        wall_c.name = "wall_c"
        wall_c.image = cv2.imread(os.path.join("res", "wall-c.png"))
        wall_c.char_img = "X"
        wall_c.interface = ["x", "w-1", "*", "x", "*", "w-1", "x", "x", "x"]
        wall_c.rotate = [True, True, True, True, False, False, False, False]
        wall = TileResource()
        wall.name = "wall"
        wall.image = cv2.imread(os.path.join("res", "wall.png"))
        wall.char_img = "+"
        wall.interface = ["*", "w-f", "*", "w-1", "*", "w-1", "x", "x", "x"]
        wall.rotate = [True, True, True, True, False, False, False, False]
        woods = TileResource()
        woods.name = "woods"
        woods.image = cv2.imread(os.path.join("res", "wood.png"))
        woods.char_img = "W"
        woods.interface = ["*"] * 9
        woods.rotate = [True] + [False] * 7
        blank = TileResource()
        blank.name = "blank"
        blank.image = cv2.imread(os.path.join("res", "blank.png"))
        blank.char_img = "·"
        blank.interface = ["*"] * 9
        blank.rotate = [True] + [False] * 7
        return [wall_c, wall, woods, blank]

    def __init__(self):
        pass

    def get_rotate_tile(self, rotate_state):
        img = self.rotate_img(rotate_state)
        inter = self.rotate_interface(rotate_state)
        return Tile(self.name, img, self.char_img, inter, rotate_state, self)

    def get_all_tile(self):
        return [self.get_rotate_tile(rotate_state) for rotate_state, b in enumerate(self.rotate) if b]

    def rotate_img(self, rotate_state):
        img = self.image
        if rotate_state == 0:
            pass
        elif rotate_state == 1:
            img = cv2.rotate(img, 2)
        elif rotate_state == 2:
            img = cv2.rotate(img, 0)
        elif rotate_state == 3:
            img = cv2.rotate(img, 1)
        elif rotate_state == 4:
            img = cv2.flip(img, 1)
        elif rotate_state == 5:
            img = cv2.flip(img, 1)
            img = cv2.rotate(img, 2)
        elif rotate_state == 6:
            img = cv2.flip(img, 1)
            img = cv2.rotate(img, 0)
        elif rotate_state == 7:
            img = cv2.flip(img, 1)
            img = cv2.rotate(img, 1)
        return img

    def rotate_interface(self, rotate_state):
        index_map = ROTATE_INDEX_MAP[rotate_state]
        interface = [""] * 9
        for ind, inte in enumerate(self.interface):
            interface[index_map[ind]] = inte
        return interface

    def __repr__(self):
        return f"<资源:{self.name}>"


class Tile(TileResource):
    resource = None
    rotate_state = None

    @classmethod
    def DEFAULT_TILES(cls):
        res = cls.DEFAULT_RESOURCES()
        ret = []
        for i in res:
            ret += i.get_all_tile()
        return ret

    def __init__(self, name, image, char_img, interface, rotate_state, resource):
        self.name = name
        self.resource = resource
        self.rotate_state = rotate_state
        self.image = image
        self.char_img = char_img
        self.interface = interface

    def __repr__(self):
        return f"<块:{self.name}-状态{self.rotate_state}>"


class MapManager():
    shape = DEFAULT_SHAPE
    tiles = Tile.DEFAULT_TILES()
    border = True

    def init_map(self, shape=None, tiles=None):
        if not shape:
            shape = self.shape
        if not tiles:
            tiles = self.tiles
        m = Map(*shape, choice=tiles)
        if self.border:
            self.fill_border(map=m, tile=None)
        return m

    def fill_border(self, map, tile=None):
        if not tile:
            tile = Tile("None", N.zeros((40, 40, 3)), "#", ["x"] * 9, None, None)
        map.fill_borders(tile)
        return map

    def auto_fill_map(self, m):
        try:
            m.auto_fill()
        except AllAttemptFail:
            print("tiles can not makeup a map")