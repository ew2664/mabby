from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

import numpy as np


class Arm(ABC):
    @abstractmethod
    def __init__(self, **kwargs: float):
        pass

    @abstractmethod
    def play(self) -> float:
        pass

    @property
    @abstractmethod
    def mean(self) -> float:
        pass

    @classmethod
    def armset(cls, **kwargs: List[float]) -> ArmSet:
        params_dicts = [dict(zip(kwargs, t)) for t in zip(*kwargs.values())]
        return ArmSet([cls(**params) for params in params_dicts])


class ArmSet:
    def __init__(self, arms: List[Arm]):
        self._arms = arms

    def __len__(self) -> int:
        return len(self._arms)

    def __repr__(self) -> str:
        return repr(self._arms)

    def __getitem__(self, i: int) -> Arm:
        return self._arms[i]

    def __iter__(self) -> Iterable[Arm]:
        return iter(self._arms)

    def play(self, i: int) -> float:
        return self[i].play()

    def best_arm(self) -> int:
        return int(np.argmax([arm.mean for arm in self._arms]))


class BernoulliArm(Arm):
    def __init__(self, p: float):
        self.p = p

    def play(self) -> int:
        return np.random.binomial(1, self.p)

    @property
    def mean(self) -> float:
        return self.p

    def __repr__(self) -> str:
        return f"Bernoulli(p={self.p})"


class GaussianArm(Arm):
    def __init__(self, loc: float, scale: float):
        self.loc = loc
        self.scale = scale

    def play(self) -> float:
        return np.random.normal(self.loc, self.scale)

    @property
    def mean(self) -> float:
        return self.loc

    def __repr__(self) -> str:
        return f"Gaussian(loc={self.loc}, scale={self.scale})"
