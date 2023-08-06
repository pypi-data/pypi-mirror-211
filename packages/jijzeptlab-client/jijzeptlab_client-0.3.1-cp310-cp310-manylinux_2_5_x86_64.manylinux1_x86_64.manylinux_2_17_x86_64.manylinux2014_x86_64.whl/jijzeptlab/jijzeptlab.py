from __future__ import annotations


class FixedVariables:
    def __init__(self) -> None:
        self._fixed_vars = {}

    def insert(self, key: str | tuple[str, list[int]], value: float):
        key_: tuple[str, list[int]]
        if isinstance(key, str):
            key_ = (key, [])
        else:
            key_ = key

        if key_[0] not in self._fixed_vars:
            self._fixed_vars[key_[0]] = {}
        self._fixed_vars[key_[0]][tuple(key_[1])] = value

    @classmethod
    def from_dict(
        cls, dict_data: dict[str, dict[tuple[int, ...], float | int]]
    ) -> "FixedVariables":
        fixed_vars = cls()
        fixed_vars._fixed_vars = dict_data
        return fixed_vars

    def to_dict(self) -> dict[str, dict[tuple[int, ...], float | int]]:
        return self._fixed_vars


class InstanceData:
    def __init__(self) -> None:
        self._instance_data = {}

    @classmethod
    def from_dict(cls, dict_data: dict) -> InstanceData:
        instance_data = cls()
        instance_data._instance_data = dict_data
        return instance_data

    def insert(self, name: str, value):
        self._instance_data[name] = value

    def to_dict(self) -> dict:
        return self._instance_data
