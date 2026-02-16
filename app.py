import streamlit as st
import pandas as pd
from collections import Counter
from agent import run_agent, load_memory

st.set_page_config(page_title="MoltTrend Claw", layout="wide")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🧠 MoltTrend Claw")
page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 Trend Analytics", "📚 Historical Reports", "ℹ️ About"]
)

memory = load_memory()

# ---------------------------
# DASHBOARD PAGE
# ---------------------------
if page == "📊 Dashboard":

    st.title("🚀 Autonomous Crypto Trend Intelligence")

    if st.button("Run Agent Now"):
        report, trends = run_agent()
        st.success("Agent executed successfully!")

    if memory:
        latest = memory[-1]
        trends = latest["trends"]

        col1, col2, col3 = st.columns(3)

        col1.metric("🔥 Trends Today", len(trends))

        all_trends = [coin for entry in memory for coin in entry["trends"]]
        unique_coins = len(set(all_trends))
        col2.metric("📌 Unique Coins (All Time)", unique_coins)

        most_common = Counter(all_trends).most_common(1)
        if most_common:
            col3.metric("🏆 Most Frequent Coin", most_common[0][0])

        st.divider()

        st.subheader("🔥 Today's Trending Coins")
        st.write(trends)

        # st.subheader("📊 AI Report")
        # st.write(latest["report"])

# ---------------------------
# ANALYTICS PAGE
# ---------------------------
elif page == "📈 Trend Analytics":

    st.title("📈 Trend Analytics & Visual Insights")

    if not memory:
        st.warning("No data yet. Run the agent first.")
    else:
        all_trends = [coin for entry in memory for coin in entry["trends"]]
        trend_counts = Counter(all_trends)

        df = pd.DataFrame(trend_counts.items(), columns=["Coin", "Count"])
        df = df.sort_values(by="Count", ascending=False)

        st.subheader("📊 Trend Frequency")
        st.bar_chart(df.set_index("Coin"))

        st.subheader("🥧 Market Narrative Distribution")
        st.write("Percentage occurrence of coins in all reports")

        df["Percentage"] = (df["Count"] / df["Count"].sum()) * 100
        st.dataframe(df)

        st.line_chart(df.set_index("Coin"))

# ---------------------------
# HISTORICAL REPORTS
# ---------------------------
elif page == "📚 Historical Reports":

    st.title("📚 Agent Memory & Reports")

    if not memory:
        st.info("No reports stored yet.")
    else:
        for entry in reversed(memory):
            st.markdown(f"### 📅 {entry['date']}")
            st.write("**Trends:**", entry["trends"])
            st.write(entry["report"])
            st.divider()

# ---------------------------
# ABOUT PAGE
# ---------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About MoltTrend Claw")

    st.markdown("### 👥 Meet the Team")

    # Use 3 columns for team members
    col1, col2, col3 = st.columns(3)

    # ------------------- Team Member 1 -------------------
    with col1:
        # Replace the URL with a real avatar image if you have one
        st.image("https://avatars.githubusercontent.com/u/your-mirza-avatar.png", width=120)
        st.markdown("**Mirza Yasir Abdullah Baig**  \nTeam Lead & AI Engineer")
        st.markdown("[GitHub](https://github.com/mirzayasirabdullahbaig07) | [LinkedIn](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/)")

    # ------------------- Team Member 2 -------------------
    with col2:
        st.image("https://avatars.githubusercontent.com/u/your-sadia-avatar.png", width=120)
        st.markdown("**Sadia Usman Bodla**  \nData Scientist")
        st.markdown("[GitHub](https://github.com/sadia-usman-bodla) | [LinkedIn](https://www.linkedin.com/in/sadia-usman-bodla/)")

    # ------------------- Team Member 3 -------------------
    with col3:
        st.image("https://avatars.githubusercontent.com/u/your-tayyeba-avatar.png", width=120)
        st.markdown("**Tayyeba Saleem**  \nUI/UX Designer")
        st.markdown("[GitHub](https://github.com/tayyeba-saleem) | [LinkedIn](https://www.linkedin.com/in/tayyebasaleem01/)")

    st.markdown("---")

    # ---------------------------
    # PROJECT DESCRIPTION
    # ---------------------------
    st.markdown("""
    ### 🧠 What is MoltTrend Claw?

    MoltTrend Claw is an autonomous crypto intelligence agent that:

    - Monitors live crypto trends
    - Uses AI reasoning to detect narratives
    - Maintains persistent memory
    - Tracks trend evolution over time
    - Generates autonomous reports

    ### ⚙️ Built With

    - Python
    - Streamlit
    - Gemini AI
    - CoinGecko API
    - Persistent JSON Memory

    ### 🚀 Hackathon Vision

    This project demonstrates:
    - Autonomous reasoning
    - Long-term memory
    - Live market monitoring
    - Self-evolving trend intelligence

    Built for SURGE × OpenClaw Hackathon.
    """)
