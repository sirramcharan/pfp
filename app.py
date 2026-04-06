# =============================================================================
# PERSONAL FINANCE DASHBOARD — Production-Ready Portfolio Piece
# =============================================================================
# Tech Stack: Streamlit · Pandas · Plotly · (gspread for Google Sheets)
# Theme    : Glassmorphism — dark gradient backdrop, frosted-glass containers
# Author   : Generated for interview-ready portfolio showcase
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="FinSight Pro | Personal Finance",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 1. GLASSMORPHISM CSS INJECTION
#    Why: Streamlit's default theme is generic. Custom CSS lets us create a
#    premium, memorable look that stands out in a portfolio review. Frosted-glass
#    aesthetics are achieved with rgba backgrounds + backdrop-filter blur.
# =============================================================================
def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary:   #0a0e1a;
        --bg-secondary: #0f1629;
        --glass-bg:     rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.12);
        --glass-hover:  rgba(255, 255, 255, 0.09);
        --accent-cyan:  #00d4ff;
        --accent-violet:#a855f7;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --accent-rose:  #f43f5e;
        --text-primary: #f0f4ff;
        --text-muted:   rgba(200, 210, 240, 0.6);
        --shadow:       0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* ── App Background — deep navy-to-purple gradient ── */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 40%, #130f23 70%, #0d1520 100%);
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
    }

    /* ── Animated ambient orbs in background ── */
    .stApp::before {
        content: '';
        position: fixed;
        top: -20%;
        left: -10%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: float 8s ease-in-out infinite;
    }
    .stApp::after {
        content: '';
        position: fixed;
        bottom: -20%;
        right: -10%;
        width: 700px;
        height: 700px;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.06) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: float 10s ease-in-out infinite reverse;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1); }
        50%       { transform: translateY(-30px) scale(1.05); }
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Sidebar Glassmorphism ── */
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 26, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* ── Glass Card base class ── */
    .glass-card {
        background:       var(--glass-bg);
        border:           1px solid var(--glass-border);
        border-radius:    16px;
        backdrop-filter:  blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow:       var(--shadow);
        padding:          24px;
        transition:       all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    }
    .glass-card:hover {
        background:    var(--glass-hover);
        border-color:  rgba(255, 255, 255, 0.2);
        transform:     translateY(-2px);
        box-shadow:    0 12px 40px rgba(0, 0, 0, 0.5);
    }

    /* ── KPI Metric Cards ── */
    .metric-card {
        background:      var(--glass-bg);
        border:          1px solid var(--glass-border);
        border-radius:   16px;
        backdrop-filter: blur(12px);
        padding:         24px 28px;
        text-align:      left;
        position:        relative;
        overflow:        hidden;
        transition:      all 0.3s ease;
        min-height:      130px;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 120px; height: 120px;
        border-radius: 50%;
        opacity: 0.08;
    }
    .metric-card.cyan::after   { background: var(--accent-cyan);   box-shadow: 0 0 60px var(--accent-cyan);   }
    .metric-card.violet::after { background: var(--accent-violet); box-shadow: 0 0 60px var(--accent-violet); }
    .metric-card.green::after  { background: var(--accent-green);  box-shadow: 0 0 60px var(--accent-green);  }
    .metric-card.amber::after  { background: var(--accent-amber);  box-shadow: 0 0 60px var(--accent-amber);  }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 10px;
    }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    .delta-pos { background: rgba(16,185,129,0.15); color: var(--accent-green); }
    .delta-neg { background: rgba(244, 63, 94,0.15); color: var(--accent-rose);  }

    /* ── Page Title ── */
    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        background: linear-gradient(90deg, #f0f4ff 30%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
        margin-bottom: 4px;
    }
    .page-subtitle {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 28px;
    }

    /* ── Section Headers ── */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.3px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::before {
        content: '';
        width: 3px;
        height: 18px;
        border-radius: 2px;
        background: linear-gradient(180deg, var(--accent-cyan), var(--accent-violet));
        display: inline-block;
    }

    /* ── Anomaly Table ── */
    .anomaly-row {
        background: rgba(244, 63, 94, 0.08);
        border-left: 3px solid var(--accent-rose);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.88rem;
    }

    /* ── Goal Progress ── */
    .goal-item {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .goal-title { font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; }
    .goal-meta  { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 10px; }

    /* ── Tax Tracker ── */
    .tax-bar-wrap {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        height: 12px;
        overflow: hidden;
        margin: 8px 0;
    }
    .tax-bar-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet));
        transition: width 0.8s ease;
    }

    /* ── Nav pills ── */
    .nav-pill {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.25);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--accent-cyan);
        letter-spacing: 0.5px;
        margin-bottom: 24px;
    }

    /* ── Streamlit widget overrides ── */
    .stSlider > div > div > div { background: var(--accent-cyan) !important; }
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--glass-bg) !important;
        border-color: var(--glass-border) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,255,255,0.12) !important;
    }

    /* ── Plotly chart containers ── */
    .js-plotly-plot .plotly .svg-container { border-radius: 12px; }

    /* ── Progress bar custom ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet)) !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div > div {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--glass-border) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar       { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# 2. DUMMY DATA GENERATOR
#    Why: We build realistic, structured fake data so every calculation and
#    chart works end-to-end. Swap `load_dummy_data()` with the Google Sheets
#    loader below when your sheet is ready (see `load_gsheets_data()`).
# =============================================================================
@st.cache_data(ttl=300)   # Cache for 5 min — avoids re-reading on every rerun
def load_dummy_data(user_profile: str = "Arjun Sharma") -> dict:
    """
    Returns a dict of DataFrames mimicking a full financial data warehouse:
      - transactions : monthly ledger (income + categorised expenses)
      - investments  : portfolio holdings with current values
      - goals        : savings goal targets vs current progress
      - tax          : 80C investments breakdown

    The 'user_profile' param simulates pulling different Google Sheet tabs
    for different users in a shared dashboard scenario.
    """
    np.random.seed({"Arjun Sharma": 42, "Priya Nair": 7, "Rohit Verma": 99}.get(user_profile, 42))

    # ── Base salaries differ per profile ─────────────────────────────────────
    base_salary = {"Arjun Sharma": 120000, "Priya Nair": 95000, "Rohit Verma": 145000}.get(user_profile, 120000)

    # ── Transaction ledger — 18 months of history ────────────────────────────
    months = 18
    dates, categories, amounts, txn_types = [], [], [], []

    category_config = {
        # Category             : (mean_monthly, std_dev, type)
        "Salary":              (base_salary,       3000,  "Income"),
        "Freelance":           (base_salary*0.10,  8000,  "Income"),
        "Rent":                (base_salary*0.25,  500,   "Expense"),
        "Groceries":           (base_salary*0.07,  2000,  "Expense"),
        "Dining & Takeout":    (base_salary*0.06,  1500,  "Expense"),
        "Transport":           (base_salary*0.04,  800,   "Expense"),
        "Utilities":           (base_salary*0.02,  400,   "Expense"),
        "Entertainment":       (base_salary*0.03,  1200,  "Expense"),
        "Healthcare":          (base_salary*0.02,  3000,  "Expense"),
        "Shopping":            (base_salary*0.05,  4000,  "Expense"),
        "Subscriptions":       (1200,              100,   "Expense"),
        "Mutual Funds (SIP)":  (base_salary*0.12,  0,     "Savings"),
        "PPF":                 (12500,             0,     "Savings"),
        "Emergency Fund":      (base_salary*0.05,  2000,  "Savings"),
    }

    today = datetime.today()
    for m in range(months, 0, -1):
        month_date = today - timedelta(days=m * 30)
        for cat, (mean, std, txn_type) in category_config.items():
            val = max(500, np.random.normal(mean, std))
            # Inject occasional spending spikes for anomaly detection demo
            if cat in ["Shopping", "Dining & Takeout", "Entertainment"] and np.random.rand() < 0.15:
                val *= np.random.uniform(1.5, 2.5)   # 50–150% spike
            dates.append(month_date.replace(day=1))
            categories.append(cat)
            amounts.append(round(val, 2))
            txn_types.append(txn_type)

    transactions = pd.DataFrame({
        "date":     dates,
        "category": categories,
        "amount":   amounts,
        "type":     txn_types,
    })

    # ── Investment portfolio ──────────────────────────────────────────────────
    investments = pd.DataFrame({
        "asset_class":  ["Large Cap Equity", "Mid Cap Equity", "Small Cap Equity",
                         "Debt / Bonds", "Gold ETF", "Cash & FD"],
        "category":     ["Equity", "Equity", "Equity", "Debt", "Gold", "Cash"],
        "current_value":[320000, 180000, 95000, 150000, 75000, 60000],
        "invested_amt": [280000, 150000, 70000, 145000, 65000, 60000],
    })
    investments["pnl"] = investments["current_value"] - investments["invested_amt"]
    investments["pnl_pct"] = (investments["pnl"] / investments["invested_amt"] * 100).round(2)

    # ── Savings goals ─────────────────────────────────────────────────────────
    goals = pd.DataFrame({
        "goal":      ["Emergency Fund (6 mo)", "New Car 🚗", "Europe Trip ✈️",
                      "Home Down Payment 🏠", "Retirement Corpus"],
        "target":    [360000, 900000, 250000, 3000000, 15000000],
        "current":   [270000, 320000, 118000,  420000,   950000],
        "deadline":  ["Dec 2025", "Mar 2026", "Aug 2025", "Jan 2030", "Dec 2045"],
        "color":     ["cyan", "violet", "green", "amber", "rose"],
    })

    # ── 80C Tax-saving investments ────────────────────────────────────────────
    tax_80c = pd.DataFrame({
        "instrument":  ["PPF", "ELSS Mutual Fund", "LIC Premium", "NPS (Employee)"],
        "invested":    [150000, 60000, 28000, 20000],
        "limit":       [150000, 150000, 150000, 50000],
    })

    return {
        "transactions": transactions,
        "investments":  investments,
        "goals":        goals,
        "tax_80c":      tax_80c,
        "user":         user_profile,
        "base_salary":  base_salary,
    }


# =============================================================================
# 2b. GOOGLE SHEETS LOADER (commented — swap in when sheet is ready)
# =============================================================================
# def load_gsheets_data(user_profile: str) -> dict:
#     """
#     Connects to Google Sheets using a service account stored in st.secrets.
#     In .streamlit/secrets.toml:
#       [gcp_service_account]
#       type = "service_account"
#       project_id = "..."
#       private_key_id = "..."
#       private_key = "..."
#       client_email = "..."
#       ...
#     """
#     import gspread
#     from google.oauth2.service_account import Credentials
#     scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds  = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
#     client = gspread.authorize(creds)
#     sheet  = client.open("PersonalFinance").worksheet(user_profile)
#     df     = pd.DataFrame(sheet.get_all_records())
#     # … transform df into the same dict structure as load_dummy_data()
#     return df


# =============================================================================
# 3. DERIVED METRICS CALCULATOR
#    Why: Single source of truth for all KPIs — avoids recalculating the same
#    numbers across pages, which could cause discrepancies in an interview demo.
# =============================================================================
def compute_kpis(data: dict) -> dict:
    txn = data["transactions"]
    inv = data["investments"]

    # Current month context
    latest_month = txn["date"].max()

    def month_total(txn_type, month):
        return txn[(txn["type"] == txn_type) & (txn["date"] == month)]["amount"].sum()

    income   = month_total("Income",   latest_month)
    expenses = month_total("Expense",  latest_month)
    savings  = month_total("Savings",  latest_month)

    # Net Worth = total portfolio value + cash savings goal
    net_worth = inv["current_value"].sum() + data["goals"]["current"].sum()

    # Savings rate = savings / gross income (industry standard definition)
    savings_rate = (savings / income * 100) if income > 0 else 0

    # Runway = liquid assets / monthly burn rate
    liquid    = inv[inv["category"] == "Cash"]["current_value"].sum()
    burn_rate = expenses  # monthly non-savings outflow
    runway    = (liquid / burn_rate) if burn_rate > 0 else 0

    # Monthly savings trend (last 6 months) — used for sparklines/trend text
    last_6 = txn[txn["type"] == "Savings"].groupby("date")["amount"].sum().tail(6)

    return {
        "net_worth":    net_worth,
        "savings_rate": savings_rate,
        "runway":       runway,
        "income":       income,
        "expenses":     expenses,
        "savings":      savings,
        "savings_trend":last_6,
        "latest_month": latest_month,
    }


# =============================================================================
# 4. CHART HELPERS — all return Plotly figures with a consistent dark theme
# =============================================================================
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font         =dict(family="DM Sans", color="#c8d2f0"),
    margin       =dict(l=10, r=10, t=40, b=10),
    legend       =dict(
        bgcolor     ="rgba(255,255,255,0.05)",
        bordercolor ="rgba(255,255,255,0.1)",
        borderwidth =1,
    ),
)

def fig_sankey(data: dict) -> go.Figure:
    """
    Sankey diagram: visualises money flow from income sources → buckets → categories.
    Why Sankey? It makes the concept of 'where does my money go' immediately
    intuitive — far more powerful in an interview than a plain pie chart.
    """
    txn = data["transactions"]
    latest = txn["date"].max()
    month_txn = txn[txn["date"] == latest]

    salary     = month_txn[month_txn["category"] == "Salary"]["amount"].sum()
    freelance  = month_txn[month_txn["category"] == "Freelance"]["amount"].sum()

    # Needs (essentials)
    needs_cats  = ["Rent", "Groceries", "Utilities", "Healthcare", "Transport"]
    needs_total = month_txn[month_txn["category"].isin(needs_cats)]["amount"].sum()
    needs_vals  = {c: month_txn[month_txn["category"] == c]["amount"].sum() for c in needs_cats}

    # Wants (discretionary)
    wants_cats  = ["Dining & Takeout", "Entertainment", "Shopping", "Subscriptions"]
    wants_total = month_txn[month_txn["category"].isin(wants_cats)]["amount"].sum()
    wants_vals  = {c: month_txn[month_txn["category"] == c]["amount"].sum() for c in wants_cats}

    # Savings
    savings_cats = ["Mutual Funds (SIP)", "PPF", "Emergency Fund"]
    sav_total    = month_txn[month_txn["category"].isin(savings_cats)]["amount"].sum()
    sav_vals     = {c: month_txn[month_txn["category"] == c]["amount"].sum() for c in savings_cats}

    # Node labels
    labels = (
        ["Salary", "Freelance",                   # 0, 1  — income sources
         "Needs", "Wants", "Savings",             # 2, 3, 4 — buckets
         ] + needs_cats + wants_cats + savings_cats  # 5+ — leaf categories
    )
    idx = {l: i for i, l in enumerate(labels)}

    # Build source → target → value triples
    sources, targets, values, colors = [], [], [], []

    def add_flow(src, tgt, val, color):
        sources.append(idx[src]); targets.append(idx[tgt])
        values.append(max(val, 1)); colors.append(color)

    # Income → buckets (split proportionally)
    total_income = salary + freelance
    for bucket, total, col in [("Needs", needs_total, "rgba(0,212,255,0.4)"),
                                ("Wants", wants_total, "rgba(168,85,247,0.4)"),
                                ("Savings", sav_total, "rgba(16,185,129,0.4)")]:
        if total_income > 0:
            add_flow("Salary",    bucket, salary    * (total / total_income), col)
            add_flow("Freelance", bucket, freelance * (total / total_income), col)

    # Buckets → leaf categories
    for cat, val in needs_vals.items():
        if val > 0: add_flow("Needs",   cat, val, "rgba(0,212,255,0.25)")
    for cat, val in wants_vals.items():
        if val > 0: add_flow("Wants",   cat, val, "rgba(168,85,247,0.25)")
    for cat, val in sav_vals.items():
        if val > 0: add_flow("Savings", cat, val, "rgba(16,185,129,0.25)")

    node_colors = (
        ["rgba(0,212,255,0.7)",  "rgba(0,212,255,0.5)"]  +   # income
        ["rgba(0,212,255,0.6)",  "rgba(168,85,247,0.6)", "rgba(16,185,129,0.6)"] +  # buckets
        ["rgba(0,212,255,0.35)"] * len(needs_cats) +
        ["rgba(168,85,247,0.35)"]* len(wants_cats) +
        ["rgba(16,185,129,0.35)"]* len(savings_cats)
    )

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20, thickness=18, line=dict(color="rgba(255,255,255,0.1)", width=0.5),
            label=labels, color=node_colors,
        ),
        link=dict(source=sources, target=targets, value=values,
                  color=colors, hovertemplate="%{source.label} → %{target.label}<br>₹%{value:,.0f}<extra></extra>"),
    ))
    fig.update_layout(title_text="Monthly Cash Flow", title_x=0.02,
                      title_font=dict(size=14, color="#f0f4ff"), **CHART_LAYOUT)
    return fig


def fig_networth_forecast(current_nw: float, monthly_savings: float,
                           years: int = 5, annual_return_pct: float = 12.0) -> go.Figure:
    """
    Compound-growth forecast for net worth.
    Formula: FV = PV*(1+r)^n + PMT * [((1+r)^n - 1)/r]
    We also render a ±2% confidence band to show sensitivity — this
    demonstrates quantitative thinking to interviewers.
    """
    monthly_r = (annual_return_pct / 100) / 12
    months    = years * 12
    dates     = [datetime.today() + timedelta(days=30 * i) for i in range(months + 1)]

    def project(pv, r):
        vals = [pv]
        for _ in range(months):
            vals.append(vals[-1] * (1 + r) + monthly_savings)
        return vals

    central   = project(current_nw, monthly_r)
    optimistic= project(current_nw, ((annual_return_pct + 2) / 100) / 12)
    pessimistic=project(current_nw, ((annual_return_pct - 2) / 100) / 12)

    fig = go.Figure()

    # Confidence band
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=optimistic + pessimistic[::-1],
        fill="toself",
        fillcolor="rgba(168,85,247,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        name="±2% band",
    ))
    # Central projection
    fig.add_trace(go.Scatter(
        x=dates, y=central,
        mode="lines",
        line=dict(color="#a855f7", width=3),
        name=f"{annual_return_pct}% return",
        hovertemplate="<b>%{x|%b %Y}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    # Today marker
    fig.add_vline(x=datetime.today(), line_dash="dot",
                  line_color="rgba(255,255,255,0.25)", annotation_text="Today",
                  annotation_font_color="#c8d2f0")

    fig.update_layout(
        title_text=f"Net Worth Projection ({years}Y @ {annual_return_pct}% p.a.)",
        title_font=dict(size=14, color="#f0f4ff"),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   zeroline=False, tickformat=",.0f", tickprefix="₹"),
        hovermode="x unified",
        **CHART_LAYOUT,
    )
    return fig


def fig_asset_donut(investments: pd.DataFrame) -> go.Figure:
    """
    Donut chart of asset allocation by category.
    The hole text shows total portfolio — a common design pattern for
    at-a-glance portfolio value.
    """
    alloc = investments.groupby("category")["current_value"].sum().reset_index()
    total = alloc["current_value"].sum()
    colors= ["#00d4ff", "#a855f7", "#f59e0b", "#10b981", "#f43f5e"]

    fig = go.Figure(go.Pie(
        labels=alloc["category"],
        values=alloc["current_value"],
        hole=0.62,
        marker=dict(colors=colors[:len(alloc)],
                    line=dict(color="rgba(10,14,26,1)", width=3)),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        textinfo="none",
    ))
    fig.add_annotation(
        text=f"₹{total/100000:.1f}L<br><span style='font-size:11px;'>Total</span>",
        x=0.5, y=0.5, showarrow=False, align="center",
        font=dict(size=20, color="#f0f4ff", family="Space Grotesk"),
    )
    fig.update_layout(
        title_text="Asset Allocation",
        title_font=dict(size=14, color="#f0f4ff"),
        showlegend=True, **CHART_LAYOUT,
    )
    return fig


def fig_monthly_trend(transactions: pd.DataFrame) -> go.Figure:
    """
    Stacked bar: income vs expense vs savings over time.
    Grouped monthly view makes overspending months immediately visible.
    """
    monthly = transactions.groupby(["date", "type"])["amount"].sum().reset_index()
    color_map = {"Income": "#00d4ff", "Expense": "#f43f5e", "Savings": "#10b981"}

    fig = px.bar(monthly, x="date", y="amount", color="type",
                 barmode="group", color_discrete_map=color_map,
                 labels={"amount": "₹ Amount", "date": "Month", "type": ""},
                 title="Monthly Income vs Expenses vs Savings")
    fig.update_traces(hovertemplate="₹%{y:,.0f}<extra></extra>")
    fig.update_layout(
        xaxis=dict(showgrid=False, tickformat="%b %y"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   tickformat=",.0f", tickprefix="₹"),
        **CHART_LAYOUT,
    )
    return fig


def detect_anomalies(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Anomaly detection using rolling 3-month average baseline.
    Algorithm:
      1. Compute rolling 3-month mean per expense category.
      2. Flag any month where spend > 120% of that rolling mean.
    Why: This mimics a simple statistical process control (SPC) rule —
    common in quantitative finance for detecting regime changes.
    """
    expenses = transactions[transactions["type"] == "Expense"].copy()
    expenses = expenses.sort_values("date")

    # Rolling mean per category (shift(1) to avoid look-ahead bias)
    expenses["rolling_avg"] = expenses.groupby("category")["amount"].transform(
        lambda x: x.shift(1).rolling(3, min_periods=1).mean()
    )
    expenses["pct_vs_avg"] = (expenses["amount"] / expenses["rolling_avg"] - 1) * 100

    # Flag if >20% above baseline
    anomalies = expenses[expenses["pct_vs_avg"] > 20].copy()
    anomalies = anomalies.sort_values("pct_vs_avg", ascending=False)
    anomalies["date_str"] = anomalies["date"].dt.strftime("%b %Y")
    return anomalies[["date_str", "category", "amount", "rolling_avg", "pct_vs_avg"]].head(10)


# =============================================================================
# 5. PAGE RENDERERS
# =============================================================================

def render_dashboard(data: dict, kpis: dict):
    st.markdown('<div class="page-title">Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Your financial command centre — monthly snapshot</div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-pill">📊 OVERVIEW</span>', unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    nw_lakh     = kpis["net_worth"] / 100000
    sr          = kpis["savings_rate"]
    runway      = kpis["runway"]
    monthly_sav = kpis["savings"]

    c1.markdown(f"""
    <div class="metric-card cyan">
        <div class="metric-label">Total Net Worth</div>
        <div class="metric-value">₹{nw_lakh:.1f}L</div>
        <span class="metric-delta delta-pos">↑ 3.2% this month</span>
    </div>""", unsafe_allow_html=True)

    delta_class = "delta-pos" if sr >= 20 else "delta-neg"
    delta_label = "✓ Healthy" if sr >= 20 else "⚠ Below 20% target"
    c2.markdown(f"""
    <div class="metric-card violet">
        <div class="metric-label">Monthly Savings Rate</div>
        <div class="metric-value">{sr:.1f}%</div>
        <span class="metric-delta {delta_class}">{delta_label}</span>
    </div>""", unsafe_allow_html=True)

    r_class = "delta-pos" if runway >= 6 else "delta-neg"
    c3.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Cash Runway</div>
        <div class="metric-value">{runway:.1f} mo</div>
        <span class="metric-delta {r_class}">{'✓ 6-month goal met' if runway >= 6 else '⚠ Below 6-month goal'}</span>
    </div>""", unsafe_allow_html=True)

    c4.markdown(f"""
    <div class="metric-card amber">
        <div class="metric-label">Monthly Savings (₹)</div>
        <div class="metric-value">₹{monthly_sav/1000:.1f}K</div>
        <span class="metric-delta delta-pos">↑ SIP + PPF</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sankey + Monthly Trend ─────────────────────────────────────────────
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown('<div class="section-header">Cash Flow Sankey</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_sankey(data), use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Monthly Trend</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_trend(data["transactions"]), use_container_width=True)


def render_analytics(data: dict, kpis: dict):
    st.markdown('<div class="page-title">Analytics & Forecasting</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">5-year wealth projection · Anomaly detection engine</div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-pill">📈 ANALYTICS</span>', unsafe_allow_html=True)

    # ── Forecast controls ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Net Worth Forecast</div>', unsafe_allow_html=True)

    col_ctrl1, col_ctrl2, _ = st.columns([1, 1, 2])
    with col_ctrl1:
        proj_return = st.slider("Projected Annual Return (%)", 6.0, 20.0, 12.0, 0.5,
                                help="Drag to adjust CAGR assumption and see the impact instantly")
    with col_ctrl2:
        proj_years  = st.slider("Forecast Horizon (years)", 1, 10, 5, 1)

    st.plotly_chart(
        fig_networth_forecast(kpis["net_worth"], kpis["savings"], proj_years, proj_return),
        use_container_width=True,
    )

    # ── Projection callout ────────────────────────────────────────────────────
    monthly_r  = (proj_return / 100) / 12
    fv_months  = proj_years * 12
    final_nw   = kpis["net_worth"] * ((1 + monthly_r) ** fv_months)
    for _ in range(fv_months):
        final_nw += kpis["savings"] * ((1 + monthly_r) ** _)

    col_x, col_y, col_z = st.columns(3)
    col_x.markdown(f"""<div class="metric-card cyan" style="min-height:90px">
        <div class="metric-label">Projected Net Worth ({proj_years}Y)</div>
        <div class="metric-value" style="font-size:1.5rem">₹{final_nw/100000:.1f}L</div>
    </div>""", unsafe_allow_html=True)

    growth_x = final_nw / kpis["net_worth"]
    col_y.markdown(f"""<div class="metric-card violet" style="min-height:90px">
        <div class="metric-label">Wealth Multiplier</div>
        <div class="metric-value" style="font-size:1.5rem">{growth_x:.2f}×</div>
    </div>""", unsafe_allow_html=True)

    col_z.markdown(f"""<div class="metric-card green" style="min-height:90px">
        <div class="metric-label">Compound Return Assumption</div>
        <div class="metric-value" style="font-size:1.5rem">{proj_return:.1f}% p.a.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Anomaly Detection ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Spending Anomaly Detector</div>', unsafe_allow_html=True)
    st.caption("Flags months where spending in a category is >20% above its rolling 3-month average.")

    anomalies = detect_anomalies(data["transactions"])
    if anomalies.empty:
        st.success("✅ No spending anomalies detected in recent history.")
    else:
        for _, row in anomalies.iterrows():
            pct  = row["pct_vs_avg"]
            col  = "#f43f5e" if pct > 50 else "#f59e0b"
            st.markdown(f"""
            <div class="anomaly-row">
                <div>
                    <strong style="color:#f0f4ff">{row['category']}</strong>
                    <span style="color:var(--text-muted); margin-left:10px;font-size:0.8rem">{row['date_str']}</span>
                </div>
                <div style="display:flex;gap:16px;align-items:center">
                    <span>₹{row['amount']:,.0f}</span>
                    <span style="color:var(--text-muted);font-size:0.8rem">avg ₹{row['rolling_avg']:,.0f}</span>
                    <span style="color:{col};font-weight:700">+{pct:.0f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)


def render_investments(data: dict):
    st.markdown('<div class="page-title">Investment Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Asset allocation · Goal tracking · P&amp;L snapshot</div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-pill">💼 INVESTMENTS</span>', unsafe_allow_html=True)

    inv = data["investments"]
    col_l, col_r = st.columns([2, 3])

    with col_l:
        st.markdown('<div class="section-header">Asset Allocation</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_asset_donut(inv), use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">Holdings Detail</div>', unsafe_allow_html=True)
        # Format for display
        display_inv = inv.copy()
        display_inv["Current Value"] = display_inv["current_value"].apply(lambda x: f"₹{x:,.0f}")
        display_inv["Invested"]      = display_inv["invested_amt"].apply(lambda x: f"₹{x:,.0f}")
        display_inv["P&L"]           = display_inv.apply(
            lambda r: f"{'▲' if r['pnl'] >= 0 else '▼'} ₹{abs(r['pnl']):,.0f} ({r['pnl_pct']:+.1f}%)", axis=1)
        display_inv = display_inv.rename(columns={"asset_class": "Fund / Asset", "category": "Class"})
        st.dataframe(
            display_inv[["Fund / Asset", "Class", "Current Value", "Invested", "P&L"]],
            use_container_width=True, hide_index=True,
        )

        # Portfolio summary
        total_invested = inv["invested_amt"].sum()
        total_current  = inv["current_value"].sum()
        total_pnl      = total_current - total_invested
        total_pnl_pct  = total_pnl / total_invested * 100

        st.markdown(f"""
        <div class="metric-card green" style="margin-top:16px;min-height:80px">
            <div class="metric-label">Portfolio P&L</div>
            <div style="display:flex;gap:24px;align-items:center">
                <div class="metric-value" style="font-size:1.4rem">₹{total_pnl/1000:.1f}K</div>
                <span class="metric-delta delta-pos">{total_pnl_pct:+.2f}% total return</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Goal Progress ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Savings Goal Progress</div>', unsafe_allow_html=True)
    goals = data["goals"]
    cols  = st.columns(2)

    accent_map = {"cyan": "#00d4ff", "violet": "#a855f7", "green": "#10b981",
                  "amber": "#f59e0b", "rose": "#f43f5e"}

    for i, (_, g) in enumerate(goals.iterrows()):
        pct    = min(g["current"] / g["target"], 1.0)
        color  = accent_map.get(g["color"], "#00d4ff")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="goal-item">
                <div class="goal-title">{g['goal']}</div>
                <div class="goal-meta">
                    ₹{g['current']:,.0f} of ₹{g['target']:,.0f} &nbsp;·&nbsp; Target: {g['deadline']}
                </div>
                <div class="tax-bar-wrap">
                    <div class="tax-bar-fill" style="width:{pct*100:.1f}%;background:linear-gradient(90deg,{color}88,{color});"></div>
                </div>
                <div style="font-size:0.8rem;color:var(--text-muted);margin-top:6px">{pct*100:.1f}% complete</div>
            </div>""", unsafe_allow_html=True)


def render_tax_strategy(data: dict, kpis: dict):
    st.markdown('<div class="page-title">Tax & Strategy</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Section 80C tracker · Tax-saving optimiser (Indian context)</div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-pill">🧾 TAX STRATEGY</span>', unsafe_allow_html=True)

    tax = data["tax_80c"]
    LIMIT_80C = 150000  # ₹1.5 Lakh — statutory limit under Indian Income Tax Act

    total_invested_80c = tax["invested"].sum()
    # Note: actual 80C deduction is capped at ₹1.5L regardless of total invested
    deduction_used     = min(total_invested_80c, LIMIT_80C)
    remaining          = max(LIMIT_80C - deduction_used, 0)
    utilisation_pct    = deduction_used / LIMIT_80C

    # ── 80C Summary KPIs ─────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card cyan" style="min-height:110px">
        <div class="metric-label">80C Invested</div>
        <div class="metric-value">₹{deduction_used/1000:.0f}K</div>
        <span class="metric-delta {'delta-pos' if utilisation_pct >= 1 else 'delta-neg'}">
            {'✅ Limit maxed!' if utilisation_pct >= 1 else f'₹{remaining/1000:.0f}K remaining'}
        </span>
    </div>""", unsafe_allow_html=True)

    c2.markdown(f"""<div class="metric-card violet" style="min-height:110px">
        <div class="metric-label">80C Limit</div>
        <div class="metric-value">₹1.50L</div>
        <span class="metric-delta delta-pos">Under Section 80C, IT Act</span>
    </div>""", unsafe_allow_html=True)

    # Tax saved estimate — assuming 30% slab (highest)
    tax_saved = deduction_used * 0.30
    c3.markdown(f"""<div class="metric-card green" style="min-height:110px">
        <div class="metric-label">Est. Tax Saved (30% slab)</div>
        <div class="metric-value">₹{tax_saved/1000:.1f}K</div>
        <span class="metric-delta delta-pos">Old tax regime</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 80C Progress bar ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Section 80C Utilisation</div>', unsafe_allow_html=True)
    pct_display = min(utilisation_pct, 1.0)
    st.markdown(f"""
    <div class="glass-card" style="padding:20px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="color:var(--text-muted);font-size:0.85rem">₹0</span>
            <span style="font-weight:600;color:#f0f4ff">₹{deduction_used:,.0f} invested</span>
            <span style="color:var(--text-muted);font-size:0.85rem">₹1,50,000 limit</span>
        </div>
        <div class="tax-bar-wrap" style="height:16px">
            <div class="tax-bar-fill" style="width:{pct_display*100:.1f}%"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:8px">
            <span style="color:#10b981;font-size:0.85rem">Used: {pct_display*100:.1f}%</span>
            <span style="color:#f59e0b;font-size:0.85rem">Remaining: ₹{remaining:,.0f}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Instrument Breakdown ──────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 3])
    with col_a:
        st.markdown('<div class="section-header">Instruments Used</div>', unsafe_allow_html=True)
        fig_tax = px.bar(
            tax, x="invested", y="instrument", orientation="h",
            color="invested", color_continuous_scale=["#a855f7", "#00d4ff"],
            labels={"invested": "Amount (₹)", "instrument": ""},
            title="80C Investments by Instrument",
        )
        fig_tax.add_vline(x=LIMIT_80C, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                          annotation_text="₹1.5L cap", annotation_font_color="#c8d2f0")
        fig_tax.update_layout(coloraxis_showscale=False, **CHART_LAYOUT)
        fig_tax.update_traces(hovertemplate="₹%{x:,.0f}<extra></extra>")
        st.plotly_chart(fig_tax, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Strategy Recommendations</div>', unsafe_allow_html=True)

        recommendations = [
            ("💡", "Max out 80C first",
             f"You have ₹{remaining:,.0f} left. Invest in ELSS for the dual benefit of tax saving + equity growth."),
            ("🏦", "Explore 80D (Health Insurance)",
             "Claim up to ₹25,000 premium deduction (₹50K for senior citizens). Often overlooked."),
            ("📈", "NPS for extra ₹50K deduction",
             "Section 80CCD(1B) allows an additional ₹50,000 deduction over the 80C cap — a total ₹2L benefit."),
            ("🧾", "HRA Exemption",
             "If you pay rent, ensure your HRA component is structured to maximise the exemption under Section 10(13A)."),
        ]
        for icon, title, desc in recommendations:
            st.markdown(f"""
            <div class="goal-item" style="margin-bottom:10px">
                <div style="display:flex;gap:10px;align-items:flex-start">
                    <span style="font-size:1.3rem">{icon}</span>
                    <div>
                        <div class="goal-title">{title}</div>
                        <div style="font-size:0.83rem;color:var(--text-muted);margin-top:4px">{desc}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)


# =============================================================================
# 6. SIDEBAR
# =============================================================================
def render_sidebar() -> tuple[str, str]:
    with st.sidebar:
        # App branding
        st.markdown("""
        <div style="text-align:center;padding:20px 0 10px">
            <div style="font-size:2.2rem">💎</div>
            <h2 style="margin:4px 0 0">FinSight Pro</h2>
            <div style="font-size:0.75rem;color:rgba(200,210,240,0.5);letter-spacing:2px;
                        text-transform:uppercase;margin-top:2px">Personal Finance OS</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # User profile selector — simulates multiple Google Sheet tabs
        user_profile = st.selectbox(
            "👤 User Profile",
            ["Arjun Sharma", "Priya Nair", "Rohit Verma"],
            help="Each profile pulls a different Google Sheet tab (simulated here with dummy data).",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Navigation
        st.markdown("<div style='font-size:0.72rem;letter-spacing:1.5px;color:rgba(200,210,240,0.4);text-transform:uppercase;margin-bottom:10px'>Navigation</div>", unsafe_allow_html=True)
        nav = st.radio(
            "",
            ["📊  Dashboard", "📈  Analytics", "💼  Investments", "🧾  Tax Strategy"],
            label_visibility="collapsed",
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.divider()

        # Data freshness indicator
        st.markdown(f"""
        <div style="font-size:0.75rem;color:rgba(200,210,240,0.4);text-align:center">
            🟢 Data refreshed<br>{datetime.now().strftime('%d %b %Y, %H:%M')}
        </div>""", unsafe_allow_html=True)

    return user_profile, nav


# =============================================================================
# 7. MAIN APP ENTRY POINT
# =============================================================================
def main():
    inject_css()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    user_profile, nav = render_sidebar()

    # ── Data loading (cached) ─────────────────────────────────────────────────
    # Swap `load_dummy_data` with `load_gsheets_data` when Google Sheets is ready
    data = load_dummy_data(user_profile)
    kpis = compute_kpis(data)

    # ── Page routing ──────────────────────────────────────────────────────────
    if "Dashboard" in nav:
        render_dashboard(data, kpis)
    elif "Analytics" in nav:
        render_analytics(data, kpis)
    elif "Investments" in nav:
        render_investments(data)
    elif "Tax" in nav:
        render_tax_strategy(data, kpis)


if __name__ == "__main__":
    main()
