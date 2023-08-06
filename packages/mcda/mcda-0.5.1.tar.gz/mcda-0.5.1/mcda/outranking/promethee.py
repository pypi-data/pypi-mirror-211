"""This module implements Promethee algorithms in a heavily modular way.

.. todo:: Implement commented-out classes
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from math import exp
from typing import Any, Dict, List, cast

import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from sklearn.decomposition import PCA

from ..core.interfaces import Ranker
from ..core.matrices import AdjacencyMatrix
from ..core.performance_table import PerformanceTable
from ..core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    PreferenceRelation,
    PreferenceStructure,
    Relation,
)
from ..core.scales import PreferenceDirection, QuantitativeScale, Scale
from ..core.values import Ranking, ScaleValues


class PreferenceFunction(ABC):
    """This class define an interface for preference functions to share."""

    @abstractmethod
    def _apply_on_positive(self, x: float) -> float:  # pragma: nocover
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        pass

    def __call__(self, x: float) -> float:
        """Return preference degree on a criterion of two alternatives.

        :param x: criteria values difference
        :return:
        """
        if x <= 0:
            return 0
        return self._apply_on_positive(x)


class UShapeFunction(PreferenceFunction):
    """This class implements the u-shape preference function.

    :param q: the indifference threshold
    """

    def __init__(self, q: float):
        self.q = q

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.q else 0


class UsualFunction(UShapeFunction):
    """This class implements the usual preference function.

    This is actually a :class:`UShapeFunction` with 0 as the threshold.
    """

    def __init__(self):
        super().__init__(0)


class VShapeFunction(PreferenceFunction):
    """This class implements the v-shape preference function.

    :param p: preference threshold
    """

    def __init__(self, p: float):
        self.p = p

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.p else abs(x) / self.p


class LevelFunction(PreferenceFunction):
    """This class implements the level preference function.

    :param p: preference threshold
    :param q: indifference threshold
    """

    def __init__(self, p: float, q: float):
        if q > p:
            raise ValueError(f"incorrect threshold : q={q} greater than p={p}")
        self.p = p
        self.q = q

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.p else 0.5 if x > self.q else 0


class LinearFunction(LevelFunction):
    """This class implements the linear level preference function.

    :param p: preference threshold
    :param q: indifference threshold
    """

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return (
            1
            if x > self.p
            else (abs(x) - self.q) / (self.p - self.q)
            if x > self.q
            else 0
        )


class GaussianFunction(PreferenceFunction):
    """This class implements the gaussian preference function.

    :param s: standard deviation
    """

    def __init__(self, s: float):
        self.s = s

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of two alternatives.

        :param x: criteria values difference
        :return:
        """
        return 1 - exp(-(x**2) / (2 * self.s**2))


class GeneralizedCriteria:
    """This class implements generalized criteria.

    This consists for each criterion of a preference function and a preference
    direction.

    Implementations naming conventions are taken from
    :cite:p:`figueira2005mcda`.

    :param preference_functions: one preference function per criterion
    :param preference_directions:
        one preference direction per criterion (set to `MAX` if not provided)

    .. todo:: Could be based on a GeneralizedCriterion class
    """

    def __init__(
        self,
        preference_functions: Dict[Any, PreferenceFunction],
        preference_directions: Dict[Any, PreferenceDirection] = None,
        **kwargs,
    ):
        self.preference_functions = preference_functions
        self.preference_directions = (
            {c: PreferenceDirection.MAX for c in preference_functions}
            if preference_directions is None
            else preference_directions
        )
        super().__init__(**kwargs)

    def _pairwise_partial_preference(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> Series:
        """Return the criteria preference degrees of two alternatives.

        :param alternative_values1: criteria values for one alternative
        :param alternative_values2: criteria values for the second alternative
        :return:
        """
        scales: Dict[Any, Scale] = {
            c: QuantitativeScale(
                cast(QuantitativeScale, s).dmin,
                cast(QuantitativeScale, s).dmax,
                self.preference_directions[c],
            )
            for c, s in alternative_values1.scales.items()
        }
        diffs = (
            alternative_values1.transform(scales).data
            - alternative_values2.transform(scales).data
        )
        return Series(
            {c: self.preference_functions[c](v) for c, v in diffs.items()}
        )

    def partial_preferences(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:
        """Compute partial preferences for each alternatives' pair.

        :param performance_table:
        :return: matrix of partial preferences
        """
        return AdjacencyMatrix(
            [
                [
                    self._pairwise_partial_preference(
                        performance_table.alternatives_values[ai],
                        performance_table.alternatives_values[aj],
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            vertices=performance_table.alternatives,
        )


class GeneralizedCriteriaAggregator(ABC):
    """This abstract class defines the methods implemented by aggregators of
    generalized criteria.
    """

    @abstractmethod
    def _pairwise_preference(
        self, partial_preferences: Series
    ) -> float:  # pragma: nocover
        """Compute pairwise multicriteria preference index.

        Aggregate partial preferences series into one value.

        :param partial_preferences:
            partial preferences between two alternatives
        :return: preference index
        """
        pass

    def preferences(
        self, partial_preferences: AdjacencyMatrix
    ) -> AdjacencyMatrix:
        """Compute pairwise multicriteria preference indices by
        aggregation of partial preferences.

        :param partial_preferences:
        :return: matrix of multicriteria preferences
        """
        data = partial_preferences.data.applymap(self._pairwise_preference)
        return partial_preferences.__class__(data)


class GeneralizedCriteriaWeightedSum(GeneralizedCriteriaAggregator):
    """This class defines the simplest aggregator of generalized criteria:
    a weighted sum.

    :param criteria_weights:
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        **kwargs,
    ):
        self.criteria_weights = Series(criteria_weights)
        super().__init__(**kwargs)

    def _pairwise_preference(
        self,
        partial_preferences: Series,
    ) -> float:
        """Compute pairwise multicriteria preference index.

        Aggregate partial preferences using a weighted sum.

        :param partial_preferences:
            partial preferences between two alternatives
        :return: preference index
        """
        return (
            self.criteria_weights * partial_preferences
        ).sum() / self.criteria_weights.sum()


"""
class ReinforcedPreference(GeneralizedCriteriaWeightedSum):
    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        reinforced_factors: Dict[Any, float],
        **kwargs,
    ):
        super().__init__(criteria_weights, **kwargs)
        self.preference_thresholds = preference_thresholds
        self.indifference_thresholds = indifference_thresholds
        self.reinforced_factors = reinforced_factors

    def _pairwise_preference(
        self,
        partial_preferences: Series,
    ) -> float:
        # weights = Series(self.criteria_weights)
        pass


class CriteriaPreferenceInteraction(ABC):
    @abstractmethod
    def __call__(
        self, preference1: float, preference2: float
    ) -> float:  # pragma: nocover
        pass


class MutualStrengtheningInteraction(CriteriaPreferenceInteraction):
    pass


class MutualWeakeningInteraction(CriteriaPreferenceInteraction):
    pass


class MutualAntagonisticInteraction(CriteriaPreferenceInteraction):
    pass


class GeneralizedCriteriaInteractions(GeneralizedCriteriaAggregator):
    def __init__(self, interaction_matrix: DataFrame):
        self.interaction_matrix = interaction_matrix


class Discordance(GeneralizedCriteriaAggregator):
    def _pairwise_preference(self, partial_preferences: Series) -> float:
        return 1 - self.pairwise_discordance(partial_preferences)

    def pairwise_discordance(self, partial_preferences: Series) -> float:
        pass

    def discordance_from_partial(
        self, partial_preferences: AdjacencyMatrix
    ) -> AdjacencyMatrix:
        data = partial_preferences.data.applymap(self.pairwise_discordance)
        return partial_preferences.__class__(data)


class Veto(GeneralizedCriteriaAggregator):
    def __init__(
        self,
        veto_thresholds: Dict[Any, float],
        **kwargs,
    ):
        self.veto_thresholds = veto_thresholds
        super().__init__(**kwargs)

    def _pairwise_preference(self, partial_preferences: Series) -> float:
        return 1 - self.pairwise_veto(partial_preferences)

    def pairwise_veto(self, partial_preferences: Series) -> float:
        pass

    def veto_from_partial(
        self, partial_preferences: AdjacencyMatrix
    ) -> AdjacencyMatrix:
        data = partial_preferences.data.applymap(self.pairwise_veto)
        return partial_preferences.__class__(data)


class StrongVeto(Veto):
    def pairwise_veto(self, partial_preferences: Series) -> float:
        pass


class ChainCriteriaAggregator(GeneralizedCriteriaAggregator):
    def __init__(
        self,
        *aggregators: GeneralizedCriteriaAggregator,
        **kwargs,
    ):
        self.aggregators = [*aggregators]
        super().__init__(**kwargs)

    def _pairwise_preference(self, partial_preferences: Series) -> float:
        res = 1.0
        for agg in self.aggregators:
            res *= agg._pairwise_preference(partial_preferences)
        return res

    def preferences(
        self, partial_preferences: AdjacencyMatrix
    ) -> AdjacencyMatrix:
        res = partial_preferences.__class__(
            1,
            vertices=partial_preferences.vertices,
        )
        for agg in self.aggregators:
            res *= agg.preferences(partial_preferences)
        return res
"""


class Flows(ABC):
    """This abstract class defines the interface of flows computers."""

    @abstractmethod
    def flows(
        self, preferences: AdjacencyMatrix, **kwargs
    ) -> Series:  # pragma: nocover
        """Compute flows.

        :param preferences:
        :return: computed flows
        """
        pass


def positive_flows(
    preferences: AdjacencyMatrix, profiles: List = None
) -> Series:
    """Compute positive flows.

    :param preferences:
    :param profiles:
    :return: computed positive flows

    .. note::
        if `profiles` is not ``None``, it will returns alternatives
        vs profiles positive flows
    """
    if profiles is None:
        data = preferences.data
    else:
        alternatives = sorted(
            set(preferences.vertices) - set(profiles),
            key=lambda a: preferences.vertices.index(a),
        )
        data = preferences.data.loc[alternatives, profiles]
    return data.sum(axis=1)


def negative_flows(
    preferences: AdjacencyMatrix, profiles: List = None
) -> Series:
    """Compute negative flows.

    :param preferences:
    :param profiles:
    :return: computed negative flows

    .. note::
        if `profiles` is not ``None``, it will returns profiles
        vs alternatives negative flows
    """
    if profiles is None:
        data = preferences.data
    else:
        alternatives = sorted(
            set(preferences.vertices) - set(profiles),
            key=lambda a: preferences.vertices.index(a),
        )
        data = preferences.data.loc[profiles, alternatives]
    return data.sum(axis=0)


class OutrankingFlows(Flows):
    """This class defines a basic outranking flows computer able to return
    either positive or negative flows.
    """

    def flows(
        self,
        preferences: AdjacencyMatrix,
        negative: bool = False,
        **kwargs,
    ) -> Series:
        """Compute outranking flows.

        :param preferences:
        :param negative:
            if ``True``, returns the negative flows, positive ones otherwise
        :return: outranking flows
        """
        return (
            negative_flows(preferences)
            if negative
            else positive_flows(preferences)
        )


class NetOutrankingFlows(Flows):
    """This class defines a net outranking flows computer."""

    def flows(self, preferences: AdjacencyMatrix, **kwargs) -> Series:
        """Compute net outranking flows.

        :param preferences:
        :return: net outranking flows
        """
        return positive_flows(preferences) - negative_flows(preferences)


"""
class NetFlowAggregatorType(Enum):
    MAX = np.nanmax
    MIN = np.nanmin
    SUM = np.nansum

    def __call__(self, preferences: AdjacencyMatrix) -> Series:
        values = preferences.data.values
        np.fill_diagonal(values, np.NaN)
        return Series(self.value(values), index=preferences.vertices)


class NetFlowScore(Flows, ABC):
    def __init__(
        self,
        aggregation_type: NetFlowAggregatorType,
        **kwargs,
    ):
        self.aggregation_type = aggregation_type

    @abstractmethod
    def _aggregate(
        self, preferences: AdjacencyMatrix
    ) -> Series:  # pragma: nocover
        pass

    def flows(
        self, preferences: AdjacencyMatrix, total_order: bool = False, **kwargs
    ) -> Series:
        res = self._aggregate(preferences)
        if not total_order:
            return res
        duplicates = res.duplicated(keep=False)
        if len(duplicates) > 0:
            res[duplicates] = self.flows(
                preferences.loc[duplicates, duplicates]
            )
        return res


class NetFlowScoreFavor(NetFlowScore):
    def _aggregate(self, preferences: AdjacencyMatrix) -> Series:
        return self.aggregation_type(preferences)


class NetFlowScoreAgainst(NetFlowScore):
    def _aggregate(self, preferences: AdjacencyMatrix) -> Series:
        return -self.aggregation_type(preferences)


class NetFlowScoreDifference(NetFlowScore):
    def _aggregate(self, preferences: AdjacencyMatrix) -> Series:
        return self.aggregation_type(preferences - preferences.data.T)
"""


def criteria_flows(partial_preferences: AdjacencyMatrix) -> DataFrame:
    """Returns the criteria flows.

    :param partial_preferences:
    :return:
    """
    res = DataFrame(
        0,
        index=partial_preferences.vertices,
        columns=cast(
            Series, partial_preferences.data.iloc[0, 0]
        ).index.tolist(),
    )
    criteria_preferences = {
        c: partial_preferences.data.applymap(lambda s, crit=c: s[crit])
        for c in res.columns
    }
    for a in res.index:
        for c, crit_prefs in criteria_preferences.items():
            res.loc[a, c] = (crit_prefs.loc[a] - crit_prefs[a]).mean()
    return res


"""
class SingleCriterionNetFlow:
    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        **kwargs,
    ):
        self.criteria_weights = Series(criteria_weights)

    def _apply(self, partial_preference: Series) -> float:
        return (
            self.criteria_weights * partial_preference
        ).sum() / self.criteria_weights.sum()

    def flows(self, partial_preferences: AdjacencyMatrix) -> Series:
        return cast(
            Series,
            criteria_flows(partial_preferences).apply(
                self._apply,
                axis=1,
            ),
        )
"""


class Promethee1(
    GeneralizedCriteria,
    GeneralizedCriteriaWeightedSum,
    OutrankingFlows,
    Ranker,
):
    """This class implements Promethee I.

    Implementation and notations are based on :cite:p:`vincke1998promethee1`.

    :param criteria_weights:
    :param preference_functions: one function per criterion
    :param preference_directions:
        one direction per criterion (MAX if not provided)
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_functions: Dict[Any, PreferenceFunction],
        preference_directions: Dict[Any, PreferenceDirection] = None,
        **kwargs,
    ):
        super().__init__(
            preference_functions=preference_functions,
            preference_directions=preference_directions,
            criteria_weights=criteria_weights,
            **kwargs,
        )

    @staticmethod
    def _flow_intersection(
        a: Any,
        b: Any,
        pos_flow_a: float,
        pos_flow_b: float,
        neg_flow_a: float,
        neg_flow_b: float,
    ) -> Relation:
        """Compute the positive and negative flow intersection.

        :param a: first alternative
        :param b: second alternative
        :param pos_flow_a: the positive flow of first alternative
        :param pos_flow_b: the positive flow of second alternative
        :param neg_flow_a: the negative flow of first alternative
        :param neg_flow_b: the negative flow of second alternative
        :return: the comparison of the two alternatives in a relation
        """

        if pos_flow_a == pos_flow_b and neg_flow_a == neg_flow_b:
            return IndifferenceRelation(a, b)
        if pos_flow_a >= pos_flow_b and neg_flow_a <= neg_flow_b:
            return PreferenceRelation(a, b)
        if pos_flow_b >= pos_flow_a and neg_flow_b <= neg_flow_a:
            return PreferenceRelation(b, a)
        return IncomparableRelation(a, b)

    def rank(
        self, performance_table: PerformanceTable, **kwargs
    ) -> PreferenceStructure:
        """Apply Promethee I algorithm.

        :param performance_table:
        :return: result as a preference structure
        """
        partial_preferences = self.partial_preferences(performance_table)
        preferences = self.preferences(partial_preferences)
        pos_flow = self.flows(preferences)
        neg_flow = self.flows(preferences, negative=True)

        res = PreferenceStructure()
        for i, a in enumerate(performance_table.alternatives):
            for b in performance_table.alternatives[(i + 1) :]:
                res += self._flow_intersection(
                    a, b, pos_flow[a], pos_flow[b], neg_flow[a], neg_flow[b]
                )
        return res


class Promethee2(
    GeneralizedCriteria,
    GeneralizedCriteriaWeightedSum,
    NetOutrankingFlows,
    Ranker,
):
    """This class implements Promethee II.

    Implementation and notations are based on :cite:p:`vincke1998promethee1`.

    :param criteria_weights:
    :param preference_functions: one function per criterion
    :preference_directions:
        one direction per criterion (MAX if not provided)
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_functions: Dict[Any, PreferenceFunction],
        preference_directions: Dict[Any, PreferenceDirection] = None,
        **kwargs,
    ):
        super().__init__(
            preference_functions=preference_functions,
            preference_directions=preference_directions,
            criteria_weights=criteria_weights,
            **kwargs,
        )

    def rank(self, performance_table: PerformanceTable, **kwargs) -> Ranking:
        """Apply Promethee II algorithm.

        :param performance_table:
        :return: result as scores
        """
        partial_preferences = self.partial_preferences(performance_table)
        preferences = self.preferences(partial_preferences)
        return Ranking(self.flows(preferences))


class PrometheeGaia(Promethee2):
    """This class is used to represent and draw a Promethee GAIA plane.

    Implementations naming conventions are taken from
    :cite:p:`figueira2005mcda`

    :param criteria_weights:
    :param preference_functions: one function per criterion
    """

    def unicriterion_net_flows_matrix(
        self, performance_table: PerformanceTable
    ) -> DataFrame:
        """Computes the whole matrix of single criterion net flows.

        Each cell corresponds to the single criterion net flow of an
        alternative considering only one criterion.

        :param performance_table:
        :return: unicriterion net flows matrix
        """
        return criteria_flows(self.partial_preferences(performance_table))

    def plot(self, performance_table: PerformanceTable):  # pragma: nocover
        """Plots the GAIA plane and displays in the top-left corner
        the ratio of saved information by the PCA, delta.

        :param performance_table:
        """
        net_flows = self.unicriterion_net_flows_matrix(performance_table)

        pca = PCA(n_components=2)
        pca.fit(net_flows)
        delta = (
            pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
        )
        alternative_vectors = pca.transform(net_flows)
        criterions = DataFrame(
            [
                [
                    1 if i == j else 0
                    for j in range(len(performance_table.criteria))
                ]
                for i in range(len(performance_table.criteria))
            ],
            index=performance_table.criteria,
            columns=performance_table.criteria,
        )
        criterion_vectors = pca.transform(criterions)
        S = self.criteria_weights.sum()
        pi: List[float] = [0, 0]
        for criterion, w in self.criteria_weights.items():
            pi[0] += criterion_vectors[criterion][0] * w
            pi[1] += criterion_vectors[criterion][1] * w
        pi[0] = pi[0] / S
        pi[1] = pi[1] / S

        plt.figure(figsize=[10, 10])

        for i, alternative in enumerate(performance_table.alternatives):
            plt.scatter(
                alternative_vectors[i][0],
                alternative_vectors[i][1],
                s=100,
                label=alternative,
            )
        for j, criterion in enumerate(performance_table.criteria):
            plt.text(
                criterion_vectors[j][0],
                criterion_vectors[j][1],
                criterion,
                ha="center",
            )
            plt.arrow(
                0,
                0,
                criterion_vectors[j][0],
                criterion_vectors[j][1],
            )

        plt.arrow(0, 0, pi[0], pi[1])
        plt.scatter(pi[0], pi[1], s=150, marker="*", label=r"$\pi$")

        ax = plt.gca()
        xmin, _ = ax.get_xlim()
        _, ymax = ax.get_ylim()

        plt.text(
            xmin, ymax, r"$\delta$ = %.3f" % delta, bbox=dict(boxstyle="round")
        )

        plt.legend()
        plt.plot()
        plt.show()
