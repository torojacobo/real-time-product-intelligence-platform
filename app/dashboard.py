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

revenue = pd.read_csv(
    MARTS_DIR / "mart_revenue.csv"
)

funnel = pd.read_csv(
    MARTS_DIR / "mart_funnel.csv"
)

quality = pd.read_csv(
    MARTS_DIR / "quality_check_results.csv"
)

revenue["event_month"] = pd.to_datetime(
    revenue["event_month"]
)

st.title("Real-Time Product Intelligence Platform")

st.markdown(
    """
    Modern analytics engineering platform designed to simulate event-driven product intelligence, revenue analytics, funnel monitoring, and automated data quality workflows.
    """
)

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

filtered = revenue[
    (revenue["country"].isin(country_filter)) &
    (revenue["platform"].isin(platform_filter))
]

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

tab1, tab2, tab3 = st.tabs([
    "Revenue Intelligence",
    "Funnel Analytics",
    "Data Quality"
])

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

with tab3:

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