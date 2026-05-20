from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent.parent

MARTS_DIR = BASE_DIR / "data" / "marts"

st.set_page_config(
    page_title="Real-Time Product Intelligence",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMetric"] {
            background-color: #111827;
            border-radius: 14px;
            padding: 18px;
            border: 1px solid #1f2937;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

revenue = pd.read_csv(
    MARTS_DIR / "mart_revenue.csv"
)

funnel = pd.read_csv(
    MARTS_DIR / "mart_funnel.csv"
)

quality = pd.read_csv(
    MARTS_DIR / "quality_check_results.csv"
)

retention = pd.read_csv(
    MARTS_DIR / "mart_retention.csv"
)

anomalies = pd.read_csv(
    MARTS_DIR / "mart_anomalies.csv"
)

# =========================================================
# DATE PARSING
# =========================================================

revenue["event_month"] = pd.to_datetime(
    revenue["event_month"]
)

retention["event_month"] = pd.to_datetime(
    retention["event_month"]
)

anomalies["event_month"] = pd.to_datetime(
    anomalies["event_month"]
)

# =========================================================
# HEADER
# =========================================================

st.title("Real-Time Product Intelligence Platform")

st.markdown(
    """
    Modern analytics engineering platform designed to simulate event-driven product intelligence, revenue analytics, funnel monitoring, retention analytics, anomaly detection, and automated data quality workflows.
    """
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

with st.sidebar:

    st.header("Filters")

    country_filter = st.multiselect(
        "Country",
        options=sorted(revenue["country"].unique()),
        default=sorted(revenue["country"].unique())
    )

    platform_filter = st.multiselect(
        "Platform",
        options=sorted(revenue["platform"].unique()),
        default=sorted(revenue["platform"].unique())
    )

# =========================================================
# FILTER DATA
# =========================================================

filtered = revenue[
    (revenue["country"].isin(country_filter)) &
    (revenue["platform"].isin(platform_filter))
]

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered["total_revenue"].sum()

total_users = filtered["active_users"].sum()

total_events = filtered["total_events"].sum()

avg_revenue_per_user = (
    total_revenue / total_users
    if total_users > 0
    else 0
)

quality_pass_rate = (
    (quality["status"] == "passed").sum()
    / len(quality)
)

# =========================================================
# TOP KPI CARDS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

kpi2.metric(
    "Active Users",
    f"{total_users:,.0f}"
)

kpi3.metric(
    "Events",
    f"{total_events:,.0f}"
)

kpi4.metric(
    "Quality Pass Rate",
    f"{quality_pass_rate:.0%}"
)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Revenue Intelligence",
    "Funnel Analytics",
    "Retention Analytics",
    "Anomaly Monitoring",
    "Data Quality"
])

# =========================================================
# TAB 1 — REVENUE INTELLIGENCE
# =========================================================

with tab1:

    st.subheader("Revenue Performance")

    revenue_by_month = (
        filtered
        .groupby("event_month", as_index=False)[
            "total_revenue"
        ]
        .sum()
    )

    fig_monthly = px.line(
        revenue_by_month,
        x="event_month",
        y="total_revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    revenue_by_country = (
        filtered
        .groupby("country", as_index=False)[
            "total_revenue"
        ]
        .sum()
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    fig_country = px.bar(
        revenue_by_country,
        x="country",
        y="total_revenue",
        title="Revenue by Country"
    )

    fig_country.update_layout(
        template="plotly_dark",
        height=380
    )

    col1.plotly_chart(
        fig_country,
        use_container_width=True
    )

    revenue_by_platform = (
        filtered
        .groupby("platform", as_index=False)[
            "total_revenue"
        ]
        .sum()
    )

    fig_platform = px.pie(
        revenue_by_platform,
        names="platform",
        values="total_revenue",
        title="Revenue by Platform"
    )

    fig_platform.update_layout(
        template="plotly_dark",
        height=380
    )

    col2.plotly_chart(
        fig_platform,
        use_container_width=True
    )

# =========================================================
# TAB 2 — FUNNEL ANALYTICS
# =========================================================

with tab2:

    st.subheader("Product Funnel Analytics")

    fig_funnel = px.bar(
        funnel,
        x="event_type",
        y="total_events",
        color="event_type",
        title="Product Funnel Event Volume"
    )

    fig_funnel.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_funnel,
        use_container_width=True
    )

    st.dataframe(
        funnel,
        use_container_width=True
    )

# =========================================================
# TAB 3 — RETENTION ANALYTICS
# =========================================================

with tab3:

    st.subheader("Retention Analytics")

    retention_filtered = retention.copy()

    retention_rate_avg = (
        retention_filtered["retention_rate"]
        .mean()
    )

    latest_mau = (
        retention_filtered
        .sort_values("event_month")
        ["monthly_active_users"]
        .iloc[-1]
    )

    latest_returning = (
        retention_filtered
        .sort_values("event_month")
        ["returning_users"]
        .iloc[-1]
    )

    rkpi1, rkpi2, rkpi3 = st.columns(3)

    rkpi1.metric(
        "Avg Retention Rate",
        f"{retention_rate_avg:.1%}"
    )

    rkpi2.metric(
        "Latest Monthly Active Users",
        f"{latest_mau:,.0f}"
    )

    rkpi3.metric(
        "Latest Returning Users",
        f"{latest_returning:,.0f}"
    )

    fig_retention = px.line(
        retention_filtered,
        x="event_month",
        y="retention_rate",
        markers=True,
        title="Monthly Retention Rate"
    )

    fig_retention.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig_retention,
        use_container_width=True
    )

    colr1, colr2 = st.columns(2)

    fig_mau = px.bar(
        retention_filtered,
        x="event_month",
        y="monthly_active_users",
        title="Monthly Active Users"
    )

    fig_mau.update_layout(
        template="plotly_dark",
        height=380
    )

    colr1.plotly_chart(
        fig_mau,
        use_container_width=True
    )

    fig_returning = px.bar(
        retention_filtered,
        x="event_month",
        y="returning_users",
        title="Returning Users"
    )

    fig_returning.update_layout(
        template="plotly_dark",
        height=380
    )

    colr2.plotly_chart(
        fig_returning,
        use_container_width=True
    )

    st.dataframe(
        retention_filtered,
        use_container_width=True
    )

# =========================================================
# TAB 4 — ANOMALY MONITORING
# =========================================================

with tab4:

    st.subheader("Revenue Anomaly Monitoring")

    anomaly_count = len(
        anomalies[
            anomalies["anomaly_status"] == "anomaly"
        ]
    )

    avg_revenue = anomalies["avg_revenue"].mean()

    max_deviation = anomalies["deviation"].max()

    akpi1, akpi2, akpi3 = st.columns(3)

    akpi1.metric(
        "Detected Anomalies",
        anomaly_count
    )

    akpi2.metric(
        "Average Revenue",
        f"${avg_revenue:,.0f}"
    )

    akpi3.metric(
        "Max Revenue Deviation",
        f"${max_deviation:,.0f}"
    )

    fig_anomalies = px.line(
        anomalies,
        x="event_month",
        y="total_revenue",
        color="anomaly_status",
        markers=True,
        title="Revenue Anomaly Detection"
    )

    fig_anomalies.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig_anomalies,
        use_container_width=True
    )

    st.dataframe(
        anomalies,
        use_container_width=True
    )

# =========================================================
# TAB 5 — DATA QUALITY
# =========================================================

with tab5:

    st.subheader("Data Quality Monitoring")

    failed_checks = quality[
        quality["status"] != "passed"
    ]

    colq1, colq2, colq3 = st.columns(3)

    colq1.metric(
        "Total Checks",
        len(quality)
    )

    colq2.metric(
        "Passed Checks",
        (quality["status"] == "passed").sum()
    )

    colq3.metric(
        "Failed Checks",
        len(failed_checks)
    )

    fig_quality = px.bar(
        quality,
        x="check_name",
        y="failed_records",
        color="status",
        title="Data Quality Validation Results"
    )

    fig_quality.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig_quality,
        use_container_width=True
    )

    st.dataframe(
        quality,
        use_container_width=True
    )