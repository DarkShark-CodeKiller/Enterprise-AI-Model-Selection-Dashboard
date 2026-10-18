# Enterprise-AI-Model-Selection-Dashboard
An interactive dashboard on streamlit helping businesses select suitable AI models based on technical capabilities, benchmark performance, and estimated API costs.

## Step 1 — Dataset and Decision-Maker

### Dataset

**Dataset:** AI Model Pricing, Specs & Benchmarks Tracker  
**Source:** [Kaggle Dataset](https://www.kaggle.com/datasets/syedahmadrayyan/ai-model-pricing-specs-and-benchmarks-tracker)

We selected this dataset because businesses increasingly need to compare AI models before integrating them into their applications.

The dataset includes API pricing, technical specifications, and selected benchmark results from major AI providers. Our `models_full.csv` contains 82 model records and 39 columns. Each row represents one model version.

The data is compiled from publicly available model documentation and other reported sources rather than generated as a teaching dataset.

Our downloaded file contains model information and available API prices from August 13, 2026. We use this historical snapshot for the dashboard. The data is not live.

### Decision-Maker

**AI Engineering Manager at a company developing AI-powered applications.**

This manager is responsible for selecting models that satisfy business requirements while keeping API spending within budget.

Rather than choosing the most powerful or cheapest model alone, the manager needs to consider both technical capabilities and expected usage costs.

---

## Step 2 — Why Build a Dashboard?

### 1. Who uses it, and how often?

The AI Engineering Manager reviews the dashboard weekly and whenever the company considers introducing or replacing an AI model.

The dashboard is especially useful when business requirements, usage volume, or API prices change.

### 2. What decision does it support?

The dashboard helps the manager decide which AI models should be shortlisted for further testing.

**Decision rule:**

If the manager finds models that satisfy the required technical capabilities and fit within the monthly API budget, they will select suitable candidates for further evaluation before making an integration decision.

If no models meet both conditions, the manager can reconsider the budget or technical requirements.

The dashboard does not automatically select a final model. Real business testing is still necessary.

### 3. What happens without the dashboard?

Without the dashboard, the manager may need to visit multiple providers' websites, compare different technical specifications, and calculate API costs manually.

This process can be repetitive and may lead to mistakes, such as comparing only input prices while ignoring output costs.

These are potential inefficiencies rather than measured cost savings.

Our dashboard brings the relevant information into one place and allows the manager to compare different business scenarios more efficiently.

### 4. Why a dashboard instead of a report or email?

Model selection is not always a one-time decision.

The manager may need to compare models again when workloads increase, budgets change, or new AI models become available.

A static report provides only one set of comparisons. An interactive dashboard allows the manager to change business requirements and immediately see how the shortlist and estimated costs change.

A weekly email may be useful for announcing major pricing changes, but it cannot provide the same interactive comparison.

---

## Step 3 — What Matters on the Dashboard?

We performed exploratory data analysis using Pandas and Matplotlib to examine data types, missing values, price distributions, and differences across model providers.

### Headline KPIs

We selected three metrics:

**1. Technically Eligible Models**

Shows how many models meet the selected technical requirements.

This answers: *How many models could potentially support our business application?*

**2. Models Within Budget**

Shows how many technically eligible models have usable pricing information and an estimated monthly cost within the selected budget.

This answers: *How many affordable options do we have?*

**3. Lowest Estimated Monthly Cost**

Shows the lowest estimated monthly API cost among technically eligible models with available pricing data.

This provides a cost reference for comparing potential alternatives. It does not indicate which model has the best quality.

### Supporting Chart

**Estimated Monthly API Cost by Model**

The bar chart compares up to ten of the lowest-cost models that satisfy the technical requirements.

This chart helps the manager understand the cost differences between candidates rather than focusing only on the cheapest model.

The comparison uses the same assumed monthly input and output Token volumes for all models.

### Interactive Filters

We included filters for:

- AI provider
- Required modality
- Tool-calling capability
- Minimum context window
- Monthly input and output Token volumes
- Monthly API budget

These filters directly affect whether a model is suitable or affordable for the business.

### Details at the Bottom

The candidate table shows model names, providers, modalities, context windows, API prices, estimated monthly costs, and source links.

The manager can use this information to investigate shortlisted models before making a decision.

### What We Chose Not to Show

**1. A single overall benchmark ranking**

Benchmark data is missing for many models, and the reported scores may come from different evaluation settings.

Combining them into one ranking could create a misleading impression of precision.

**2. Provider headquarters and founding-year comparisons**

Although the dataset contains information about providers' backgrounds, these variables do not directly help our manager determine whether a model meets the company's technical requirements and budget.

We therefore excluded them from the main dashboard.

### Data Limitations

Several limitations could affect the interpretation of results:

- Some models have missing API prices, which prevents reliable cost estimation.
- Technical capability flags do not measure actual performance or reliability.
- Different AI models may use different numbers of tokens to complete the same task.
- Image and audio workloads may involve additional pricing rules not captured by the simplified cost calculation.
- The downloaded data is a historical snapshot, so current prices and model availability may differ.
- Lower estimated API costs do not necessarily mean lower total implementation costs.

We exclude models with unknown required prices from the cost comparison rather than treating missing prices as zero.

The dashboard is intended for initial screening, not final procurement decisions.

---

## Step 4 — Refresh Frequency

### How often should data be updated?

**Proposed refresh frequency: weekly.**

AI providers periodically release new models, change prices, and update technical specifications.

A weekly refresh would allow the company to review its options without continuously collecting data.

In a real business environment, significant pricing changes or model deprecations would also require immediate verification.

### How often should the manager review it?

**Review frequency: weekly, or when a model selection decision is needed.**

The manager does not need to inspect the dashboard every minute because changing an AI provider requires technical evaluation and implementation planning.

### What should trigger action?

We propose monitoring the estimated monthly API cost of the company's currently deployed model, holding the workload constant.

**Proposed action threshold:** If its verified estimated monthly API cost increases by more than 10% compared with the previous review, the manager should investigate alternative models.

This 10% threshold is a proposed management rule, not a statistically estimated optimal value.

The current application contains only one price snapshot, so historical change monitoring is not yet implemented.

### What does stale data cost?

Outdated data could cause a company to underestimate API spending, overlook a cheaper alternative, or shortlist a model that has become unavailable.

For example, if an input price increases by $1 per million tokens and the company uses 100 million input tokens each month, relying on the old price would underestimate monthly spending by $100.

Therefore, official provider prices must be verified before making financial or deployment decisions.

### Data Period

The current dashboard uses the downloaded Kaggle snapshot dated August 13, 2026.

**Current implementation:** Static CSV.

**Proposed production update:** Weekly.

---

## Step 5 — Build and Deployment

### Tools

- Python
- Pandas
- Streamlit
- Matplotlib (for exploratory data analysis)

### Project Files

- `app.py` — Streamlit dashboard
- `models_full.csv` — Dataset
- `eda.ipynb` — Exploratory data analysis
- `requirements.txt` — Dependencies
- `README.md` — Business justification and project documentation

### How to Run

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

The application can be deployed through Streamlit Community Cloud using the GitHub repository.

### Conclusion

This dashboard helps an AI Engineering Manager identify technically suitable AI models and estimate their potential API costs under different business requirements.

Instead of providing a general model leaderboard, it supports a specific business decision: **which models deserve further testing before a company commits to an AI solution?**

The dashboard demonstrates how publicly available AI market data can support more informed technology selection and cost management.
