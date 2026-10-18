import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Enterprise AI Model Selection — Home",
    page_icon="🤖",
    layout="wide"
)

@st.cache_data
def load_data(csv_path: str = "models_full.csv") -> pd.DataFrame:
    csv = Path(csv_path)
    if not csv.exists():
        return pd.DataFrame()

    df = pd.read_csv(csv_path)

    price_cols = [
        "latest_input_price_per_1m",
        "latest_output_price_per_1m",
        "latest_cached_input_price_per_1m"
    ]

    for col in price_cols + ["context_window"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in [
        "api_available",
        "is_deprecated",
        "supports_vision",
        "supports_tool_use"
    ]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.lower()

    if "modalities" in df.columns:
        df["modalities"] = df["modalities"].fillna("unknown")

    return df


st.title("Enterprise AI Model Selection")
st.markdown(
    "欢迎使用 Enterprise AI Model Selection 仪表盘。这个项目帮助 AI 工程经理快速筛选满足业务需求的模型、比较估算的 API 成本，并查看模型的关键能力。"
)

st.write("---")

# Load data (if available)
df = load_data()

if df.empty:
    st.warning(
        "未找到数据文件 models_full.csv。请确保在运行本应用的工作目录中存在该文件，或者在项目根目录下运行 `streamlit run app.py`。"
    )
    st.stop()

# Quick metrics
st.subheader("快速概览")
col1, col2, col3, col4 = st.columns(4)

col1.metric("总模型数量", int(df.shape[0]))
col2.metric("可用提供商数量", int(df["provider_name"].nunique()))

priced_mask = df["latest_price_currency"].fillna("") == "USD"
col3.metric("含美元定价的模型", int(priced_mask.sum()))

if "context_window" in df.columns:
    median_ctx = int(df["context_window"].dropna().median()) if not df["context_window"].dropna().empty else "N/A"
else:
    median_ctx = "N/A"
col4.metric("中位上下文窗口 (tokens)", median_ctx)

# Capability breakdown
st.subheader("能力分布")
cap_col1, cap_col2, cap_col3 = st.columns(3)

vision_count = int(df[ df.get("supports_vision", "").astype(str) == "true" ].shape[0]) if "supports_vision" in df.columns else 0
audio_count = int(df[ df.get("modalities", "").str.contains("audio", case=False, na=False) ].shape[0])
tools_count = int(df[ df.get("supports_tool_use", "").astype(str) == "true" ].shape[0])

cap_col1.metric("支持视觉输入", vision_count)
cap_col2.metric("标记为音频相关", audio_count)
cap_col3.metric("支持工具调用", tools_count)

# Top providers
st.subheader("按模型数量排序的前 10 提供商")
provider_counts = df["provider_name"].fillna("(unknown)").value_counts().head(10)
st.bar_chart(provider_counts)

# How to use
st.subheader("如何使用此仪表盘")
st.markdown(
    "1. 切换到主应用页面 (app.py) 来设置业务需求、输入/输出令牌量与预算。\n"
    "2. 在侧边栏选择提供商、所需模态（文本/图像/音频）、是否需要工具调用以及最小上下文窗口。\n"
    "3. 仪表盘会列出满足技术要求并在预算内的候选模型，展示估算的每月 API 成本。\n"
)

# Quick sample table
st.subheader("示例：前 10 个模型")
show_cols = [c for c in ["model_name", "provider_name", "modalities", "context_window", "latest_input_price_per_1m", "latest_output_price_per_1m"] if c in df.columns]
st.dataframe(df[show_cols].head(10), use_container_width=True)

# Data notes
with st.expander("数据说明与使用注意事项"):
    st.write(
        "- 此数据来自历史快照（CSV）。在做采购或生产决策前，请验证最新定价。\n"
        "- 估算基于输入/输出令牌数的简单乘法，不包含缓存折扣、托管费、税费或重试等费用。\n"
        "- 模态与能力标签表示报告的功能，不代表在特定任务上的效果或质量。\n"
        "- 若要在本地运行带完整筛选功能的仪表盘，请运行：`streamlit run app.py`。"
    )

st.write("---")

st.caption("页面由脚本 homepage.py 生成 — 作为应用的落地页/简介页面。")
