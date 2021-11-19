#include <math.h>
#include <iostream>
#include <vector>
using namespace std;
int bi_insect(int n,vector<int>& list,int data_size) {
        if(data_size==0){list[0]=n;}
        else if(data_size==1){
            if(n==list[0]){return -1;}
            else if(n>list[0]){list[1]=n;}
            else if(n<list[0]){list[1]=list[0];list[0]=n;}
        }
        else{
            int l = 0;
            int r = data_size-1;
            if(n==list[l] or n==list[r]){return -1;}
            else if(n>list[r]){list[data_size]=n;}
            else if(n<list[l]){
                for(int i=data_size;i>0;i--){list[i]=list[i-1];}
                list[0]=n;
            }
            else{
                while(r-l>1){
                    int mid = (l+r)/2;
                    if(list[mid]==n){return -1;}
                    else if(list[mid]>n){r=mid;}
                    else if(list[mid]<n){l=mid;}
                }
                for(int i=data_size;i>r;i--){list[i]=list[i-1];}
                list[r]=n;
            }

        }
        return 1;
    }
int main(){
    vector<string> ret(3,"");
    for(int i=0;i<3;i++){
        ret[i]=to_string(i+1);
    } 
    for(int i)
    return 0;
}
