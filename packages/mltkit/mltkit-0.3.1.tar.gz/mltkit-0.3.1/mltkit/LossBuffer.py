from statistics import mean
from collections import OrderedDict
from typing import Dict, List, Optional, OrderedDict as T_OrderedDict, Union

_T_Values = List[float]
_T_BufferDict = T_OrderedDict[str, _T_Values]
_T_BufferArg = Union[T_OrderedDict[str, float], Dict[str, float]]


class LossBuffer(object):
    __slots__ = ['_buffers', '_mean_cache']
    _buffers: Dict[str, _T_BufferDict]
    _mean_cache: Dict[str, Dict[str, float]]

    def __init__(self) -> None:
        self._buffers = {}
        self._mean_cache = {}

    def _insert_mean_cache(self, tag: str, key: str, value: float) -> None:
        tag_dict: Dict[str, float]
        try:
            tag_dict = self._mean_cache[tag]
        except KeyError:
            tag_dict = {}
            self._mean_cache[tag] = tag_dict
        tag_dict[key] = value

    def _del_mean_cache(self, tag: str, key: str) -> None:
        try:
            del self._mean_cache[tag][key]
        except KeyError:
            pass

    def get_buffer(self, tag: str) -> Optional[_T_BufferDict]:
        try:
            return self._buffers[tag]
        except KeyError:
            pass

    def get_values(self, tag: str, key: str) -> Optional[_T_Values]:
        buffer: Optional[_T_BufferDict] = self.get_buffer(tag)
        if buffer is not None:
            try:
                values: _T_Values = buffer[key]
                if values:
                    return values
            except KeyError:
                pass

    def update_values(self, tag: str, key: str, value: float) -> None:
        try:
            buffer = self._buffers[tag]
        except KeyError:
            buffer = OrderedDict()
            self._buffers[tag] = buffer
        try:
            buffer[key].append(value)
        except KeyError:
            buffer[key] = [value]
        self._del_mean_cache(tag, key)

    def update_buffer(self, tag: str, values: _T_BufferArg) -> None:
        for k, v in values.items():
            self.update_values(tag, k, v)

    def get_mean(self, tag: str, key: str) -> Optional[float]:
        try:
            return self._mean_cache[tag][key]
        except KeyError:
            values: Optional[List[float]] = self.get_values(tag, key)
            if values is None:
                return
            mean_val: float = mean(values)
            self._insert_mean_cache(tag, key, mean_val)
            return mean_val

    def get_means(self, tag: str) -> Optional[T_OrderedDict[str, float]]:
        try:
            out: T_OrderedDict[str, float] = OrderedDict()
            for key in self._buffers[tag].keys():
                out[key] = self.get_mean(tag, key)
            return out
        except KeyError:
            pass

    def reset_values(self, tag: str, key: str) -> None:
        try:
            self._buffers[tag][key] = []
        except KeyError:
            pass
        finally:
            self._del_mean_cache(tag, key)

    def reset_buffer(self, tag: str) -> None:
        try:
            for key in self._buffers[tag].keys():
                self.reset_values(tag, key)
        except KeyError:
            pass

    def reset_all(self) -> None:
        for tag in self._buffers.keys():
            self.reset_buffer(tag)
