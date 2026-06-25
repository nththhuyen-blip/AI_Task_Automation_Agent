import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Task Automation Agent",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-card {
    background: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/expert_rated_technological_capability.csv"
    )

expert = load_data()

# =====================================
# ENHANCED RECOMMENDATION
# =====================================

def recommend_ai(score):

    if score >= 4.5:
        return "🤖 AI 90% | Human 10%"

    elif score >= 4:
        return "🤖 AI 80% | Human 20%"

    elif score >= 3:
        return "🧑‍💻 AI 60% | Human 40%"

    else:
        return "👨 Human 70% | AI 30%"


expert["Recommendation"] = expert[
    "Automation Capacity Rating"
].apply(recommend_ai)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("⚙️ Dashboard Controls")

occupation_options = sorted(
    expert[
        "Occupation (O*NET-SOC Title)"
    ].dropna().unique()
)

selected_occupations = st.sidebar.multiselect(
    "Select Occupations",
    occupation_options,
    default=occupation_options[:3]
)

filtered_df = expert[
    expert["Occupation (O*NET-SOC Title)"]
    .isin(selected_occupations)
]

# =====================================
# HEADER
# =====================================

st.title("🤖 AI Task Automation Agent")

st.markdown("""
### Phân tích và khuyến nghị ứng dụng AI Agent dựa trên dữ liệu WorkBank

Ứng dụng hỗ trợ đánh giá khả năng tự động hóa công việc bằng AI,
so sánh giữa các nghề nghiệp và đề xuất mức độ tham gia của AI.
""")

# =====================================
# KPI SECTION
# =====================================

avg_auto = round(
    filtered_df[
        "Automation Capacity Rating"
    ].mean(),
    2
)

avg_human = round(
    filtered_df[
        "Human Agency Scale Rating"
    ].mean(),
    2
)

num_tasks = filtered_df["Task"].nunique()

num_jobs = filtered_df[
    "Occupation (O*NET-SOC Title)"
].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Automation Score",
    avg_auto
)

col2.metric(
    "Human Agency",
    avg_human
)

col3.metric(
    "Tasks",
    num_tasks
)

col4.metric(
    "Occupations",
    num_jobs
)

st.markdown("---")

# =====================================
# OCCUPATION COMPARISON
# =====================================

st.subheader("📊 Occupation Comparison")

occupation_compare = (
    filtered_df
    .groupby(
        "Occupation (O*NET-SOC Title)"
    )[
        "Automation Capacity Rating"
    ]
    .mean()
    .reset_index()
)

fig_occ = px.bar(
    occupation_compare,
    x="Occupation (O*NET-SOC Title)",
    y="Automation Capacity Rating",
    color="Automation Capacity Rating",
    title="Average Automation Capacity by Occupation"
)

st.plotly_chart(
    fig_occ,
    use_container_width=True
)

# =====================================
# TASK SELECTOR
# =====================================

st.subheader("📝 Task Evaluation")

task_options = filtered_df["Task"].unique()

selected_task = st.selectbox(
    "Select Task",
    task_options
)

task_data = filtered_df[
    filtered_df["Task"] == selected_task
].iloc[0]

automation = task_data[
    "Automation Capacity Rating"
]

human = task_data[
    "Human Agency Scale Rating"
]

recommendation = recommend_ai(
    automation
)

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Automation Capacity",
        round(automation, 2)
    )

with c2:
    st.metric(
        "Human Agency",
        round(human, 2)
    )

st.success(recommendation)

# =====================================
# DISTRIBUTION
# =====================================

st.subheader(
    "📈 Automation Capacity Distribution"
)

fig_hist = px.histogram(
    filtered_df,
    x="Automation Capacity Rating",
    nbins=25,
    marginal="box",
    title="Distribution of Automation Capacity"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================================
# CORRELATION
# =====================================

st.subheader(
    "🔍 Correlation Analysis"
)

fig_scatter = px.scatter(
    filtered_df,
    x="Automation Capacity Rating",
    y="Human Agency Scale Rating",
    hover_data=[
        "Task",
        "Occupation (O*NET-SOC Title)"
    ],
    color="Automation Capacity Rating",
    title="Automation vs Human Agency"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# =====================================
# TOP 10 TASKS
# =====================================

st.subheader(
    "🏆 Top 10 Tasks Most Suitable for AI"
)

top_tasks = filtered_df.sort_values(
    "Automation Capacity Rating",
    ascending=False
)[[
    "Occupation (O*NET-SOC Title)",
    "Task",
    "Automation Capacity Rating",
    "Recommendation"
]].head(10)

st.dataframe(
    top_tasks,
    use_container_width=True
)

# =====================================
# EXPORT CSV
# =====================================

st.subheader("📥 Export Results")

csv = top_tasks.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download CSV Report",
    csv,
    "AI_Task_Report.csv",
    "text/csv"
)

# =====================================
# INSIGHTS
# =====================================

st.subheader("💡 Key Insights")

st.info(
    f"""
    • Average Automation Capacity: {avg_auto}

    • Average Human Agency: {avg_human}

    • Selected Occupations: {num_jobs}

    • Total Tasks: {num_tasks}

    • AI is most effective for repetitive and data-intensive tasks.
    """
)

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "AI Task Automation Agent | WorkBank Dataset | Streamlit Dashboard"
)