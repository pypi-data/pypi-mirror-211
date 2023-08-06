"""This module implements the Electre algorithms.

Implementation and naming conventions are taken from
:cite:p:`vincke1998electre`.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Set, Tuple, TypeVar, cast

from pandas import DataFrame, Series

from ..core.categories import BoundedCategoryProfile
from ..core.interfaces import Assignator, Ranker, Selector
from ..core.matrices import AdjacencyMatrix
from ..core.performance_table import PerformanceTable
from ..core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    OutrankingMatrix,
    PreferenceRelation,
    Relation,
)
from ..core.scales import PreferenceDirection, QuantitativeScale
from ..core.values import ScaleValues

T = TypeVar("T")


class IElectre(Generic[T], ABC):
    """This class represents the common interface between all Electre
    algorithms
    """

    @abstractmethod
    def concordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:  # pragma: nocover
        """Compute the concordance matrix.

        :param performance_table:
        :return: concordance matrix
        """
        pass

    @abstractmethod
    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:  # pragma: nocover
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix
        """
        pass

    @abstractmethod
    def construct(
        self, performance_table: PerformanceTable
    ) -> T:  # pragma: nocover
        """Construct the outranking structure.

        :param performance_table:
        :return: outranking structure
        """
        pass

    @abstractmethod
    def exploit(
        self, outranking_structure: T, **kwargs
    ) -> Any:  # pragma: nocover
        pass


class _BaseElectre1(ABC):
    """This class implements common methods for Electre I and II.

    :param criteria_weights:
    """

    def __init__(self, criteria_weights: Dict[Any, float]):
        self.criteria_weights = criteria_weights

    def _pairwise_concordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Compute the concordance comparison of 2 alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :return: concordance index

        .. warning::
            this method assumes that alternatives values have the same scales
        """
        scales = cast(Dict[str, QuantitativeScale], alternative_values1.scales)
        concordance_value = 0.0
        for k in alternative_values1.labels:
            concordance_value = (
                concordance_value + self.criteria_weights[k]
                if (
                    alternative_values1[k] >= alternative_values2[k]
                    and scales[k].preference_direction
                    == PreferenceDirection.MAX
                )
                or (
                    alternative_values1[k] <= alternative_values2[k]
                    and scales[k].preference_direction
                    == PreferenceDirection.MIN
                )
                else concordance_value
            )
        concordance_value = concordance_value / sum(
            self.criteria_weights.values()
        )
        assert concordance_value >= 0
        return concordance_value

    def concordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:
        """Compute the concordance matrix.

        :param performance_table:
        :return: concordance matrix
        """
        return AdjacencyMatrix(
            [
                [
                    self._pairwise_concordance(
                        performance_table.alternatives_values[ai],
                        performance_table.alternatives_values[aj],
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            vertices=performance_table.alternatives,
        )

    def _pairwise_disconcordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Compute the discordance comparison of 2 alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :return: discordance index

        .. warning::
            this method assumes that alternatives values have the same scales
        """
        pref_factor = Series(
            {
                c: (
                    1
                    if scale.preference_direction == PreferenceDirection.MAX
                    else -1
                )
                for c, scale in cast(
                    Dict[Any, QuantitativeScale], alternative_values1.scales
                ).items()
            }
        )
        return max(
            (alternative_values2.data - alternative_values1.data) * pref_factor
        )

    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix
        """
        return AdjacencyMatrix(
            DataFrame(
                [
                    [
                        self._pairwise_disconcordance(
                            performance_table.alternatives_values[ai],
                            performance_table.alternatives_values[aj],
                        )
                        for aj in performance_table.alternatives
                    ]
                    for ai in performance_table.alternatives
                ],
                index=performance_table.alternatives,
                columns=performance_table.alternatives,
            )
            / max(performance_table.data.apply(lambda x: max(x) - min(x)))
        )


class Electre1(_BaseElectre1, IElectre[OutrankingMatrix], Selector):
    """This class implements the Electre I algorithm.

    :param criteria_weights:
    :param c_hat: concordance threshold
    :param d_hat: discordance threshold
    """

    def __init__(
        self, criteria_weights: Dict[Any, float], c_hat: float, d_hat: float
    ):
        super().__init__(criteria_weights)
        self.c_hat = c_hat
        self.d_hat = d_hat

    def outranking(
        self,
        concordance_matrix: AdjacencyMatrix,
        discordance_matrix: AdjacencyMatrix,
    ) -> OutrankingMatrix:
        """Compute the outranking matrix using Electre I method.

        :param concordance_matrix: concordance matrix
        :param discordance_matrix: discordance matrix
        :return: the outranking matrix
        """
        ones = DataFrame(
            1,
            index=concordance_matrix.vertices,
            columns=concordance_matrix.vertices,
        )
        return OutrankingMatrix(
            ones[
                (concordance_matrix.data >= self.c_hat)
                & (discordance_matrix.data <= self.d_hat)
            ].fillna(0)
        )

    def construct(
        self, performance_table: PerformanceTable
    ) -> OutrankingMatrix:
        """Construct the outranking matrix using Electre I method.

        :param performance_table:
        :return: the outranking matrix of the performance table
        """
        return self.outranking(
            self.concordance(performance_table),
            self.discordance(performance_table),
        )

    def exploit(
        self,
        outranking_structure: OutrankingMatrix,
        cycle_reduction: bool = False,
        transitivity: bool = False,
        **kwargs,
    ) -> List:
        """Choose best alternative candidates from outranking matrix.

        It uses :meth:`OutrankingMatrix.kernel` to find the best candidates.

        :param outranking_structure:
        :param cycle_reduction:
            if ``True``, apply :attr:`.AdjacencyMatrix.cycle_reduction_matrix`
            to outranking matrix
        :param transitivity:
            if ``True``, apply :attr:`.AdjacencyMatrix.transitive_closure` to
            outranking matrix
        :return: best alternative candidates

        .. warning::
            if `outranking_matrix` kernel does not exist, it returns all
            alternatives
        """
        matrix = (
            outranking_structure.cycle_reduction_matrix
            if cycle_reduction
            else outranking_structure
        )
        matrix = matrix.transitive_closure if transitivity else matrix
        kernel = matrix.kernel
        return kernel if len(kernel) > 0 else outranking_structure.vertices

    def select(
        self,
        performance_table: PerformanceTable,
        cycle_reduction: bool = False,
        transitivity: bool = False,
        **kwargs,
    ) -> List:
        """Compute the outranking matrix using Electre I method.

        :param performance_table:
        :param cycle_reduction:
            if ``True``, apply :attr:`.AdjacencyMatrix.cycle_reduction_matrix`
            to outranking matrix
        :param transitivity:
            if ``True``, apply :attr:`.AdjacencyMatrix.transitive_closure` to
            outranking matrix
        :return: best alternative candidates

        .. warning::
            if `outranking_matrix` kernel does not exist, it returns all
            alternatives
        """
        matrix = self.construct(performance_table)
        return self.exploit(
            matrix, cycle_reduction=cycle_reduction, transitivity=transitivity
        )


class Electre2(
    _BaseElectre1, IElectre[Tuple[OutrankingMatrix, OutrankingMatrix]], Ranker
):
    """This class implements the Electre II algorithm.

    :param criteria_weights:
    :param c_hat: concordance thresholds (min, max)
    :param d_hat: discordance threshold (min, max)
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        c_hat: Tuple[float, float],
        d_hat: Tuple[float, float],
    ):
        super().__init__(criteria_weights)
        self.c_hat: Tuple[float, float] = c_hat
        self.d_hat: Tuple[float, float] = d_hat

    def outranking(
        self,
        concordance_matrix: AdjacencyMatrix,
        discordance_matrix: AdjacencyMatrix,
        strong: bool = True,
    ) -> OutrankingMatrix:
        """Calculate the outranking matrix according to given thresholds.

        :param concordance_matrix: concordance matrix
        :param discordance_matrix: discordance matrix
        :param strong:
            return strong outranking matrix if ``True``, weak otherwise
        :return: outranking matrix
        """
        c_hat = self.c_hat[1] if strong else self.c_hat[0]
        d_hat = self.d_hat[0] if strong else self.d_hat[1]
        ones = DataFrame(
            1,
            index=concordance_matrix.vertices,
            columns=concordance_matrix.vertices,
        )
        return OutrankingMatrix(
            ones[
                (concordance_matrix.data >= concordance_matrix.data.T)
                & (concordance_matrix.data >= c_hat)
                & (discordance_matrix.data <= d_hat)
            ].fillna(0)
        )

    @staticmethod
    def distillation(
        strong_outranking_matrix: OutrankingMatrix,
        weak_outranking_matrix: OutrankingMatrix,
        ascending: bool = False,
    ) -> OutrankingMatrix:
        """Compute distillation using outranking matrices.

        :param strong_outranking_matrix:
        :param weak_outranking_matrix:
        :param ascending:
            if ``True`` distillation is done in ascending direction
        :return: resulting ranking as an outranking matrix
        """
        axis = 1 if ascending else 0
        distillate = []
        rest = weak_outranking_matrix.vertices
        strong_outranking_matrix = cast(
            OutrankingMatrix, strong_outranking_matrix.cycle_reduction_matrix
        )
        weak_outranking_matrix = cast(
            OutrankingMatrix, weak_outranking_matrix.cycle_reduction_matrix
        )
        while len(rest) > 0:
            outranked = strong_outranking_matrix.data.loc[rest, rest].apply(
                sum, axis=axis
            )
            B = outranked[outranked == 0].index.tolist()
            outranked = weak_outranking_matrix.data.loc[B, B].apply(
                sum, axis=axis
            )
            A = outranked[outranked == 0].index.tolist()
            for i in A:
                rest.remove(i)
            distillate.append(A)
        # Build resulting OutrankingMatrix
        order = distillate[::-1] if ascending else distillate
        return OutrankingMatrix.from_ordered_alternatives_groups(order)

    def construct(
        self, performance_table: PerformanceTable
    ) -> Tuple[OutrankingMatrix, OutrankingMatrix]:
        """Compute strong and weak dominance outranking matrices.

        :param performance_table:
        :return: strong outranking matrix, weak outranking matrix
        """
        concordance_matrix = self.concordance(performance_table)
        discordance_matrix = self.discordance(performance_table)
        s_dominance_matrix = self.outranking(
            concordance_matrix,
            discordance_matrix,
        )
        w_dominance_matrix = self.outranking(
            concordance_matrix,
            discordance_matrix,
            strong=False,
        )
        return s_dominance_matrix, w_dominance_matrix

    def exploit(
        self,
        outranking_structure: Tuple[OutrankingMatrix, OutrankingMatrix],
        **kwargs,
    ) -> OutrankingMatrix:
        """Compute distillations and merge results.

        :param outranking_structure: strong and weak outranking matrices
        :return: result outranking matrix
        """
        strong_outranking_matrix, weak_outranking_matrix = outranking_structure
        return cast(
            OutrankingMatrix,
            self.distillation(
                strong_outranking_matrix,
                weak_outranking_matrix,
                ascending=True,
            )
            * self.distillation(
                strong_outranking_matrix,
                weak_outranking_matrix,
                ascending=False,
            ),
        )

    def rank(
        self, performance_table: PerformanceTable, **kwargs
    ) -> OutrankingMatrix:
        """Compute final outranking matrix for Electre II.

        :param performance_table:
        :return: result outranking matrix
        """
        return self.exploit(self.construct(performance_table))


class _BaseElectre3(ABC):
    """This class implements basic Electre III methods shared to other classes.

    :param criteria_weights:
    :param preference_thresholds:
    :param indifference_thresholds:
    :param veto_thresholds:
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        veto_thresholds: Dict[Any, float],
    ):
        self.criteria_weights = criteria_weights
        self.preference_thresholds = preference_thresholds
        self.indifference_thresholds = indifference_thresholds
        self.veto_thresholds = veto_thresholds

    @staticmethod
    def _concordance_index(
        ga: float,
        gb: float,
        pga: float,
        qga: float,
        preference_direction: PreferenceDirection,
    ) -> float:
        """Compute the concordance index between two alternatives wrt a
        criterion.

        :param ga: preference function of first alternative wrt criterion
        :param gb: preference function of second alternative wrt criterion
        :param pga: preference threshold for the criterion
        :param qga: indifference threshold for the criterion
        :param preference_direction:
        :return: concordance index value"""
        if pga < qga:
            raise ValueError(
                "Indifference value cannot be greater than preference value"
            )
        if (
            gb > (ga + pga) and preference_direction == PreferenceDirection.MAX
        ) or (
            gb < (ga - pga) and preference_direction == PreferenceDirection.MIN
        ):
            return 0
        if (
            gb <= (ga + qga)
            and preference_direction == PreferenceDirection.MAX
        ) or (
            gb >= (ga - qga)
            and preference_direction == PreferenceDirection.MIN
        ):
            return 1
        return (
            (ga + pga - gb) / (pga - qga)
            if preference_direction == PreferenceDirection.MAX
            else (-ga + pga + gb) / (pga - qga)
        )

    def _pairwise_concordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Compute the pairwise concordance between two alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :return: pairwise concordance value

        .. warning::
            this method assumes that alternatives values have the same scales
        """

        scales = cast(Dict[str, QuantitativeScale], alternative_values1.scales)
        return sum(
            self.criteria_weights[i]
            * self._concordance_index(
                alternative_values1[i],
                alternative_values2[i],
                self.preference_thresholds[i],
                self.indifference_thresholds[i],
                scales[i].preference_direction,
            )
            for i in self.criteria_weights
        ) / sum(self.criteria_weights.values())

    def concordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:
        """Compute the concordance matrix.

        :param performance_table:
        :return: concordance matrix
        """
        return AdjacencyMatrix(
            [
                [
                    self._pairwise_concordance(
                        performance_table.alternatives_values[ai],
                        performance_table.alternatives_values[aj],
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            vertices=performance_table.alternatives,
        )

    @staticmethod
    def _discordance_index(
        ga: float,
        gb: float,
        pga: float,
        vga: float,
        preference_direction: PreferenceDirection,
    ) -> float:
        """Compute the discordance index between two alternatives wrt a
        criterion.

        :param ga: preference function of first alternative wrt the criterion
        :param gb: preference function of second alternative wrt the criterion
        :param pga: preference threshold for the criterion
        :param vga:
            veto threshold for the criterion. ``None`` for the highest value
        :param preference_direction:
        :return: discordance index value"""
        if vga is not None and pga > vga:
            raise ValueError(
                "Preference value cannot be greater than Veto value"
            )
        if (
            vga is None
            or (
                gb <= (ga + pga)
                and preference_direction == PreferenceDirection.MAX
            )
            or (
                gb >= (ga - pga)
                and preference_direction == PreferenceDirection.MIN
            )
        ):
            return 0
        elif (
            gb > (ga + vga) and preference_direction == PreferenceDirection.MAX
        ) or (
            gb < (ga - vga) and preference_direction == PreferenceDirection.MIN
        ):
            return 1
        else:
            return (
                (gb - pga - ga) / (vga - pga)
                if preference_direction == PreferenceDirection.MAX
                else (-gb - pga + ga) / (vga - pga)
            )

    def _pairwise_disconcordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> Series:
        """Compute the discordance comparison of 2 alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :return: discordance indexes

        .. warning::
            this method assumes that alternatives values have the same scales
        """
        return Series(
            {
                j: self._discordance_index(
                    alternative_values1.data[j],
                    alternative_values2.data[j],
                    self.preference_thresholds[j],
                    self.veto_thresholds[j],
                    cast(
                        QuantitativeScale,
                        alternative_values1.scales[j],
                    ).preference_direction,
                )
                for j in alternative_values1.labels
            }
        )

    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> AdjacencyMatrix:
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix
        """
        return AdjacencyMatrix(
            [
                [
                    self._pairwise_disconcordance(
                        performance_table.alternatives_values[ai],
                        performance_table.alternatives_values[aj],
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            vertices=performance_table.alternatives,
        )

    @staticmethod
    def _pairwise_credibility_index(
        pairwise_concordance_: float,
        pairwise_discordance_: Series,
    ) -> float:
        """Compute the credibility index between two alternatives.

        :pairwise_concordance_:
            concordance value for criterion between both alternatives
        :pairwise_discordance_:
            discordance serie for criterion between both alternatives
        :return: pairwise credibility index
        """
        sup_discordance = pairwise_discordance_[
            pairwise_discordance_ > pairwise_concordance_
        ]
        S_ab = pairwise_concordance_
        if len(sup_discordance) > 0:
            for Di_ab in sup_discordance:
                S_ab = S_ab * (1 - Di_ab) / (1 - pairwise_concordance_)
        return S_ab

    def credibility(
        self, performance_table: PerformanceTable
    ) -> AdjacencyMatrix:
        """Compute the credibility matrix.

        :param performance_table:
        :return: credibility matrix
        """
        concordance_matrix = self.concordance(
            performance_table,
        )
        discordance_matrix = self.discordance(
            performance_table,
        )
        return AdjacencyMatrix(
            [
                [
                    self._pairwise_credibility_index(
                        concordance_matrix.data.loc[i, j],
                        discordance_matrix.data.loc[i, j],
                    )
                    for j in performance_table.alternatives
                ]
                for i in performance_table.alternatives
            ],
            vertices=performance_table.alternatives,
        )


class Electre3(_BaseElectre3, IElectre[AdjacencyMatrix], Ranker):
    """This class implements the Electre III algorithm.

    :param criteria_weights:
    :param preference_thresholds:
    :param indifference_thresholds:
    :param veto_thresholds:
    :param alpha:  preset up values of distillation coefficients
    :param beta: preset up values of distillation coefficients
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        veto_thresholds: Dict[Any, float],
        alpha: float = 0.30,
        beta: float = -0.15,
    ):
        super().__init__(
            criteria_weights,
            preference_thresholds,
            indifference_thresholds,
            veto_thresholds,
        )
        self.alpha = alpha
        self.beta = beta

    def construct(
        self, performance_table: PerformanceTable
    ) -> AdjacencyMatrix:
        """Construct outranking structure which is the credibility matrix.

        :param performance_table:
        :return: credibility matrix
        """
        return self.credibility(performance_table)

    def qualification(self, credibility_mat: AdjacencyMatrix) -> Series:
        """Compute the qualification for each pair of alternatives a and b.

        :param credibility_mat:
        :return: qualifications
        """
        lambda_max = max(credibility_mat.data.apply(max))
        lambda_ = lambda_max - (self.alpha + self.beta * lambda_max)

        lambda_strengths = Series(
            {
                i: sum(
                    (
                        credibility_mat.data.loc[i, j] > lambda_
                        and credibility_mat.data.loc[i, j]
                        > credibility_mat.data.loc[j, i]
                    )
                    for j in credibility_mat.vertices
                )
                for i in credibility_mat.vertices
            }
        )

        lambda_weakness = Series(
            {
                j: sum(
                    (
                        credibility_mat.data.loc[i, j] > lambda_
                        and credibility_mat.data.loc[i, j]
                        > credibility_mat.data.loc[j, i]
                    )
                    for i in credibility_mat.vertices
                )
                for j in credibility_mat.vertices
            }
        )

        return lambda_strengths - lambda_weakness

    def distillation(
        self,
        credibility_matrix: AdjacencyMatrix,
        ascending: bool = False,
    ) -> OutrankingMatrix:
        """Compute distillation.

        :param credibility_matrix:
        :param ascending: if ``True`` distillation is performed in ascension
        :return: ranking of categories
        """
        comp = min if ascending else max

        rest = credibility_matrix.vertices
        distillate = []
        while len(rest) > 0:
            updated_credibility_mat = AdjacencyMatrix(
                credibility_matrix.data.loc[rest, rest]
            )
            qualifications = self.qualification(
                updated_credibility_mat,
            )

            maxes = qualifications[qualifications == comp(qualifications)]
            if len(maxes) > 1:
                updated_credibility_mat = AdjacencyMatrix(
                    updated_credibility_mat.data.loc[maxes.index, maxes.index]
                )
                qualifications = self.qualification(
                    updated_credibility_mat,
                )
                maxes = qualifications[qualifications == comp(qualifications)]
            distillate.append(maxes.index.tolist())
            for i in maxes.index.tolist():
                rest.remove(i)
        order = distillate[::-1] if ascending else distillate
        return OutrankingMatrix.from_ordered_alternatives_groups(order)

    def exploit(
        self, outranking_structure: AdjacencyMatrix, **kwargs
    ) -> OutrankingMatrix:
        """Compute the complete Electre III exploitation phase.

        :param outranking_structure: credibility matrix
        :return: final outranking matrix
        """
        return cast(
            OutrankingMatrix,
            self.distillation(outranking_structure, ascending=True)
            * self.distillation(outranking_structure, ascending=False),
        )

    def rank(
        self, performance_table: PerformanceTable, **kwargs
    ) -> OutrankingMatrix:
        """Compute the complete Electre III algorithm

        :param performance_table:
        :return: final outranking matrix
        """
        return self.exploit(self.construct(performance_table))


class ElectreTri(_BaseElectre3, IElectre[AdjacencyMatrix], Assignator):
    """This class implements the Electre-Tri B algorithm.

    :param criteria_weights:
    :param profiles: profiles in ascending dominance order
    :param preference_thresholds:
    :param indifference_thresholds:
    :param veto_thresholds:
    :param lambda_: cut level
    :param categories: categories in ascending ranking order
    :raise ValueError:
        * if length of `categories` is not length of `profiles` + 1
        * if the profiles are not in ascending dominance order

    :attr category_profiles:
        category profiles formed using `categories` and `profiles`

    .. note::
        Implementation and naming conventions are taken from
        :cite:p:`vincke1998electreTRI`.
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        profiles: PerformanceTable,
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        veto_thresholds: Dict[Any, float],
        lambda_: float,
        categories: List = None,
    ):
        super().__init__(
            criteria_weights,
            preference_thresholds,
            indifference_thresholds,
            veto_thresholds,
        )
        categories = (
            list(range(len(profiles.alternatives) + 1))
            if categories is None
            else categories
        )
        if len(categories) != len(profiles.alternatives) + 1:
            raise ValueError(
                "there must be exactly one more category than profiles"
            )
        self.profiles = profiles
        self.category_profiles: Dict[Any, BoundedCategoryProfile] = dict(
            zip(
                categories,
                BoundedCategoryProfile.profiles_partition(self.profiles),
            )
        )
        self.lambda_ = lambda_

    def construct(
        self, performance_table: PerformanceTable
    ) -> AdjacencyMatrix:
        """Construct alternatives and profiles credibility matrix.

        Returned credibility matrix concatenates `performance_table`
        and :attr:`profiles` (in that order).

        :param performance_table:
        :return:
        :raise IndexError: if profiles and alternatives share some labels
        """
        common_labels = set(performance_table.alternatives).intersection(
            set(self.profiles.alternatives)
        )
        if len(common_labels) != 0:
            raise IndexError(
                "profiles and alternatives must have different labels. "
                f"Common labels: {common_labels}"
            )

        # Transform profiles to performance table scales
        _profiles = self.profiles.transform(performance_table.scales)

        # Concatenate performance table and category profiles
        altered_performance_table = PerformanceTable.concat(
            [performance_table, _profiles], axis=0
        )

        return self.credibility(altered_performance_table)

    def _pairwise_outrank(
        self,
        credibility_mat: AdjacencyMatrix,
        label1: Any,
        label2: Any,
    ) -> bool:
        """Check whether first label outranks second.

        :param credibility_mat:
        :param label1:
        :param label2:
        :return: ``True`` if `label1` outranks `label2`, ``False`` otherwise
        """
        aSb = cast(float, credibility_mat.data.at[label1, label2])
        return aSb >= self.lambda_

    def _pairwise_relation(
        self,
        credibility_mat: AdjacencyMatrix,
        label1: Any,
        label2: Any,
    ) -> Relation:
        """Compute relation between two actions based on credibility matrix.

        :param credibility_mat:
            credibility matrix of concatenated performance table / profiles
        :param label1:
        :param label2:
        :return: relationship between both alternatives
        """
        aSb = cast(float, credibility_mat.data.at[label1, label2])
        bSa = cast(float, credibility_mat.data.at[label2, label1])
        if aSb >= self.lambda_ and bSa >= self.lambda_:
            return IndifferenceRelation(label1, label2)
        elif aSb >= self.lambda_ > bSa:
            return PreferenceRelation(label1, label2)
        elif aSb < self.lambda_ <= bSa:
            return PreferenceRelation(label2, label1)
        return IncomparableRelation(label1, label2)

    def _exploit_pessimistic(
        self, outranking_structure: AdjacencyMatrix
    ) -> Dict[Any, Set]:
        """Compute the exploitation procedure pessimistically.

        :param outranking_structure: credibility matrix
        :return: categories
        """
        rest = set(outranking_structure.vertices) - set(
            self.profiles.alternatives
        )
        categories = list(self.category_profiles.keys())
        classes: Dict[Any, Set] = {category: set() for category in categories}
        for cat, cat_profile in reversed(
            list(self.category_profiles.items())[1:]
        ):
            assigned = set()
            for a in rest:
                if self._pairwise_outrank(
                    outranking_structure,
                    a,
                    cast(ScaleValues, cat_profile.lower).name,
                ):
                    classes[cat].add(a)
                    assigned.add(a)
            rest -= assigned
        classes[categories[0]] = rest
        return classes

    def _exploit_optimistic(
        self, outranking_structure: AdjacencyMatrix
    ) -> Dict[Any, Set]:
        """Compute the exploitation procedure optimistically.

        :param outranking_structure: credibility matrix
        :return: categories
        """
        rest = set(outranking_structure.vertices) - set(
            self.profiles.alternatives
        )
        categories = list(self.category_profiles.keys())
        classes: Dict[Any, Set] = {}
        for cat, cat_profile in list(self.category_profiles.items())[:-1]:
            assigned = set()
            profile = cast(ScaleValues, cat_profile.upper).name
            for a in rest:
                pref = PreferenceRelation(
                    profile,
                    a,
                )
                if (
                    self._pairwise_relation(
                        outranking_structure,
                        profile,
                        a,
                    )
                    == pref
                ):
                    assigned.add(a)
            classes[cat] = assigned
            rest -= assigned
        classes[categories[-1]] = rest
        return classes

    def exploit(
        self,
        outranking_structure: AdjacencyMatrix,
        pessimistic: bool = False,
        **kwargs,
    ) -> Dict[Any, Set]:
        """Compute the exploitation procedure (either optimistically or
        pessimistically).

        :param outranking_structure: credibility matrix
        :param pessimistic: if ``True`` performs procedure pessimistically
        :return: categories in ascending domination order

        .. note::
            the category profiles defining the categories are the ones from
            :attr:`category_profiles`
        """
        return (
            self._exploit_pessimistic(outranking_structure)
            if pessimistic
            else self._exploit_optimistic(outranking_structure)
        )

    def assign(
        self,
        performance_table: PerformanceTable,
        pessimistic: bool = False,
        **kwargs,
    ) -> Dict[Any, Set]:
        """Compute the exploitation procedure (either optimistically or
        pessimistically).

        :param performance_table:
        :param pessimistic:
        :return: categories in ascending domination order

        .. note::
            the category profiles defining the categories are the ones from
            :attr:`category_profiles`
        """
        return self.exploit(
            self.construct(performance_table=performance_table),
            pessimistic=pessimistic,
        )
