namespace Metaheurystyki.Neighbourhood;

public class InsertNeighbourStrategy : INeighbourStrategy
{
  public void GetNeighbour(IList<int> input, int i, int j)
  {
    var temp = input[i];
    input.RemoveAt(i);
    input.Insert(j, temp);
  }
}