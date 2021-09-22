#include <iostream>
#include <string.h>
#include <vector>
using namespace std;
// Class Slot():
//     x = None
//     y = None
//     z = None
//     choice = None
//     finish = None
//     tile = None
//     def __init__(self, x, y, z=None, choice=None):
//         self.x = x
//         self.y = y
//         self.z = z
//         self.choice = choice
//     def __repr__(self):
//         return f"<Slot:坐标{self.x},{self.y},{self.z}>"
//     def is_border(self, x, y):
//         return self.x == 0 or self.y == 0 or self.x == x - 1 or self.y == y - 1
//     def get_direction_possible_interfaces(self, ind):
//         if self.finish:
//             return [self.tile.interface[ind]]
//         ret = []
//         for tile in self.choice:
//             ret.append(tile.interface[ind])
//        return list(set(ret))
//     def refresh_choice(self, interface_info):
//         if self.finish:
//             return 0
//         else:
//             for ind, info in enumerate(interface_info):
//                 temp_s = set(info)
//                 if "*" in temp_s:
//                     temp = []
//                     for c in self.choice:
//                         if c.interface[ind] != "x":
//                             temp.append(c)
//                 else:
//                     temp = []
//                     for c in self.choice:
//                         if c.interface[ind] == "*":
//                             if len(temp_s) == 1 and "x" in temp_s:
//                                 continue
//                             else:
//                                 temp.append(c)
//                         elif c.interface[ind] in temp_s:
//                             temp.append(c)
//                 self.choice = temp
//             return len(self.choice)
//     def random_confirm(self):
//         ind = random.randint(0, len(self.choice) - 1)
//         self.tile = self.choice[ind]
//         self.finish = True
//         self.choice.pop(ind)
//     def comfirm_tile(self, tile):
//         self.tile = tile
//         self.finish = True
//         self.choice = []


// class Map():
//     lenth = None
//     width = None
//     slots = None
//     matrix = None
//     def __init__(self, l, w, d=None, choice=None):
//         self.lenth = l
//         self.width = w
//         self.slots = [Slot(x, y, choice=choice) for y in range(l) for x in range(w)]
//         self.matrix = [[None for y in range(l)] for x in range(w)]
//         for s in self.slots:
//             self.matrix[s.x][s.y] = s
//     @property
//     def shape(self):
//         return (self.width, self.lenth)
//     @property
//     def info(self):
//         return self.lenth, self.width, self.slots
//     @classmethod
//     def create_from_data(cls, d):
//         return cls(len(d[0]), len(d), d)
//     @classmethod
//     def create_from_map(cls, map_obj):
//         return cls(*map_obj.info)
//     @property
//     def finish(self):
//         for i in self.slots:
//             if i.finish:
//                 continue
//             else:
//                 return False
//         return True
//     def choose_lowentropy_slot(self):
//         minchoiceslots = []
//         min_lenth = float("inf")
//         for s in self.slots:
//             if s.finish:
//                 continue
//             n = self.refresh_position_choice(s.x, s.y)
//             if n == 0:
//                 raise AllAttemptFail
//             else:
//                 if n == min_lenth:
//                     minchoiceslots.append(s)
//                 elif n > min_lenth:
//                     continue
//                 else:
//                     min_lenth = n
//                     minchoiceslots = [s]
//         return random.choice(minchoiceslots)
//     def auto_fill(self):
//         while not self.finish:
//             s = self.choose_lowentropy_slot()
//             s.random_confirm()
//     def get_position_slot(self, x, y):
//         if 0 <= x < self.width and 0 <= y < self.lenth:
//             return self.matrix[x][y]
//         else:
//             return None
//     def get_position_adjacent_slots(self, x, y):
//         ret = []
//         for xx in (x - 1, x, x + 1):
//             for yy in (y - 1, y, y + 1):
//                 ret.append(self.get_position_slot(xx, yy))
//         return ret
//     def get_position_interface_info(self, x, y):
//         s = self.matrix[x][y]
//         if s.finish:
//             return None
//         else:
//             adjacent_slots = self.get_position_adjacent_slots(x, y)
//             info = [None] * 9
//             for ind, s in enumerate(adjacent_slots):
//                 info[ind] = s.get_direction_possible_interfaces(INTERFACE_RELATIVE_INDEX[ind])
//             return info
//     def refresh_position_choice(self, x, y):
//         s = self.matrix[x][y]
//         interface_info = self.get_position_interface_info(x, y)
//         return s.refresh_choice(interface_info)
//     def get_border_slots(self):
//         return [s for s in self.slots if s.is_border(x=self.width, y=self.lenth)]
//     def fill_borders(self, tile):
//         border_slots = self.get_border_slots()
//         for s in border_slots:
//             s.comfirm_tile(tile)
//     def show(self, str_out=False):
//         if self.finish:
//             if str_out:
//                 self.str_output()
//             else:
//                 stack_img = N.vstack([N.hstack([s.tile.image for s in row]) for row in self.matrix])
//                 # cv2.imshow("img",stack_img)
//                 cv2.imwrite("out.png", stack_img)
//         else:
//             print("Not finish Yet")
//     def str_output(self):
//         for i in self.matrix:
//             for s in i:
//                 print(s.tile.char_img, end="")
//             print("")


// class TileResource():
//     name = None
//     image = None
//     char_img = None
//     interface = [None] * 9  # 0-8 totally 9 directions , 4 is this tile self
//     rotate = [None] * 8  # 0 is unchanged, 1-3 left,right,around, 4 is mirror, 5-7 are left,right,around to mirror
//     @classmethod
//     def DEFAULT_RESOURCES(cls):
//         wall_c = TileResource()
//         wall_c.name = "wall_c"
//         wall_c.image = cv2.imread(os.path.join("res", "wall-c.png"))
//         wall_c.char_img = "X"
//         wall_c.interface = ["x", "w-1", "*", "x", "*", "w-1", "x", "x", "x"]
//         wall_c.rotate = [True, True, True, True, False, False, False, False]
//         wall = TileResource()
//         wall.name = "wall"
//         wall.image = cv2.imread(os.path.join("res", "wall.png"))
//         wall.char_img = "+"
//         wall.interface = ["*", "w-f", "*", "w-1", "*", "w-1", "x", "x", "x"]
//         wall.rotate = [True, True, True, True, False, False, False, False]
//         woods = TileResource()
//         woods.name = "woods"
//         woods.image = cv2.imread(os.path.join("res", "wood.png"))
//         woods.char_img = "W"
//         woods.interface = ["*"] * 9
//         woods.rotate = [True] + [False] * 7
//         blank = TileResource()
//         blank.name = "blank"
//         blank.image = cv2.imread(os.path.join("res", "blank.png"))
//         blank.char_img = "·"
//         blank.interface = ["*"] * 9
//         blank.rotate = [True] + [False] * 7
//         return [wall_c, wall, woods, blank]
//    def __init__(self):
//         pass
//     def get_rotate_tile(self, rotate_state):
//         img = self.rotate_img(rotate_state)
//         inter = self.rotate_interface(rotate_state)
//         return Tile(self.name, img, self.char_img, inter, rotate_state, self)
//     def get_all_tile(self):
//         return [self.get_rotate_tile(rotate_state) for rotate_state, b in enumerate(self.rotate) if b]
//     def rotate_img(self, rotate_state):
//         img = self.image
//         if rotate_state == 0:
//             pass
//         elif rotate_state == 1:
//             img = cv2.rotate(img, 2)
//         elif rotate_state == 2:
//             img = cv2.rotate(img, 0)
//         elif rotate_state == 3:
//             img = cv2.rotate(img, 1)
//         elif rotate_state == 4:
//             img = cv2.flip(img, 1)
//         elif rotate_state == 5:
//             img = cv2.flip(img, 1)
//             img = cv2.rotate(img, 2)
//         elif rotate_state == 6:
//             img = cv2.flip(img, 1)
//             img = cv2.rotate(img, 0)
//         elif rotate_state == 7:
//             img = cv2.flip(img, 1)
//             img = cv2.rotate(img, 1)
//         return img
//     def rotate_interface(self, rotate_state):
//         index_map = ROTATE_INDEX_MAP[rotate_state]
//         interface = [""] * 9
//         for ind, inte in enumerate(self.interface):
//             interface[index_map[ind]] = inte
//         return interface
//     def __repr__(self):
//         return f"<资源:{self.name}>"


// class Tile(TileResource):
//     resource = None
//     rotate_state = None
//     @classmethod
//     def DEFAULT_TILES(cls):
//         res = cls.DEFAULT_RESOURCES()
//         ret = []
//         for i in res:
//             ret += i.get_all_tile()
//         return ret
//     def __init__(self, name, image, char_img, interface, rotate_state, resource):
//         self.name = name
//         self.resource = resource
//         self.rotate_state = rotate_state
//         self.image = image
//         self.char_img = char_img
//         self.interface = interface
//     def __repr__(self):
//         return f"<块:{self.name}-状态{self.rotate_state}>"


// class MapManager():
//     shape = DEFAULT_SHAPE
//     tiles = Tile.DEFAULT_TILES()
//     border = True
//     def init_map(self, shape=None, tiles=None):
//         if not shape:
//             shape = self.shape
//         if not tiles:
//             tiles = self.tiles
//         m = Map(*shape, choice=tiles)
//         if self.border:
//             self.fill_border(map=m, tile=None)
//         return m
//     def fill_border(self, map, tile=None):
//         if not tile:
//             tile = Tile("None", N.zeros((40, 40, 3)), "#", ["x"] * 9, None, None)
//         map.fill_borders(tile)
//         return map
//     def auto_fill_map(self, m):
//         try:
//             m.auto_fill()
//         except AllAttemptFail:
//             print("tiles can not makeup a map")


class TileResource
{
private:
    string name="name";
    string image="./1.png";
    string char_img="#";

public:
    TileResource(string name, string image,string char_img,string* interface,bool* rotate);
    TileResource();
    ~TileResource();
    string* interface;  // 0-8 totally 9 directions , 4 is this tile self
    bool* rotate;  // 0 is unchanged, 1-3 left,right,around, 4 is mirror, 5-7 are left,right,around to mirror

};

TileResource::TileResource(string name, string image,string char_img,string* interface,bool* rotate)
{
    this->name=name;
    this->image=image;
    this->char_img=char_img;
    this->interface=interface;
    this->rotate=rotate;
}
TileResource::TileResource()
{
    cout<<"copy"<<endl;
}

TileResource::~TileResource()
{
    cout<<"delete"<<endl;

}

class Tile
{
private:
    TileResource *resource;
    int rotate_state;
public:
    Tile(TileResource &resource,int rotate_state){
        this->resource=&resource;
        this->rotate_state=rotate_state;
    }
    ~Tile() {
        // printf("tile destructor call");
    }
};
struct Tiles_and_size
{
    Tile **tiles;
    int size;
};

Tiles_and_size transform_to_tiles(TileResource *resource,int size_r){
    Tile* ret[1024];
    int size=0;
    for (int i = 0; i < size_r; i++)
    {
        for(int j=0;j<8;j++){
            if (resource[i].rotate[j]){
                ret[size++] = new Tile(resource[i],j);
            }
        }    
    }
    Tiles_and_size res = {ret,size};
    return res;
}
class Slot
{
private:
    int x; 
    int y;
    int z=0; 
    Tile *choice[1024];
    int choice_size; 
    bool finish; 
    Tile *tile; 
public:
    Slot(int x, int y,Tile **choice,int choice_size):x(x),y(y),choice_size(choice_size),finish(false) {
        for (int i=0;i<choice_size;i++){
            this->choice[i] = choice[i];
        }
    }
    Slot(){}
    ~Slot() {
        // printf("Slot-(%d,%d) destructor call\n",x,y);
    }
    void init(int x, int y,Tile **choice,int choice_size){
        this->x=x;
        this->y=y;
        this->finish=false;
        this->choice_size=choice_size;
        for (int i=0;i<choice_size;i++){
            this->choice[i] = choice[i];
        }
    }
    bool is_finish(){
        return finish;
    }
};
class Map
{
private:
    int lenth,width;
    vector<vector<Slot> > matrix;
    int max_entropy;
public:
    Map(int l,int w,Tile **choice,int tile_size) {
        matrix.resize(w,vector<Slot>(l,Slot()));
        max_entropy=tile_size;
        for (int i = l - 1; i >= 0; i--)
        {
            for (int j = w - 1; j >= 0; j--)
            {
                matrix[j][i].init(j,i,choice,tile_size);
            }
            
        }
    }
    ~Map() {

    }
    bool is_finish(){
        for (int i = lenth - 1; i >= 0; i--)
        {
            for (int j = width - 1; j >= 0; j--)
            {
                if(matrix[j][i].is_finish()){
                    continue;
                }
                else{
                    return false;
                }
            }
            
        }
        
        return true;
    }
    void auto_fill(bool border){
        while (!this->is_finish())
        {
            Slot &s = this->choose_lowentropy_slot();
            s.random_confirm();
        }
    }
    Slot &get_position_slot(int x,int y){
        return matrix[x][y];
    }
    Slot **get_position_adjacent_slots(int x,int y){
        Slot *ret[9];
        int xrange[3] = {x-1,x,x+1};
        int yrange[3] = {y-1,y,y+1};
        for (int i = 0; i <3; i++)
        {
            for (int j = 0; j<3; j++)
            {
                ret[3*i+j]=&matrix[i][j];
            }
        }
        return ret;
    }

    Slot &choose_lowentropy_slot(){
        int min_lenth = max_entropy;
        Slot *minslots[1024];
        int minslots_t=0;
        for (int i = lenth - 1; i >= 0; i--)
        {
            for (int j = width - 1; j >= 0; j--)
            {
                Slot &s=this->get_position_slot(j,i);
                if(s.is_finish()){continue;}
                int n = this->refresh_position_choice(j,i);
                if(n==0){throw "AllAttemptFail";}
                if (n==min_lenth)
                {
                    minslots[minslots_t++] = &s;
                }
                else if (n>min_lenth)
                {
                    continue;
                }
                else
                {
                    min_lenth = n;
                    minslots[0] = &s;
                    minslots_t = 1;
                }
            }
        }

        default_random_engine e;
        uniform_int_distribution<unsigned> u(0, 9);
    
        
        }
}
//     def choose_lowentropy_slot(self):
//         minchoiceslots = []
//         min_lenth = float("inf")
//         for s in self.slots:
//             if s.finish:
//                 continue
//             n = self.refresh_position_choice(s.x, s.y)
//             if n == 0:
//                 raise AllAttemptFail
//             else:
//                 if n == min_lenth:
//                     minchoiceslots.append(s)
//                 elif n > min_lenth:
//                     continue
//                 else:
//                     min_lenth = n
//                     minchoiceslots = [s]
//         return random.choice(minchoiceslots)
//     def auto_fill(self):
//         while not self.finish:
//             s = self.choose_lowentropy_slot()
//             s.random_confirm()
//     def get_position_slot(self, x, y):
//         if 0 <= x < self.width and 0 <= y < self.lenth:
//             return self.matrix[x][y]
//         else:
//             return None
//     def get_position_adjacent_slots(self, x, y):
//         ret = []
//         for xx in (x - 1, x, x + 1):
//             for yy in (y - 1, y, y + 1):
//                 ret.append(self.get_position_slot(xx, yy))
//         return ret
//     def get_position_interface_info(self, x, y):
//         s = self.matrix[x][y]
//         if s.finish:
//             return None
//         else:
//             adjacent_slots = self.get_position_adjacent_slots(x, y)
//             info = [None] * 9
//             for ind, s in enumerate(adjacent_slots):
//                 info[ind] = s.get_direction_possible_interfaces(INTERFACE_RELATIVE_INDEX[ind])
//             return info
//     def refresh_position_choice(self, x, y):
//         s = self.matrix[x][y]
//         interface_info = self.get_position_interface_info(x, y)
//         return s.refresh_choice(interface_info)
//     def get_border_slots(self):
//         return [s for s in self.slots if s.is_border(x=self.width, y=self.lenth)]
//     def fill_borders(self, tile):
//         border_slots = self.get_border_slots()
//         for s in border_slots:
//             s.comfirm_tile(tile)
//     def show(self, str_out=False):
//         if self.finish:
//             if str_out:
//                 self.str_output()
//             else:
//                 stack_img = N.vstack([N.hstack([s.tile.image for s in row]) for row in self.matrix])
//                 # cv2.imshow("img",stack_img)
//                 cv2.imwrite("out.png", stack_img)
//         else:
//             print("Not finish Yet")
//     def str_output(self):
//         for i in self.matrix:
//             for s in i:
//                 print(s.tile.char_img, end="")
//             print("")
};
class MapManager
{
private:
    int tile_size;
    Tile *tiles[1024];
public:
    MapManager(Tile** tiles,int tile_size);
    ~MapManager();
    Map init_map(int x,int y);
    void auto_fill_map(Map,bool);
};

MapManager::MapManager(Tile** tiles,int tile_size)
{
    for (int i=0;i<tile_size;i++){
            this->tiles[i] = tiles[i];
        }
    this->tile_size = tile_size;
}

MapManager::~MapManager()
{
    for (int i = tile_size - 1; i >= 0; i--)
    {
        delete tiles[i];
        // cout<<"Tile destuctor call\n";

    }
    // cout<<"MapManager destuctor call\n";
    
}
Map MapManager::init_map(int x, int y){
    Map map_ret = {x,y,tiles,tile_size};
    return map_ret;
}
void MapManager::auto_fill_map(Map m, bool border){
    m.auto_fill(border);

}