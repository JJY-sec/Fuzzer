#include<stdio.h>
#include<string.h>
void main(){
    char buf[0x10];
    scanf("%s",buf);
    if (buf[0]=='a'){
        if(buf[1]=='b'){
            if(buf[2]=='c'){
                if(strlen(buf)>0x10-1){
                    printf("test\n");
                }
            }
        }
    }

}
