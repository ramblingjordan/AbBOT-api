from typing import Any, Callable, Mapping, TypedDict


class ZIPCode(TypedDict):
  city: str
  county: str
  pop: int
  ip_address_ranges: list[str]


JSONType = Any
APIMapping = Mapping[str, Callable[[], JSONType]]
