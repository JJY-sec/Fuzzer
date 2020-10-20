#include<stdio.h>
#include<stdlib.h>
void main(){
    char buf[0x20];
    read(0,buf,0x20);
    if (buf[0]=='a'&&buf[1]=='f'){
        if(buf[2]=='b'&&buf[3]=='g'){
            if(buf[4]=='c'&&buf[5]=='h'){
                abort();
            }
        }
    }

}
