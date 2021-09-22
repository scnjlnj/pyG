#include "objs/map.h"
#include <iostream>

using namespace std;



int main(){
    // mm = MapManager()
    // m=mm.init_map(shape=(40,24))
    // mm.auto_fill_map(m)
    // m.show()
    // cv2.waitKey()
    // int a[]= {1,2,3,4,5};
    // int* b = new int[5]{5,2,3,4,5};
    // string c = "abbcd";
    // cout<<c;
    string inters[] = {"x", "w-1", "*", "x", "*", "w-1", "x", "x", "x"};
    bool rotates[] = {true,true,true,true,false,false,false,false};
    TileResource tr{"name1","1.png","#",inters,rotates};
    TileResource *p;
    p = &tr;
    int size=1;
    Tiles_and_size tiles = transform_to_tiles(p,size);
    MapManager mmg = {tiles.tiles,tiles.size};
    Map m1 = mmg.init_map(3,2);
    // getchar();
    return 0;
}