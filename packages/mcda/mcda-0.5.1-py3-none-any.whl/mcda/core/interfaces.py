"""This module is used to gather core interfaces and encourage their use for
a more coherent API.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, Sequence, TypeVar

from .performance_table import PerformanceTable
from .relations import IPreferenceStructure

T = TypeVar("T")


class Learner(Generic[T], ABC):
    """This interface describes a generic learner."""

    @abstractmethod
    def learn(self) -> T:  # pragma: nocover
        """Learn and return an object.

        :return:
        """
        pass


class Ranker(ABC):
    """Interface to implement ranking MCDA algorithms."""

    @abstractmethod
    def rank(
        self, performance_table: PerformanceTable, **kwargs
    ) -> IPreferenceStructure:  # pragma: nocover
        """Rank alternatives.

        :param performance_table:
        :return: ranking
        """
        pass


class Assignator(ABC):
    """Interface to implement assignment MCDA algorithms."""

    @abstractmethod
    def assign(
        self, performance_table: PerformanceTable, **kwargs
    ) -> Dict:  # pragma: nocover
        """Assign alternatives to categories.

        :param performance_table:
        :return: categories
        """
        pass


class Selector(ABC):
    """Interface to implement selection MCDA algorithms."""

    @abstractmethod
    def select(
        self, performance_table: PerformanceTable, **kwargs
    ) -> Sequence:  # pragma: nocover
        """Select a subset of alternatives.

        :param performance_table:
        :return: selected alternatives
        """
        pass


class Clusterizor(ABC):
    """Interface to implement clustering MCDA algorithms."""

    @abstractmethod
    def clusterize(
        self, performance_table: PerformanceTable, **kwargs
    ) -> Dict:  # pragma: nocover
        """Clusterize alternatives.

        :param performance_table:
        :return: alternatives clusters
        """
        pass
