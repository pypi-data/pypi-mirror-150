import random
from typing import Iterator, Tuple

from .base import BaseAlgorithm
from ..space import SeparateSpace, ContinuousSpace, FixedSpace, BaseSpace
from ..utils import ValueProxyLock, RunFailed
from ..value import HyperValue


def random_space_value(space: BaseSpace):
    if isinstance(space, SeparateSpace):
        return random.randint(0, space.count - 1) * space.step + space.start
    elif isinstance(space, ContinuousSpace):
        return random.random() * (space.ubound - space.lbound) + space.lbound
    elif isinstance(space, FixedSpace):
        return random.randint(0, space.count - 1)
    else:
        raise TypeError(f'Unknown space type - {repr(space)}.')  # pragma: no cover


class RandomSearchAlgorithm(BaseAlgorithm):
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs):
        BaseAlgorithm.__init__(self, **kwargs)

    @classmethod
    def _random_hyper_value(cls, hv: HyperValue):
        return hv.trans(random_space_value(hv.space))

    def _iter_spaces(self, vsp: Tuple[HyperValue, ...], pres: ValueProxyLock) -> Iterator[Tuple[object, ...]]:
        while True:
            yield tuple(map(self._random_hyper_value, vsp))
            try:
                _ = pres.get()
            except RunFailed:
                pass
