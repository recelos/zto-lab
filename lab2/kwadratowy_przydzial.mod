int n = ...; 
 
range Obiekty = 1..n;
range Lokalizacje = 1..n;
 
 
int d[Obiekty][Lokalizacje] = ...;
int w[Lokalizacje][Lokalizacje] = ...;
 
dvar boolean x[Obiekty][Lokalizacje];
 
minimize sum (i in Obiekty, j in Obiekty, k in Lokalizacje, l in Lokalizacje) 
    w[i][j] * d[k][l] * x[i][k] * x[j][l];
 
subject to {
  forall (i in Obiekty){
    sum (j in Lokalizacje) x[i][j] == 1;
  }
  forall (i in Lokalizacje){
    sum (j in Obiekty) x[j][i] == 1;
  }
};