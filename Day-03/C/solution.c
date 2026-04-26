#include<stdio.h>
long long O(char*O0){long long OO=0;for(int I1=0;O0[I1];I1++)for(int II=I1+1;O0[
II];II++){int l1=(O0[I1]-'0')*10+O0[II]-'0';if(l1>OO)OO=l1;}return OO;}
long long l(char*O0,int O1){int I1=0;while(O0[I1])I1++;if(I1<O1)return 0;char ll[
13];int II=0;for(int OO=0;OO<O1;OO++){int l1=I1-O1+OO;char I='0';int O=II;for(int
l=II;l<=l1;l++)if(O0[l]>I){I=O0[l];O=l;}ll[OO]=I;II=O+1;}ll[O1]=0;long long OO0=0
;for(int I=0;I<O1;I++)OO0=OO0*10+ll[I]-'0';return OO0;}
int main(void){char _[999];long long __=0,___=0;while(fgets(_,999,stdin)){int ____
=0;while(_[____]&&_[____]!='\n')____++;_[____]=0;if(!_[0])continue;__+=O(_);___+=l
(_,12);}printf("%lld\n%lld\n",__,___);}
