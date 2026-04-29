#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdint.h>
#include<ctype.h>
                                 int main
                                (int a,
                                char**
                               b){FILE*
                              f;long s;
                             char*i,*p,*
                             q;uint64_t t
                            =0,x,y;int n=
                            0,c,k;if(a-2)
                           return!fprintf(
                          stderr,"Use: %s "
                          "<file>\n",*b);f=
                          fopen(b[1],"r");if
                         (!f)return!fprintf(
                        stderr,"No file: %s\n"
                        ,b[1]);fseek(f,0,2);s=
                       ftell(f);fseek(f,0,0);i
                       =malloc(s+1);fread(i,1,s
                       ,f);i[s]=0;fclose(f);for
                      (p=q=i;*p;(*p-32&&*p-9&&*
                     p-10&&*p-13)?(*q++=*p):0,++
                     p);*q=0;for(p=i;*p;n++){char
                     *d=strchr(p,'-');p=strchr(d,
                      ',');p=p?p+1:d+strlen(d);}
                    uint64_t*m=malloc(2*n*8);for(p
                   =i;*p;){char*d=strchr(p,'-');*m
                  ++=strtoull(p,0,10);*m++=strtoull
                  (d+1,0,10);p=strchr(d,',');p=p?p+
                  1:d+strlen(d);}m-=2*n;for(k=1;k<7;
                 k++){uint64_t e=1,g=k==1?1:1;int j;
                 for(j=0;j<k-1;j++)g*=10;for(j=0;j<k;
                j++)e*=10;for(x=g;x<e;x++){char v[32]
               ,w[64];snprintf(v,32,"%llu",x);snprintf
               (w,64,"%s%s",v,v);y=strtoull(w,0,10);for
               (c=0;c<n;c++)if(y>=m[2*c]&&y<=m[2*c+1]){
              t+=y;break;}}}printf("%llu\n",t);free(m);
                          free(i);return 0;}
