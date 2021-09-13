from typing import Any, Callable, Mapping, TypedDict


class ZIPCode(TypedDict):
  zip: str
  city: str
  county: str
  pop: int


JSONType = Any
APIMapping = Mapping[str, Callable[[], JSONType]]
