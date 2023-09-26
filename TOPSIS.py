import pandas as pd
import streamlit as st

st.title("Multi-Criteria Decision Making with TOPSIS")

st.markdown(
    "**TOPSIS**, or the Technique for Order of Preference by Similarity to Ideal Solution, is a multi-criteria decision analysis method. This method is used to determine the best solution from a set of alternatives, based on multiple criteria or attributes. The basic idea behind TOPSIS is to identify solutions that are closest to the ideal solution and furthest from the anti-ideal or negative-ideal solution."
)

st.write("For more information see:")

st.markdown(
    'Hwang, C.L.; Lai, Y.J.; Liu, T.Y. (1993). "A new approach for multiple objective decision making". _Computers and Operational Research_. **20** (8): 889-899. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1016/0305-0548(93)90109-v](https://doi.org/10.1016%2F0305-0548%2893%2990109-v).'
)

st.header("Options")

options = pd.DataFrame(columns=["Option"])

st.write("1. Add options in the table below.")

edited_options = st.data_editor(options, num_rows="dynamic")

st.header("Critera and Score")

options_list = edited_options["Option"].tolist()

criteria_scores = pd.DataFrame(
    columns=["Criterion", "Weight", "Is Negative", *options_list]
)
criteria_scores["Criterion"] = criteria_scores["Criterion"].astype(str)
criteria_scores["Weight"] = criteria_scores["Weight"].astype(float)
criteria_scores["Is Negative"] = criteria_scores["Is Negative"].astype(bool)

st.write(
    "2. Add criteria, weights, and specify if the criterion is negative. Provide scores for each option."
)

edited_criteria_scores = st.data_editor(criteria_scores, num_rows="dynamic")

st.header("Options preference")

if not edited_criteria_scores.empty:
    melted_df = edited_criteria_scores.melt(
        id_vars=["Criterion", "Weight", "Is Negative"],
        var_name="Option",
        value_name="Score",
    )
    melted_df["Score"] = melted_df["Score"].astype(float)

    normalization_factor = melted_df
    normalization_factor["SqueredScore"] = normalization_factor["Score"] ** 2
    normalization_factor = (
        normalization_factor.groupby("Criterion")["SqueredScore"]
        .sum()
        .reset_index()
        .rename(columns={"SqueredScore": "NormalizedScore"})
    )
    normalization_factor["NormalizedScore"] = (
        normalization_factor["NormalizedScore"] ** 0.5
    )

    normalized_weighted = melted_df.merge(
        normalization_factor, on="Criterion", how="left"
    )
    normalized_weighted["NormalizedScore"] = (
        normalized_weighted["Score"] / normalized_weighted["NormalizedScore"]
    )
    normalized_weighted["NormalizedWeightedScore"] = (
        normalized_weighted["NormalizedScore"] * normalized_weighted["Weight"]
    )
    normalized_weighted["Is Negative"] = normalized_weighted["Is Negative"].fillna(
        False
    )

    positive_criteria = normalized_weighted[normalized_weighted["Is Negative"] == False]
    best_positive = (
        positive_criteria.groupby("Criterion")["NormalizedWeightedScore"]
        .max()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "IdealBest"})
    )
    worst_positive = (
        positive_criteria.groupby("Criterion")["NormalizedWeightedScore"]
        .min()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "IdealWorst"})
    )

    negative_criteria = normalized_weighted[normalized_weighted["Is Negative"] == True]
    best_negative = (
        negative_criteria.groupby("Criterion")["NormalizedWeightedScore"]
        .min()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "IdealBest"})
    )
    worst_negative = (
        negative_criteria.groupby("Criterion")["NormalizedWeightedScore"]
        .max()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "IdealWorst"})
    )

    best_worst_positive = best_positive.merge(
        worst_positive, on="Criterion", how="left"
    )
    best_worst_negative = best_negative.merge(
        worst_negative, on="Criterion", how="left"
    )
    ideal_best_worst = pd.concat([best_worst_positive, best_worst_negative])

    normalized_weighted = normalized_weighted.merge(
        ideal_best_worst[["Criterion", "IdealBest", "IdealWorst"]],
        on="Criterion",
        how="left",
    )

    normalized_weighted["EuclidianDistanceBestPartial"] = (
        normalized_weighted["NormalizedWeightedScore"]
        - normalized_weighted["IdealBest"]
    ) ** 2
    normalized_weighted["EuclidianDistanceWorstPartial"] = (
        normalized_weighted["NormalizedWeightedScore"]
        - normalized_weighted["IdealWorst"]
    ) ** 2

    euclidian = (
        normalized_weighted.groupby("Option")[
            ["EuclidianDistanceBestPartial", "EuclidianDistanceWorstPartial"]
        ]
        .sum()
        .reset_index()
    )
    euclidian["EuclidianDistanceBest"] = (
        euclidian["EuclidianDistanceBestPartial"] ** 0.5
    )
    euclidian["EuclidianDistanceWorst"] = (
        euclidian["EuclidianDistanceWorstPartial"] ** 0.5
    )
    euclidian["Performance Score"] = euclidian["EuclidianDistanceWorst"] / (
        euclidian["EuclidianDistanceBest"] + euclidian["EuclidianDistanceWorst"]
    )

    euclidian["Rank"] = euclidian["Performance Score"].rank(ascending=False)

    st.dataframe(euclidian[["Option", "Performance Score", "Rank"]], hide_index=True)

st.markdown(
    "Made with ❤️ by Maurycy Blaszczak ([maurycyblaszczak.com](https://maurycyblaszczak.com/))"
)
