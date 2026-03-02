import streamlit as st
import os
from dotenv import load_dotenv

from services.monday_client import MondayClient
from services.agent import BIAgent
from core.data_normalizer import simplify_items
from core.business_metrics import filter_deals, calculate_pipeline_by_sector
from core.trace import TraceLogger

# -------------------------
# SESSION MEMORY SETUP
# -------------------------
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {}

# -------------------------
# ENV SETUP
# -------------------------
load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEALS_BOARD_ID = "5026871547"
WORK_ORDERS_BOARD_ID = "5026871534"

# -------------------------
# UI
# -------------------------
st.set_page_config(page_title="Founder's BI Agent", layout="wide")

st.title("Founder's BI Agent")
st.markdown("Live Monday.com-powered Business Intelligence Agent")

user_query = st.text_input("Ask a founder-level business question:")

if user_query:

    trace = TraceLogger()

    # -------------------------
    # CLARIFICATION LOGIC
    # -------------------------
    query_lower = user_query.lower()

    needs_clarification = False

    if (
        "pipeline" in query_lower
        and not any(
            word in query_lower
            for word in [
                "sector", "mining", "powerline", "tender", "renewables",
                "railways", "aviation", "manufacturing",
                "q1", "q2", "q3", "q4", "quarter"
            ]
        )
    ):
        needs_clarification = True

    if needs_clarification:
        st.warning(
            "Do you want the overall pipeline, a specific sector, or a specific quarter?"
        )
        st.session_state.conversation_context["pending_clarification"] = True
        st.session_state.conversation_context["last_query"] = user_query
        st.stop()

    # -------------------------
    # HANDLE FOLLOW-UP CONTEXT
    # -------------------------
    if st.session_state.conversation_context.get("pending_clarification"):
        previous_query = st.session_state.conversation_context.get("last_query", "")
        user_query = previous_query + " " + user_query
        st.session_state.conversation_context["pending_clarification"] = False

    try:
        # -------------------------
        # 1️⃣ FETCH LIVE DATA
        # -------------------------
        monday_client = MondayClient(MONDAY_API_KEY)

        deals_raw = monday_client.fetch_board(DEALS_BOARD_ID)
        orders_raw = monday_client.fetch_board(WORK_ORDERS_BOARD_ID)

        trace.log(f"[API] Deals board fetched ({len(deals_raw)} records)")
        trace.log(f"[API] Work Orders board fetched ({len(orders_raw)} records)")

        # -------------------------
        # 2️⃣ CLEAN DATA
        # -------------------------
        deals = simplify_items(deals_raw)
        orders = simplify_items(orders_raw)

        # -------------------------
        # 3️⃣ FILTER PIPELINE
        # -------------------------
        filtered_deals = filter_deals(deals, user_query)
        trace.log(f"[FILTER] {len(filtered_deals)} open deals retained after time filter")

        # -------------------------
        # 4️⃣ CORE METRICS
        # -------------------------
        metrics = calculate_pipeline_by_sector(filtered_deals)

        # -------------------------
        # 5️⃣ CONVERSION ANALYSIS
        # -------------------------
        deal_companies = set(
            d.get("dropdown_mm0ybffa")
            for d in filtered_deals
            if d.get("dropdown_mm0ybffa")
        )

        order_companies = set(
            o.get("dropdown_mm0ybffa")
            for o in orders
            if o.get("dropdown_mm0ybffa")
        )

        converted_companies = deal_companies.intersection(order_companies)

        conversion_rate = (
            len(converted_companies) / len(deal_companies) * 100
            if deal_companies else 0
        )

        metrics["conversion_rate_percent"] = round(conversion_rate, 2)
        metrics["converted_company_count"] = len(converted_companies)

        trace.log("[ANALYTICS] Sector + conversion metrics calculated")

        # -------------------------
        # 6️⃣ GENERATE AI INSIGHT
        # -------------------------
        agent = BIAgent(GEMINI_API_KEY)
        insight = agent.generate_insight(user_query, metrics)

        trace.log("[LLM] Executive summary generated")

        # -------------------------
        # 7️⃣ DISPLAY OUTPUT
        # -------------------------
        st.subheader("📈 Executive Insight")
        st.write(insight)

        with st.expander("🔍 Agent Execution Trace"):
            for step in trace.get_steps():
                st.write(step)

    except Exception as e:
        st.error(f"Error: {e}")