from typing import Any, Callable, Mapping, TypedDict


class ZIPCode(TypedDict):
  zip: str
  county: str
  pop: int


class City(TypedDict):
  ip_address: list[str]
  zip_codes: list[ZIPCode]


JSONType = Any
APIMapping = Mapping[str, Callable[[], JSONType]]
