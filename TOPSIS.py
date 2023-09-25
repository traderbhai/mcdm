import streamlit as st
import pandas as pd

st.title("Multi-Criteria Decision Making with TOPSIS")

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

st.write("2. Add criteria, weights, specify if negative, and scores for each option.")

edited_criteria_scores = st.data_editor(criteria_scores, num_rows="dynamic")

st.header("Options preference")

if not edited_criteria_scores.empty:
    melted = edited_criteria_scores.melt(
        id_vars=["Criterion", "Weight", "Is Negative"],
        var_name="Option",
    )
    melted["value"] = melted["value"].astype(float)

    normalization = melted
    normalization["Squered"] = normalization["value"] ** 2
    normalization = (
        normalization.groupby("Criterion")["Squered"]
        .sum()
        .reset_index()
        .rename(columns={"Squered": "Normalization"})
    )
    normalization["Normalization"] = normalization["Normalization"] ** 0.5

    full_matrix = melted.merge(normalization, on="Criterion", how="left")
    full_matrix["NormalizedScore"] = full_matrix["value"] / full_matrix["Normalization"]
    full_matrix["NormalizedWeightedScore"] = (
        full_matrix["NormalizedScore"] * full_matrix["Weight"]
    )

    full_matrix["Is Negative"] = full_matrix["Is Negative"].fillna(False)
    positive = full_matrix[full_matrix["Is Negative"] == False]
    max_positive = (
        positive.groupby("Criterion")["NormalizedWeightedScore"]
        .max()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "Max"})
    )
    min_positive = (
        positive.groupby("Criterion")["NormalizedWeightedScore"]
        .min()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "Min"})
    )

    negative = full_matrix[full_matrix["Is Negative"] == True]
    max_negative = (
        negative.groupby("Criterion")["NormalizedWeightedScore"]
        .min()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "Max"})
    )
    min_negative = (
        negative.groupby("Criterion")["NormalizedWeightedScore"]
        .max()
        .reset_index()
        .rename(columns={"NormalizedWeightedScore": "Min"})
    )

    max_min_positive = max_positive.merge(min_positive, on="Criterion", how="left")
    max_min_negative = max_negative.merge(min_negative, on="Criterion", how="left")
    max_min = pd.concat([max_min_positive, max_min_negative])

    full_matrix = full_matrix.merge(
        max_min[["Criterion", "Max", "Min"]], on="Criterion", how="left"
    )

    full_matrix["plus"] = (
        full_matrix["NormalizedWeightedScore"] - full_matrix["Max"]
    ) ** 2
    full_matrix["minus"] = (
        full_matrix["NormalizedWeightedScore"] - full_matrix["Min"]
    ) ** 2

    euclidian = full_matrix.groupby("Option")[["plus", "minus"]].sum().reset_index()
    euclidian["plus"] = euclidian["plus"] ** 0.5
    euclidian["minus"] = euclidian["minus"] ** 0.5
    euclidian["Performance Score"] = euclidian["minus"] / (
        euclidian["plus"] + euclidian["minus"]
    )

    euclidian["Rank"] = euclidian["Performance Score"].rank(ascending=False)

    st.dataframe(euclidian[["Option", "Performance Score", "Rank"]])
