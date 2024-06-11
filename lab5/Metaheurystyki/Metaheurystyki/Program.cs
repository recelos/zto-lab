using System;
using GeneratorCS;
using Metaheurystyki;
using Metaheurystyki.Neighbourhood;

var graph = new Graph(GetRandomMatrix(100, 110));

var ts = new TabuSearch(graph, 10, new InsertNeighbourStrategy());

var (answer, path) = ts.Solve(0);

Console.WriteLine($"{path.CombineToString()}");

static int[][] GetRandomMatrix(int range, int size)
{
  var random = new RandomNumberGenerator(Constants.Seed);

  //inicjalizacja macierzy
  var adjMatrix = new int[size][];

  for (var i = 0; i < size; i++)
  {
    adjMatrix[i] = new int[size];
  }

  // wypelnij przekatne wartosciami -1
  for (var i = 0; i < size; i++)
  {
    adjMatrix[i][i] = -1;
  }
    
  for (var i = 0; i < size; i++)
  {
    for (var j = 0; j < size; j++)
    {
      if (i != j)
      {
        var value = random.nextInt(1, range);
        adjMatrix[i][j] = value;
      }
    }
  }
    
  return adjMatrix;
}