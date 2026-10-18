
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Enterprise AI Model Selection",
    page_icon="🤖",
    layout="wide"
)

# 1. Load data
@st.cache_data
def load_data():
    df = pd.read_csv("models_full.csv")

    price_cols = [
        "latest_input_price_per_1m",
        "latest_output_price_per_1m",
        "latest_cached_input_price_per_1m"
    ]

    for col in price_cols + ["context_window"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in [
        "api_available",
        "is_deprecated",
        "supports_vision",
        "supports_tool_use"
    ]:
        df[col] = df[col].astype("string").str.lower()

    df["modalities"] = df["modalities"].fillna("unknown")

    return df


df = load_data()

# 2. Page title
st.title("Enterprise AI Model Selection Dashboard")

st.caption(
    "For AI Engineering Managers: identify AI models that meet "
    "business requirements and compare their estimated API costs."
)

st.info(
    "Data: Kaggle model snapshot, August 13, 2026. "
    "Proposed production refresh: weekly. "
    "Prices must be verified before purchasing."
)

# 3. Business requirements in sidebar
st.sidebar.header("Business Requirements")

providers = sorted(df["provider_name"].dropna().unique())

selected_providers = st.sidebar.multiselect(
    "AI Providers",
    providers,
    default=providers
)

required_modality = st.sidebar.selectbox(
    "Required Modality",
    ["Text only", "Image input", "Audio capability"]
)

need_tools = st.sidebar.checkbox(
    "Require tool calling"
)

min_context = st.sidebar.number_input(
    "Minimum Context Window (tokens)",
    min_value=0,
    value=0,
    step=16000
)

st.sidebar.header("Monthly API Usage")

input_tokens = st.sidebar.number_input(
    "Input Tokens (millions)",
    min_value=0.0,
    value=100.0,
    step=10.0
)

output_tokens = st.sidebar.number_input(
    "Output Tokens (millions)",
    min_value=0.0,
    value=20.0,
    step=5.0
)

monthly_budget = st.sidebar.number_input(
    "Monthly API Budget (USD)",
    min_value=0.0,
    value=500.0,
    step=50.0
)

# 4. Filter models by hard requirements
eligible = df[
    (df["api_available"] == "true") &
    (df["is_deprecated"] == "false") &
    (df["provider_name"].isin(selected_providers))
].copy()

if required_modality == "Image input":
    eligible = eligible[
        (eligible["modalities"].str.contains(
            "vision", case=False, na=False
        )) &
        (eligible["supports_vision"] == "true")
    ]

elif required_modality == "Audio capability":
    eligible = eligible[
        eligible["modalities"].str.contains(
            "audio", case=False, na=False
        )
    ]

if need_tools:
    eligible = eligible[
        eligible["supports_tool_use"] == "true"
    ]

eligible = eligible[
    eligible["context_window"] >= min_context
] if min_context > 0 else eligible

# 5. Estimate monthly API cost
# Prices are USD per one million tokens.
eligible["monthly_cost"] = (
    input_tokens * eligible["latest_input_price_per_1m"].fillna(0)
    + output_tokens * eligible["latest_output_price_per_1m"].fillna(0)
)

# A price is required only when that token volume is positive.
known_cost = pd.Series(True, index=eligible.index)

if input_tokens > 0:
    known_cost &= eligible["latest_input_price_per_1m"].notna()

if output_tokens > 0:
    known_cost &= eligible["latest_output_price_per_1m"].notna()

known_cost &= eligible["latest_price_currency"].eq("USD")

priced = eligible[known_cost].copy()
priced = priced.sort_values("monthly_cost")

affordable = priced[
    priced["monthly_cost"] <= monthly_budget
].copy()

# 6. Headline metrics
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Technically Eligible Models",
    len(eligible)
)

col2.metric(
    "Models Within Budget",
    len(affordable)
)

min_cost = priced["monthly_cost"].min()

col3.metric(
    "Lowest Estimated Monthly Cost",
    f"${min_cost:,.2f}" if pd.notna(min_cost) else "N/A"
)

# 7. Supporting chart
st.subheader("Estimated Monthly API Cost")

if not priced.empty:
    chart_data = priced.head(10).set_index("model_name")

    st.bar_chart(
        chart_data[["monthly_cost"]],
        horizontal=True,
        x_label="Estimated monthly cost (USD)",
        y_label="Model"
    )

    st.caption(
        "Ten lowest-cost models that meet the selected technical "
        "requirements and have usable price data. "
        "Models above the budget are also shown for comparison."
    )

else:
    st.warning(
        "No eligible models with complete pricing information "
        "for this workload."
    )

# 8. Candidate shortlist
st.subheader("Candidates Within Budget")

if affordable.empty:
    st.warning(
        "No priced model meets all selected requirements "
        "within the budget. Consider revisiting the budget "
        "or technical requirements."
    )
else:
    table_cols = [
        "model_name",
        "provider_name",
        "modalities",
        "context_window",
        "supports_tool_use",
        "latest_input_price_per_1m",
        "latest_output_price_per_1m",
        "monthly_cost",
        "source_url"
    ]

    shortlist = affordable[table_cols].rename(columns={
        "model_name": "Model",
        "provider_name": "Provider",
        "modalities": "Modalities",
        "context_window": "Context Window",
        "supports_tool_use": "Tool Calling",
        "latest_input_price_per_1m": "Input Price / 1M",
        "latest_output_price_per_1m": "Output Price / 1M",
        "monthly_cost": "Monthly Cost (USD)",
        "source_url": "Official Source"
    })

    st.dataframe(
        shortlist,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Official Source": st.column_config.LinkColumn(
                "Official Source"
            ),
            "Monthly Cost (USD)": st.column_config.NumberColumn(
                "Monthly Cost (USD)",
                format="$%.2f"
            )
        }
    )

# 9. Data limitations
with st.expander("Data Notes & Limitations"):
    st.write(
        f"{len(eligible) - len(priced)} technically eligible "
        "models lack usable pricing data for this workload."
    )
    st.write(
        "Cost estimates use the same input and output token "
        "volumes for every model. They do not include cached "
        "input discounts, hosting fees, taxes, retries, or "
        "other API charges."
    )
    st.write(
        "Modality flags describe reported capabilities, "
        "not their quality or suitability for a specific task. "
        "Audio capability does not specify input/output direction."
    )
    st.write(
        "Benchmark coverage is sparse and evaluation conditions "
        "may differ. Models must be tested on real business "
        "tasks before deployment."
    )
    st.write(
        "This version uses a historical CSV snapshot. "
        "Weekly data refresh is a proposed production policy, "
        "not an automated feature of this app."
    )
