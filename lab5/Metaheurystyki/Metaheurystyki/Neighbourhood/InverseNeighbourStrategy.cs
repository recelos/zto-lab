namespace Metaheurystyki.Neighbourhood;

public class InverseNeighbourStrategy : INeighbourStrategy
{
  public void GetNeighbour(IList<int> input, int i, int j)
  {
    input.ReverseSubList(i,j);
  }
}