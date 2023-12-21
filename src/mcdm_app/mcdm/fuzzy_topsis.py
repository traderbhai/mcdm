from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TriangularFuzzyNumber:
    a: Decimal
    b: Decimal
    c: Decimal

    def __post_init__(self):
        if self.a < 0 or self.b < 0 or self.c < 0:
            raise ValueError
        if not (self.a <= self.b <= self.c):
            raise ValueError

    def __mul__(self, other: "TriangularFuzzyNumber | Decimal") -> "TriangularFuzzyNumber":
        if isinstance(other, TriangularFuzzyNumber):
            return TriangularFuzzyNumber(
                self.a * other.a,
                self.b * other.b,
                self.c * other.c,
            )
        return TriangularFuzzyNumber(
            self.a * other,
            self.b * other,
            self.c * other,
        )

    def __truediv__(self, other: "TriangularFuzzyNumber | Decimal") -> "TriangularFuzzyNumber":
        if isinstance(other, TriangularFuzzyNumber):
            return TriangularFuzzyNumber(
                self.a / other.a,
                self.b / other.b,
                self.c / other.c,
            )
        return TriangularFuzzyNumber(
            self.a / other,
            self.b / other,
            self.c / other,
        )

    def __pow__(self, other: Decimal) -> "TriangularFuzzyNumber":
        if other < 0:
            return TriangularFuzzyNumber(
                Decimal("1") / (self.c ** abs(other)),
                Decimal("1") / (self.b ** abs(other)),
                Decimal("1") / (self.a ** abs(other)),
            )
        return TriangularFuzzyNumber(
            self.a**other,
            self.b**other,
            self.c**other,
        )

    def __lt__(self, other: "TriangularFuzzyNumber") -> bool:
        return self.a < other.a

    def __le__(self, other: "TriangularFuzzyNumber") -> bool:
        return self.a < other.a or self == other

    def __gt__(self, other: "TriangularFuzzyNumber") -> bool:
        return self.c > other.c

    def __ge__(self, other: "TriangularFuzzyNumber") -> bool:
        return self.c > other.c or self == other

    @staticmethod
    def combine(fuzzy_numbers: list["TriangularFuzzyNumber"], how: Optional[str] = None) -> "TriangularFuzzyNumber":
        if how == "max":
            return TriangularFuzzyNumber(
                max(number.a for number in fuzzy_numbers),
                max(number.b for number in fuzzy_numbers),
                max(number.c for number in fuzzy_numbers),
            )

        if how == "min":
            return TriangularFuzzyNumber(
                min(number.a for number in fuzzy_numbers),
                min(number.b for number in fuzzy_numbers),
                min(number.c for number in fuzzy_numbers),
            )

        return TriangularFuzzyNumber(
            min(number.a for number in fuzzy_numbers),
            sum(number.b for number in fuzzy_numbers) / Decimal(len(fuzzy_numbers)),
            max(number.c for number in fuzzy_numbers),
        )

    @staticmethod
    def euclidean_distance(left: "TriangularFuzzyNumber", right: "TriangularFuzzyNumber") -> Decimal:
        return (
            (
                (left.a - right.a) ** Decimal("2")
                + (left.b - right.b) ** Decimal("2")
                + (left.c - right.c) ** Decimal("2")
            )
            / Decimal("3")
        ) ** Decimal("0.5")


def combine_decision_makers(decision_matrixes: pd.DataFrame) -> pd.DataFrame:
    decision_combined = (
        decision_matrixes.groupby(["Option", "Criterion", "Is Negative"])
        .agg(
            {
                "Weight": lambda x: TriangularFuzzyNumber.combine(x.tolist()),
                "Score": lambda x: TriangularFuzzyNumber.combine(x.tolist()),
            }
        )
        .reset_index()
    )

    return decision_combined


def calculate_normalized_fuzzy_decision_matrix(combined_decision_matrix: pd.DataFrame) -> pd.DataFrame:
    benefit_criteria = combined_decision_matrix[~combined_decision_matrix["Is Negative"]]
    c_max = (
        benefit_criteria.groupby("Criterion")["Score"]
        .agg(lambda series: np.max(series.apply(lambda score: score.c)))
        .reset_index(name="NormalizationFactor")  # pyright: ignore
    )

    cost_criteria = combined_decision_matrix[combined_decision_matrix["Is Negative"]]
    a_min = (
        cost_criteria.groupby("Criterion")["Score"]
        .agg(lambda series: np.min(series.apply(lambda score: score.a)))
        .reset_index(name="NormalizationFactor")  # pyright: ignore
    )

    normalization_factor = pd.concat([c_max, a_min])

    matrix_with_factor = combined_decision_matrix.merge(normalization_factor, on="Criterion", how="left")

    matrix_with_factor["NormalizedScore"] = np.where(
        matrix_with_factor["Is Negative"],
        matrix_with_factor["Score"] ** -1 * matrix_with_factor["NormalizationFactor"],
        matrix_with_factor["Score"] / matrix_with_factor["NormalizationFactor"],
    )

    return matrix_with_factor


def calculate_weighted_normalized_fuzzy_decision_matrix(normalized_fuzzy_decision_matrix: pd.DataFrame) -> pd.DataFrame:
    normalized_fuzzy_decision_matrix["WeightedNormalizedScore"] = (
        normalized_fuzzy_decision_matrix["NormalizedScore"] * normalized_fuzzy_decision_matrix["Weight"]
    )

    return normalized_fuzzy_decision_matrix


def calculate_ideal_solutions(weighted_normalized_fuzzy_decision_matrix: pd.DataFrame) -> pd.DataFrame:
    ideal_best = (
        weighted_normalized_fuzzy_decision_matrix.groupby("Criterion")["WeightedNormalizedScore"]
        .agg(lambda x: TriangularFuzzyNumber.combine(x, how="max"))
        .reset_index(name="IdealBest")  # pyright: ignore
    )
    ideal_worst = (
        weighted_normalized_fuzzy_decision_matrix.groupby("Criterion")["WeightedNormalizedScore"]
        .agg(lambda x: TriangularFuzzyNumber.combine(x, how="min"))
        .reset_index(name="IdealWorst")  # pyright: ignore
    )

    with_ideal_best_worst = weighted_normalized_fuzzy_decision_matrix.merge(
        ideal_best, on="Criterion", how="left"
    ).merge(ideal_worst, on="Criterion", how="left")
    return with_ideal_best_worst


def calculate_distance_from_solutions(with_ideal_solutions: pd.DataFrame) -> pd.DataFrame:
    with_ideal_solutions["DistanceBest"] = with_ideal_solutions.apply(
        lambda row: TriangularFuzzyNumber.euclidean_distance(row["WeightedNormalizedScore"], row["IdealBest"]),
        axis=1,
    )
    with_ideal_solutions["DistanceWorst"] = with_ideal_solutions.apply(
        lambda row: TriangularFuzzyNumber.euclidean_distance(row["WeightedNormalizedScore"], row["IdealWorst"]),
        axis=1,
    )
    return with_ideal_solutions


def calculate_closeness_coefficient(distance_from_solutions: pd.DataFrame) -> pd.DataFrame:
    distance_per_option = (
        distance_from_solutions.groupby("Option")
        .agg(
            {
                "DistanceBest": "sum",
                "DistanceWorst": "sum",
            }
        )
        .reset_index()
    )

    distance_per_option["ClosenessCoefficient"] = distance_per_option["DistanceWorst"] / (
        distance_per_option["DistanceWorst"] + distance_per_option["DistanceBest"]
    )

    distance_per_option["Rank"] = distance_per_option["ClosenessCoefficient"].rank(ascending=False)
    return distance_per_option


def calculate_fuzzy_topsis(decision_matrixes: pd.DataFrame) -> pd.DataFrame:
    return calculate_closeness_coefficient(
        calculate_distance_from_solutions(
            calculate_ideal_solutions(
                calculate_weighted_normalized_fuzzy_decision_matrix(
                    calculate_normalized_fuzzy_decision_matrix(combine_decision_makers(decision_matrixes))
                )
            )
        )
    )[["Option", "ClosenessCoefficient", "Rank"]].rename(columns={"ClosenessCoefficient": "Performance Score"})  # pyright: ignore
