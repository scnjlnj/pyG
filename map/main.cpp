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
    cout<<"inters"<<endl;
    int i;
    for (i=0;i<9;i++){
        cout<<tr.interface[i]<<",";
    }
    cout<<endl;
    cout<<"rotates"<<endl;
    for (i=0;i<8;i++){
        cout<<tr.rotate[i]<<",";
    }
    cout<<endl;
    // delete []b;
    getchar();
    return 0;
}