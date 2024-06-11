using System.Text;

namespace Metaheurystyki;

public class Graph
{
  public int[][] AdjacencyMatrix { get; }

  public int Size => AdjacencyMatrix.Length;
  
  public Graph(int[][] adjMatrix)
  {
    AdjacencyMatrix = adjMatrix;
  }

  public override string ToString()
  {
    var output = new StringBuilder();
    foreach (var line in AdjacencyMatrix)
    {
      foreach (var value in line)
      {
        output.Append($"{value, -5}");
      }
      output.AppendLine();
    }

    return output.ToString();
  }
}