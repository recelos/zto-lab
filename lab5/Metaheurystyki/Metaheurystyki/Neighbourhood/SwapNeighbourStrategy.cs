namespace Metaheurystyki.Neighbourhood;

public class SwapNeighbourStrategy : INeighbourStrategy
{
  public void GetNeighbour(IList<int> input, int i, int j)
    => input.Swap(i, j);
}