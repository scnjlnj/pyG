#include <iostream>
#include <vector> 
#include <random>
using namespace std;
class Rect
{
private:
    int lenth,width;
    string name="defalut";
public:
    Rect():lenth(1),width(1){cout<<"Default construct...\n";};
    Rect(int lenth,int width,string);
    ~Rect();
    Rect(const Rect & c){
        lenth = c.lenth; width = c.width;name = c.name;
        cout<<"copy_from "<<&c<<"\t" ;
        cout<<"Copy Constructor called"<<"I am "<<this<<endl ;
    }
    int getArea();
    int getPerimeter();
};

Rect::Rect(int lenth,int width,string name)
{
    this->lenth=lenth;
    this->width=width;
    this->name=name;
    cout<<name<<"\t"<<this<<"\t";
    cout<<"construct....\n";
}

Rect::~Rect()
{
    cout<<name<<"\t"<<this<<"\t";
    cout<<"destruct....\n";
}
int Rect::getArea(){
    int ret = lenth*width;
    // cout<<"area is "<<ret<<endl;
    return ret;
}
int Rect::getPerimeter(){
    int ret = (lenth+width)*2;
    // cout<<"perimeter is "<<ret<<endl;
    return ret;
}
 
int main( ){
    // auto seed = chrono::high_resolution_clock::now().time_since_epoch().count();
    // default_random_engine e(seed);
    // uniform_int_distribution<unsigned> u(0, 9);
    // 一般性：rand() % (b-a+1)+ a ;    就表示  a~b 之间的一个随机整数。
    for(int i=0; i<10; ++i)
        cout<<rand()*10/32767<<endl;
    return 0;
}
    
    // vector<vector<Rect> > rects(w,vector<Rect>(l,Rect(2,3,"2_3_rect")));
    // Rect *temp = &rects[0][0];
    // cout<<"area,perimeter:"<<temp->getArea()<<","<<temp->getPerimeter()<<temp<<endl;
    // rects[0][0]=Rect(4,6,"4_6_rect");
    // cout<<rects.size()<<endl;
    // cout<<"area,perimeter:"<<rects[0][0].getArea()<<","<<rects[0][0].getPerimeter()<<&rects[0][0]<<endl;
    // cout<<"area,perimeter:"<<rects[1][0].getArea()<<","<<rects[1][0].getPerimeter()<<endl;
    // cout<<"area,perimeter:"<<temp->getArea()<<","<<temp->getPerimeter()<<temp<<endl;


    // cin>>l;
    // cin>>w;
    // Rect rect2(l,w);
    // cout<<"area,perimeter:"<<rect2.getArea()<<","<<rect2.getPerimeter()<<endl;
    // return 0;

