namespace Metaheurystyki.Neighbourhood;

public interface INeighbourStrategy
{
  void GetNeighbour(IList<int> input, int i, int j);
}