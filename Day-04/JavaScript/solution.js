// Day 4: Printing Department
// Counts accessible paper rolls (@ with <4 adjacent @)
// Then iteratively removes accessible rolls
// Output: part1\npart2
// Dimensions: ~66x9 characters
// Node.js required
i=require('fs').readFileSync(0,'utf8');l=i.split('\n');R=l.length;C=
Math.max(...l.map(r=>r.length));g=l.map(r=>[...r.padEnd(C,'.')]);d=
[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]];p=t=0;g2=g.
map(r=>[...r]);for(r=0;r<R;r++)for(c=0;c<C;c++)if(g[r][c]=='@'){a=
0;for([x,y]of d)if((n=r+x)>=0&&n<R&&(m=c+y)>=0&&m<C&&g[n][m]=='@')
a++;if(a<4)p++}while(1){q=[];for(r=0;r<R;r++)for(c=0;c<C;c++)if(g2
[r][c]=='@'){a=0;for([x,y]of d)if((n=r+x)>=0&&n<R&&(m=c+y)>=0&&m<C
&&g2[n][m]=='@')a++;if(a<4)q.push([r,c])}if(!q.length)break;t+=q.
length;for([r,c]of q)g2[r][c]='.'}console.log(p+'\n'+t)