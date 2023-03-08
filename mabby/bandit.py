from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

import numpy as np
from numpy.random import Generator


class Arm(ABC):
    @abstractmethod
    def __init__(self, **kwargs: float):
        pass

    @abstractmethod
    def play(self, rng: Generator) -> float:
        """Play arm and sample reward from distribution"""

    @property
    @abstractmethod
    def mean(self) -> float:
        """Compute mean of reward distribution"""

    @classmethod
    def bandit(cls, **kwargs: list[float]) -> Bandit:
        params_dicts = [dict(zip(kwargs, t)) for t in zip(*kwargs.values())]
        if len(params_dicts) == 0:
            raise ValueError("insufficient parameters to create an arm")
        return Bandit([cls(**params) for params in params_dicts])


class Bandit:
    def __init__(self, arms: list[Arm]):
        self._arms = arms

    def __len__(self) -> int:
        return len(self._arms)

    def __repr__(self) -> str:
        return repr(self._arms)

    def __getitem__(self, i: int) -> Arm:
        return self._arms[i]

    def __iter__(self) -> Iterable[Arm]:
        return iter(self._arms)

    def play(self, i: int, rng: Generator) -> float:
        return self[i].play(rng)

    def best_arm(self) -> int:
        return int(np.argmax([arm.mean for arm in self._arms]))

    def regret(self, choice: int) -> float:
        return self._arms[self.best_arm()].mean - self._arms[choice].mean


class BernoulliArm(Arm):
    def __init__(self, p: float):
        self.p = p

    def play(self, rng: Generator) -> int:
        return rng.binomial(1, self.p)

    @property
    def mean(self) -> float:
        return self.p

    def __repr__(self) -> str:
        return f"Bernoulli(p={self.p})"


class GaussianArm(Arm):
    def __init__(self, loc: float, scale: float):
        self.loc = loc
        self.scale = scale

    def play(self, rng: Generator) -> float:
        return rng.normal(self.loc, self.scale)

    @property
    def mean(self) -> float:
        return self.loc

    def __repr__(self) -> str:
        return f"Gaussian(loc={self.loc}, scale={self.scale})"