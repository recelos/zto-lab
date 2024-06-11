using System.Diagnostics;
using GeneratorCS;
using Metaheurystyki.Neighbourhood;

namespace Metaheurystyki;

public class TabuSearch
{
  private readonly Graph _graph;
  private readonly double _maxTime;
  private readonly INeighbourStrategy _neighbourStrategy;

  public TabuSearch(Graph graph, double timeInSeconds, INeighbourStrategy neighbourStrategy)
  {
    _graph = graph;
    _neighbourStrategy = neighbourStrategy;
    _maxTime = timeInSeconds * 1000; // zamiana [s] na [ms]
  }

  public (int, List<int>) Solve(int start)
  {
    var currentPath = Enumerable.Range(0, _graph.Size)
      .Except(new[] { start })
      .ToList();
    currentPath.Shuffle(new RandomNumberGenerator(Constants.Seed));

    var iteration = 0;
    
    var currentWeight = GetCurrentWeight(currentPath, start);
    var outputWeight = currentWeight;
    Console.WriteLine($"{iteration++, -6}{outputWeight}");
    var outputPath = new List<int>();
    var diversificationCounter = 0;
    var tabuList = new Queue<(int, int)>();
    
    var timer = new Stopwatch();
    timer.Start();
    while (timer.ElapsedMilliseconds <= _maxTime)
    {
      var move = (0, 0);
      
      var previousWeight = currentWeight;
      // szukamy najlepszego ruchu w sasiedztwie
      FindBestMove(start, currentPath, ref currentWeight, tabuList, ref move); 
      // bierzemy najlepszego sasiada
      GetNeighbour(currentPath, move.Item1, move.Item2);
      // dodajemy ruch do listy ograniczen
      tabuList.Enqueue(move);
      // jesli lista sasiadow jest wieksza od rozmiaru grafu, usun pierwszy element z listy
      if (tabuList.Count > _graph.Size)
      {
        tabuList.Dequeue();
      }
      
      // jesli znaleziono najlepsze dotychczasowe rozwiazanie, zapisz je
      if (currentWeight < outputWeight)
      {
        outputPath = new List<int>(currentPath);
        outputWeight = currentWeight;
        Console.WriteLine($"{iteration, -6}{outputWeight}");
      }
      // jezeli znaleziono minimum lokalne, nalezy zaczac szukac gdzie indziej
      else if (previousWeight > currentWeight)
      {
        diversificationCounter++;
        if (diversificationCounter > _graph.Size * 10)
        {
          currentWeight = int.MaxValue;
          diversificationCounter = 0;
          currentPath.Shuffle(new RandomNumberGenerator(Constants.Seed));
          tabuList.Clear();
        }
      }

      iteration++;
    }
    timer.Stop();

    outputPath.Insert(0, start);
    outputPath.Add(0);
    return (outputWeight, outputPath);
  }

  private void FindBestMove(int start, List<int> currentPath, 
    ref int currentWeight, Queue<(int, int)> tabuList, ref (int, int) move)
  {
    for (var i = 0; i < _graph.Size - 1; i++)
    {
      for (var j = i + 1; j < _graph.Size - 1; j++)
      {
        var neighbourPath = new List<int>(currentPath);
        GetNeighbour(neighbourPath, i, j);
        var neighbourWeight = GetCurrentWeight(neighbourPath, start); //GetCurrentWeightAfterSwap(currentPath, neighbourPath, (i,j), currentWeight); //GetCurrentWeight(neighbourPath, start);

        if (neighbourWeight < currentWeight && !tabuList.Contains((i, j)))
        {
          currentWeight = neighbourWeight;
          move = (i, j);
        }
      }
    }
  }

  private void GetNeighbour(IList<int> input, int i, int j)
    => _neighbourStrategy.GetNeighbour(input, i, j);

  private int GetCurrentWeight(List<int> path, int start)
  {
    var weight = 0;
    var currentVertex = start;

    foreach (var vertex in path)
    {
      weight += _graph.AdjacencyMatrix[currentVertex][vertex];
      currentVertex = vertex;
    }

    weight += _graph.AdjacencyMatrix[currentVertex][start];
    return weight;
  }
}