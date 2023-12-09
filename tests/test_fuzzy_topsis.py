from decimal import Decimal

import pandas as pd

from mcdm_app.mcdm.fuzzy_topsis import TriangularFuzzyNumber, calculate_fuzzy_topsis

data_in = pd.DataFrame(
    {
        "Option": {
            0: "O1",
            1: "O1",
            2: "O1",
            3: "O2",
            4: "O2",
            5: "O2",
            6: "O3",
            7: "O3",
            8: "O3",
            9: "O4",
            10: "O4",
            11: "O4",
        },
        "Criterion": {
            0: "C1",
            1: "C2",
            2: "C3",
            3: "C1",
            4: "C2",
            5: "C3",
            6: "C1",
            7: "C2",
            8: "C3",
            9: "C1",
            10: "C2",
            11: "C3",
        },
        "Is Negative": {
            0: False,
            1: False,
            2: True,
            3: False,
            4: False,
            5: True,
            6: False,
            7: False,
            8: True,
            9: False,
            10: False,
            11: True,
        },
        "Weight": {
            0: "5,7,9",
            1: "7,9,9",
            2: "3,5,7",
            3: "5,7,9",
            4: "7,9,9",
            5: "3,5,7",
            6: "5,7,9",
            7: "7,9,9",
            8: "3,5,7",
            9: "5,7,9",
            10: "7,9,9",
            11: "3,5,7",
        },
        "Score": {
            0: "3,5,7",
            1: "5,7,9",
            2: "5,7,9",
            3: "5,7,9",
            4: "3,5,7",
            5: "3,5,7",
            6: "5,7,9",
            7: "3,5,7",
            8: "1,3,5",
            9: "1,1,3",
            10: "1,3,5",
            11: "1,1,3",
        },
    }
)

data_out = pd.DataFrame(
    {
        "Option": {0: "O1", 1: "O2", 2: "O3", 3: "O4"},
        "Performance Score": {
            0: Decimal("0.5229085207146214868662810814"),
            1: Decimal("0.5314055553937191891384368032"),
            2: Decimal("0.6646060148641092460205184193"),
            3: Decimal("0.3714941371683631216678094040"),
        },
        "Rank": {0: 3.0, 1: 2.0, 2: 1.0, 3: 4.0},
    }
)


def test_calculate_fuzzy_topsis():
    data_in["Weight"] = data_in["Weight"].apply(
        lambda x: TriangularFuzzyNumber(
            Decimal(x.split(",")[0]),
            Decimal(x.split(",")[1]),
            Decimal(x.split(",")[2]),
        )
    )
    data_in["Score"] = data_in["Score"].apply(
        lambda x: TriangularFuzzyNumber(
            Decimal(x.split(",")[0]),
            Decimal(x.split(",")[1]),
            Decimal(x.split(",")[2]),
        )
    )

    assert calculate_fuzzy_topsis(data_in).equals(data_out)
