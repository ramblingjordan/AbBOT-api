import random
from typing import Any, List, Tuple, Union, cast

WeightedLists = List[List[Union[float, Any]]]
WeightedTuples = List[Tuple[float, Any]]


def weighted_choice(items: Union[WeightedLists, WeightedTuples]) -> Any:
  weights: List[float] = []
  values: List[Any] = []
  for weight, value in items:
    weights.append(cast(float, weight))
    values.append(cast(Any, value))

  return random.choices(population=values, weights=weights, k=1)[0]
