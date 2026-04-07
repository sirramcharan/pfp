# ============================================================
# FINSIGHT — Personal Finance Manager
# Single-user · JSON persistence · No prebuilt data
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, date, timedelta

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight | My Finance",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 1. CSS — Glassmorphism Dark Theme
# ============================================================
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --glass:   rgba(255,255,255,0.05);
        --glass-b: rgba(255,255,255,0.10);
        --glass-h: rgba(255,255,255,0.08);
        --cyan:    #00d4ff;
        --violet:  #a855f7;
        --green:   #10b981;
        --amber:   #f59e0b;
        --rose:    #f43f5e;
        --text:    #eef2ff;
        --muted:   rgba(200,210,240,0.55);
        --shadow:  0 8px 32px rgba(0,0,0,0.45);
        --r:       14px;
    }
    .stApp {
        background: linear-gradient(135deg,#080c18 0%,#0e1225 45%,#120e22 75%,#0b1220 100%);
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }
    .stApp::before {
        content:''; position:fixed; top:-15%; left:-8%;
        width:500px; height:500px; border-radius:50%;
        background:radial-gradient(circle,rgba(168,85,247,0.07) 0%,transparent 70%);
        pointer-events:none; z-index:0;
        animation:orb 9s ease-in-out infinite;
    }
    .stApp::after {
        content:''; position:fixed; bottom:-20%; right:-10%;
        width:600px; height:600px; border-radius:50%;
        background:radial-gradient(circle,rgba(0,212,255,0.05) 0%,transparent 70%);
        pointer-events:none; z-index:0;
        animation:orb 12s ease-in-out infinite reverse;
    }
    @keyframes orb {
        0%,100%{transform:translateY(0) scale(1);}
        50%{transform:translateY(-25px) scale(1.04);}
    }
    #MainMenu, footer, header { visibility:hidden; display:none; }
    .stDeployButton { display:none; }

    [data-testid="stSidebar"] {
        background: rgba(8,12,24,0.92) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-b) !important;
    }
    .card {
        background: var(--glass);
        border: 1px solid var(--glass-b);
        border-radius: var(--r);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: var(--shadow);
        padding: 22px 26px;
        position: relative;
        overflow: hidden;
        transition: all .25s ease;
        margin-bottom: 12px;
    }
    .card::before {
        content:''; position:absolute; top:0; left:0; right:0; height:1px;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.18),transparent);
    }
    .card:hover { background:var(--glass-h); transform:translateY(-2px); }
    .kpi { min-height:115px; }
    .kpi .orb { width:80px; height:80px; border-radius:50%; position:absolute;
                top:-20px; right:-20px; opacity:.09; }
    .kpi-label { font-size:.72rem; font-weight:600; letter-spacing:1.4px;
                 text-transform:uppercase; color:var(--muted); margin-bottom:8px; }
    .kpi-value { font-family:'Space Grotesk',sans-serif; font-size:1.85rem;
                 font-weight:700; line-height:1.1; margin-bottom:6px; }
    .badge { display:inline-block; font-size:.75rem; font-weight:600;
             padding:3px 10px; border-radius:20px; }
    .bg  { background:rgba(16,185,129,.15); color:var(--green); }
    .br  { background:rgba(244,63,94,.15);  color:var(--rose); }
    .ba  { background:rgba(245,158,11,.15); color:var(--amber); }
    .ptitle {
        font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700;
        background:linear-gradient(90deg,#eef2ff 30%,var(--cyan));
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        letter-spacing:-.6px; margin-bottom:2px;
    }
    .psub { color:var(--muted); font-size:.88rem; margin-bottom:24px; }
    .pill {
        display:inline-block; background:rgba(0,212,255,.08);
        border:1px solid rgba(0,212,255,.22); border-radius:20px;
        padding:3px 13px; font-size:.75rem; font-weight:600;
        color:var(--cyan); letter-spacing:.5px; margin-bottom:20px;
    }
    .sh {
        font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:600;
        color:var(--text); margin:16px 0 10px; display:flex; align-items:center; gap:8px;
    }
    .sh::before { content:''; width:3px; height:16px; border-radius:2px;
                  background:linear-gradient(180deg,var(--cyan),var(--violet));
                  display:inline-block; }
    .pbar-wrap { background:rgba(255,255,255,.06); border-radius:8px;
                 height:10px; overflow:hidden; margin:7px 0; }
    .pbar-fill  { height:100%; border-radius:8px;
                  background:linear-gradient(90deg,var(--cyan),var(--violet)); }
    .arow {
        background:rgba(244,63,94,.06); border-left:3px solid var(--rose);
        border-radius:8px; padding:10px 14px; margin-bottom:8px;
        display:flex; justify-content:space-between; align-items:center; font-size:.87rem;
    }
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stSelectbox > div > div,
    .stDateInput > div > div {
        background: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg,var(--cyan),var(--violet)) !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div > div {
        background: rgba(255,255,255,.06) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] {
        background: var(--glass); border: 1px solid var(--glass-b);
        border-radius: var(--r) !important;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; }
    ::-webkit-scrollbar { width:5px; }
    ::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.12); border-radius:3px; }
    .wizard {
        max-width:620px; margin:50px auto; background:var(--glass);
        border:1px solid var(--glass-b); border-radius:20px;
        backdrop-filter:blur(16px); padding:40px 44px;
        box-shadow: 0 24px 64px rgba(0,0,0,0.5);
    }
    .wizard-title {
        font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700;
        background:linear-gradient(90deg,#eef2ff,var(--cyan));
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        text-align:center; margin-bottom:6px;
    }
    .wizard-sub { text-align:center; color:var(--muted); font-size:.9rem; margin-bottom:30px; }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# 2. CONSTANTS
# ============================================================
EXPENSE_CATS = [
    "Rent / EMI","Groceries","Dining & Takeout","Transport",
    "Utilities","Entertainment","Healthcare","Shopping",
    "Subscriptions","Education","Insurance","Other",
]
INCOME_CATS  = ["Salary","Freelance","Business","Investment Return","Gift / Bonus","Other Income"]
SAVINGS_CATS = ["Emergency Fund","Mutual Fund / SIP","PPF / EPF","Fixed Deposit","NPS","Stock Purchase","Other Savings"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c8d2f0"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(255,255,255,0.04)",
                bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
)


# ============================================================
# 3. STATE & PERSISTENCE
# ============================================================
def default_data() -> dict:
    return {
        "profile":      {"name":"", "currency":"₹", "tax_slab":30},
        "budgets":      {},
        "transactions": [],
        "investments":  [],
        "goals":        [],
        "tax_80c":      [],
        "setup_done":   False,
    }

def init_state():
    if "data" not in st.session_state:
        st.session_state.data = default_data()
    if "page" not in st.session_state:
        st.session_state.page = "🏠  Dashboard"

def export_json() -> str:
    return json.dumps(st.session_state.data, indent=2, default=str)

def import_json(raw: str):
    st.session_state.data = json.loads(raw)

init_state()
D = st.session_state.data


# ============================================================
# 4. DATAFRAME HELPERS
# ============================================================
def txn_df() -> pd.DataFrame:
    if not D["transactions"]:
        return pd.DataFrame(columns=["date","category","type","amount","note"])
    df = pd.DataFrame(D["transactions"])
    df["date"]   = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])
    return df.sort_values("date", ascending=False).reset_index(drop=True)

def inv_df() -> pd.DataFrame:
    if not D["investments"]:
        return pd.DataFrame(columns=["name","class","invested","current","date"])
    df = pd.DataFrame(D["investments"])
    df["invested"] = pd.to_numeric(df["invested"])
    df["current"]  = pd.to_numeric(df["current"])
    return df

def goals_df() -> pd.DataFrame:
    if not D["goals"]:
        return pd.DataFrame(columns=["name","target","current","deadline","color"])
    df = pd.DataFrame(D["goals"])
    df["target"]  = pd.to_numeric(df["target"])
    df["current"] = pd.to_numeric(df["current"])
    return df

def tax_df() -> pd.DataFrame:
    if not D["tax_80c"]:
        return pd.DataFrame(columns=["instrument","invested"])
    df = pd.DataFrame(D["tax_80c"])
    df["invested"] = pd.to_numeric(df["invested"])
    return df


# ============================================================
# 5. KPI CALCULATOR
# ============================================================
def compute_kpis(df: pd.DataFrame) -> dict:
    empty = {"income":0,"expenses":0,"savings":0,"savings_rate":0,
             "net_worth":0,"runway":0,"month_label":"—",
             "prev_income":0,"prev_expenses":0}
    if df.empty:
        return empty

    today = pd.Timestamp.today()
    cur_m = today.to_period("M")
    prv_m = (today - pd.DateOffset(months=1)).to_period("M")

    def ps(txn_type, period):
        mask = (df["type"] == txn_type) & (df["date"].dt.to_period("M") == period)
        return df.loc[mask, "amount"].sum()

    income   = ps("Income",  cur_m)
    expenses = ps("Expense", cur_m)
    savings  = ps("Savings", cur_m)

    savings_rate = (savings / income * 100) if income > 0 else 0

    idf       = inv_df()
    total_inv = idf["current"].sum() if not idf.empty else 0
    cum_sav   = df[df["type"] == "Savings"]["amount"].sum()
    net_worth = total_inv + cum_sav

    burn   = expenses if expenses > 0 else 1
    runway = cum_sav / burn

    return {
        "income":       income,
        "expenses":     expenses,
        "savings":      savings,
        "savings_rate": savings_rate,
        "net_worth":    net_worth,
        "runway":       runway,
        "month_label":  today.strftime("%B %Y"),
        "prev_income":  ps("Income",  prv_m),
        "prev_expenses":ps("Expense", prv_m),
    }


# ============================================================
# 6. CHARTS
# ============================================================
def chart_sankey(df: pd.DataFrame) -> go.Figure:
    today = pd.Timestamp.today()
    cur_m = today.to_period("M")
    month = df[df["date"].dt.to_period("M") == cur_m]
    inc_t = month[month["type"]=="Income"]["amount"].sum()
    exp_t = month[month["type"]=="Expense"]["amount"].sum()
    sav_t = month[month["type"]=="Savings"]["amount"].sum()
    if inc_t == 0:
        fig = go.Figure()
        fig.update_layout(title_text="No income data for this month", **CHART_LAYOUT)
        return fig
    ebc = month[month["type"]=="Expense"].groupby("category")["amount"].sum()
    sbc = month[month["type"]=="Savings"].groupby("category")["amount"].sum()
    labels = ["Income","Expenses","Savings"] + list(ebc.index) + list(sbc.index)
    idx    = {l:i for i,l in enumerate(labels)}
    src,tgt,vals,cols = [],[],[],[]
    def add(s,t,v,c):
        if v>0: src.append(idx[s]);tgt.append(idx[t]);vals.append(v);cols.append(c)
    add("Income","Expenses",exp_t,"rgba(0,212,255,0.35)")
    add("Income","Savings", sav_t,"rgba(16,185,129,0.35)")
    for c,v in ebc.items(): add("Expenses",c,v,"rgba(0,212,255,0.2)")
    for c,v in sbc.items(): add("Savings", c,v,"rgba(16,185,129,0.2)")
    nc = (["rgba(0,212,255,0.7)","rgba(168,85,247,0.6)","rgba(16,185,129,0.6)"] +
          ["rgba(168,85,247,0.3)"]*len(ebc) + ["rgba(16,185,129,0.3)"]*len(sbc))
    fig = go.Figure(go.Sankey(
        node=dict(pad=18, thickness=16, line=dict(color="rgba(255,255,255,0.08)",width=0.5),
                  label=labels, color=nc),
        link=dict(source=src,target=tgt,value=vals,color=cols,
                  hovertemplate="%{source.label} → %{target.label}<br>%{value:,.0f}<extra></extra>"),
    ))
    C = D["profile"]["currency"]
    fig.update_layout(title_text=f"This Month's Cash Flow ({C})", **CHART_LAYOUT)
    return fig


def chart_monthly_bar(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig=go.Figure(); fig.update_layout(title_text="No data",**CHART_LAYOUT); return fig
    df2 = df.copy()
    df2["month"] = df2["date"].dt.to_period("M").astype(str)
    cutoff = str((pd.Timestamp.today()-pd.DateOffset(months=11)).to_period("M"))
    df2 = df2[df2["month"]>=cutoff]
    monthly = df2.groupby(["month","type"])["amount"].sum().reset_index()
    cmap = {"Income":"#00d4ff","Expense":"#f43f5e","Savings":"#10b981"}
    fig = px.bar(monthly,x="month",y="amount",color="type",barmode="group",
                 color_discrete_map=cmap,labels={"amount":"Amount","month":"","type":""},
                 title="12-Month Overview")
    fig.update_traces(hovertemplate="%{y:,.0f}<extra></extra>")
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.05)",tickformat=",.0f"),
        **CHART_LAYOUT)
    return fig


def chart_expense_pie(df: pd.DataFrame) -> go.Figure:
    today=pd.Timestamp.today(); cur_m=today.to_period("M")
    exp = df[(df["type"]=="Expense")&(df["date"].dt.to_period("M")==cur_m)]
    if exp.empty:
        fig=go.Figure(); fig.update_layout(title_text="No expenses this month",**CHART_LAYOUT); return fig
    bc = exp.groupby("category")["amount"].sum().reset_index()
    colors=["#00d4ff","#a855f7","#10b981","#f59e0b","#f43f5e",
            "#6366f1","#ec4899","#14b8a6","#f97316","#84cc16","#06b6d4","#8b5cf6"]
    fig = go.Figure(go.Pie(
        labels=bc["category"],values=bc["amount"],hole=0.55,textinfo="label+percent",
        marker=dict(colors=colors[:len(bc)],line=dict(color="rgba(8,12,24,1)",width=2)),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<extra></extra>",
    ))
    fig.update_layout(title_text="Expense Breakdown (This Month)",showlegend=False,**CHART_LAYOUT)
    return fig


def chart_forecast(current_nw: float, monthly_savings: float,
                   years: int, annual_return: float) -> go.Figure:
    """
    Uses closed-form FV annuity formula:
      FV = PV*(1+r)^n + PMT*[((1+r)^n - 1)/r]
    Builds month-by-month series for the line, no loop bug.
    """
    # Ensure r is never 0 to avoid division errors
    r  = max((annual_return / 100) / 12, 1e-9)
    rh = max(((annual_return + 2) / 100) / 12, 1e-9)
    rl = max(((annual_return - 2) / 100) / 12, 1e-9)
    n  = years * 12

    dates = [datetime.today() + timedelta(days=30*i) for i in range(n+1)]

    # Build series via recurrence (avoids n nested loops)
    def series(pv, rate):
        v = [pv]
        for _ in range(n):
            v.append(v[-1]*(1+rate) + monthly_savings)
        return v

    central    = series(current_nw, r)
    optimistic = series(current_nw, rh)
    pessimistic= series(current_nw, rl)

    # Final value via closed form (used in callout metrics)
    final = current_nw*(1+r)**n + monthly_savings*(((1+r)**n - 1)/r)

    C = D["profile"]["currency"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates+dates[::-1], y=optimistic+pessimistic[::-1],
        fill="toself", fillcolor="rgba(168,85,247,0.07)",
        line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", name="±2% band",
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=central, mode="lines",
        line=dict(color="#a855f7", width=2.5),
        name=f"{annual_return:.1f}% p.a.",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:,.0f}<extra></extra>",
    ))
    fig.add_vline(x=datetime.today(), line_dash="dot",
                  line_color="rgba(255,255,255,0.2)",
                  annotation_text="Today", annotation_font_color="#c8d2f0")
    fig.add_annotation(x=dates[-1], y=central[-1],
                       text=f" {C}{final/100000:.1f}L",
                       showarrow=False,
                       font=dict(color="#a855f7",size=12,family="Space Grotesk"),
                       xanchor="left")
    fig.update_layout(
        title_text=f"Net Worth Projection — {years}Y @ {annual_return:.1f}%",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   tickformat=",.0f", tickprefix=C),
        hovermode="x unified", **CHART_LAYOUT,
    )
    return fig, final


def chart_asset_donut(idf: pd.DataFrame) -> go.Figure:
    if idf.empty:
        fig=go.Figure(); fig.update_layout(title_text="No investments yet",**CHART_LAYOUT); return fig
    alloc = idf.groupby("class")["current"].sum().reset_index()
    total = alloc["current"].sum()
    cols  = ["#00d4ff","#a855f7","#f59e0b","#10b981","#f43f5e","#6366f1"]
    C     = D["profile"]["currency"]
    fig = go.Figure(go.Pie(
        labels=alloc["class"], values=alloc["current"], hole=0.62,
        marker=dict(colors=cols[:len(alloc)], line=dict(color="rgba(8,12,24,1)",width=3)),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} (%{percent})<extra></extra>",
        textinfo="none",
    ))
    fig.add_annotation(text=f"{C}{total/100000:.1f}L<br><span style='font-size:11px'>Total</span>",
                       x=0.5,y=0.5,showarrow=False,
                       font=dict(size=18,color="#f0f4ff",family="Space Grotesk"))
    fig.update_layout(title_text="Asset Allocation",showlegend=True,**CHART_LAYOUT)
    return fig


def chart_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig=go.Figure(); fig.update_layout(title_text="No data",**CHART_LAYOUT); return fig
    exp = df[df["type"]=="Expense"].copy()
    exp["month"] = exp["date"].dt.to_period("M").astype(str)
    cutoff = str((pd.Timestamp.today()-pd.DateOffset(months=5)).to_period("M"))
    exp = exp[exp["month"]>=cutoff]
    if exp.empty:
        fig=go.Figure(); fig.update_layout(title_text="Need more data (6 months)",**CHART_LAYOUT); return fig
    pivot = exp.groupby(["category","month"])["amount"].sum().unstack(fill_value=0)
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,"rgba(0,212,255,0.05)"],[0.5,"rgba(168,85,247,0.5)"],[1,"rgba(244,63,94,0.8)"]],
        hovertemplate="<b>%{y}</b> · %{x}<br>%{z:,.0f}<extra></extra>",
    ))
    fig.update_layout(title_text="Spending Heatmap (6 months)",
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False,autorange="reversed"),**CHART_LAYOUT)
    return fig


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    exp = df[df["type"]=="Expense"].copy().sort_values("date")
    exp["month"] = exp["date"].dt.to_period("M")
    monthly = exp.groupby(["month","category"])["amount"].sum().reset_index().sort_values("month")
    monthly["rolling_avg"] = monthly.groupby("category")["amount"].transform(
        lambda x: x.shift(1).rolling(3,min_periods=1).mean()
    )
    monthly["pct"] = (monthly["amount"]/monthly["rolling_avg"]-1)*100
    flags = monthly[monthly["pct"]>20].copy().sort_values("pct",ascending=False)
    flags["month_str"] = flags["month"].astype(str)
    return flags[["month_str","category","amount","rolling_avg","pct"]].head(8)


def chart_savings_trend(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig=go.Figure(); fig.update_layout(**CHART_LAYOUT); return fig
    df2 = df.copy()
    df2["month"] = df2["date"].dt.to_period("M").astype(str)
    m = df2.groupby(["month","type"])["amount"].sum().unstack(fill_value=0).reset_index()
    if "Income" not in m.columns or "Savings" not in m.columns:
        fig=go.Figure(); fig.update_layout(**CHART_LAYOUT); return fig
    m["rate"] = (m["Savings"]/m["Income"].replace(0,np.nan)*100).fillna(0)
    m = m.tail(12)
    fig = go.Figure(go.Scatter(
        x=m["month"], y=m["rate"], mode="lines+markers",
        line=dict(color="#10b981",width=2.5),
        fill="tozeroy", fillcolor="rgba(16,185,129,0.08)",
        hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=20, line_dash="dash", line_color="rgba(255,255,255,0.2)",
                  annotation_text="20% target", annotation_font_color="#c8d2f0")
    fig.update_layout(
        title_text="Savings Rate Trend",
        yaxis=dict(ticksuffix="%",showgrid=True,gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(showgrid=False), **CHART_LAYOUT,
    )
    return fig


# ============================================================
# 7. ONBOARDING
# ============================================================
def render_onboarding():
    st.markdown("""
    <div class='wizard'>
        <div class='wizard-title'>💎 FinSight</div>
        <div class='wizard-sub'>Your personal finance command centre.<br>Quick setup — takes 60 seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown("#### 👤 Tell me about yourself")
        name  = st.text_input("Your name", placeholder="e.g. Arjun Sharma")
        curr  = st.selectbox("Currency", ["₹ (INR)","$ (USD)","€ (EUR)","£ (GBP)"])
        slab  = st.selectbox("Income tax slab (%)", [0,5,10,15,20,25,30], index=6)

        st.markdown("#### 💰 Optional: Monthly Budget Limits")
        st.caption("Leave at 0 to skip. You can set these later in ⚙️ Settings.")
        budgets = {}
        quick_cats = ["Rent / EMI","Groceries","Dining & Takeout","Transport","Entertainment","Utilities"]
        bc = st.columns(2)
        for i, cat in enumerate(quick_cats):
            with bc[i%2]:
                v = st.number_input(cat, min_value=0, value=0, step=500, key=f"ob_{cat}")
                if v > 0: budgets[cat] = v

        st.markdown("<br>", unsafe_allow_html=True)
        ok = st.button("✅  Launch My Dashboard", use_container_width=True,
                       type="primary", disabled=not name.strip())
        if ok:
            D["profile"]["name"]     = name.strip()
            D["profile"]["currency"] = curr.split()[0]
            D["profile"]["tax_slab"] = slab
            D["budgets"]             = budgets
            D["setup_done"]          = True
            st.session_state.page    = "🏠  Dashboard"
            st.rerun()


# ============================================================
# 8. SIDEBAR
# ============================================================
def render_sidebar():
    C    = D["profile"]["currency"]
    name = D["profile"].get("name","User")
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:16px 0 4px">
            <div style="font-size:2rem">💎</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.25rem;font-weight:700;
                        background:linear-gradient(90deg,#eef2ff,#00d4ff);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                FinSight
            </div>
            <div style="font-size:.75rem;color:rgba(200,210,240,0.4);
                        letter-spacing:1.4px;text-transform:uppercase;margin-top:2px">
                {name}'s Finance
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        pages = ["🏠  Dashboard","➕  Add Transaction","📋  Transactions",
                 "📊  Analytics","💼  Investments","🎯  Goals","🧾  Tax (80C)","⚙️  Settings"]
        page = st.radio("", pages, index=pages.index(st.session_state.page),
                        label_visibility="collapsed")
        st.session_state.page = page

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div style='font-size:.7rem;letter-spacing:1.2px;color:rgba(200,210,240,0.35);text-transform:uppercase;margin-bottom:8px'>Data</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️  Export JSON backup",
            data=export_json(),
            file_name=f"finsight_{name.lower().replace(' ','_')}_{date.today()}.json",
            mime="application/json",
            use_container_width=True,
        )
        uploaded = st.file_uploader("⬆️  Restore backup", type="json", label_visibility="visible")
        if uploaded is not None:
            try:
                import_json(uploaded.read().decode("utf-8"))
                st.success("Restored!")
                st.rerun()
            except Exception as e:
                st.error(f"Invalid file: {e}")

        st.markdown(f"<div style='font-size:.7rem;color:rgba(200,210,240,0.3);text-align:center;margin-top:12px'>{datetime.now().strftime('%d %b %Y · %H:%M')}</div>", unsafe_allow_html=True)


# ============================================================
# 9. PAGES
# ============================================================

# ── Dashboard ─────────────────────────────────────────────────
def page_dashboard():
    C    = D["profile"]["currency"]
    name = D["profile"].get("name","User")
    df   = txn_df()
    kpis = compute_kpis(df)

    st.markdown(f'<div class="ptitle">Good day, {name} 👋</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="psub">{kpis["month_label"]} · Financial Snapshot</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">🏠 DASHBOARD</span>', unsafe_allow_html=True)

    def delta(cur, prev):
        if prev == 0: return ""
        p = (cur-prev)/prev*100
        cls = "bg" if p>=0 else "br"; sym = "↑" if p>=0 else "↓"
        return f'<span class="badge {cls}">{sym} {abs(p):.1f}% vs last month</span>'

    k1,k2,k3,k4 = st.columns(4)
    with k1:
        nw = kpis["net_worth"]
        st.markdown(f"""<div class="card kpi">
            <div class="orb" style="background:#00d4ff;box-shadow:0 0 60px #00d4ff"></div>
            <div class="kpi-label">Net Worth</div>
            <div class="kpi-value">{C}{nw/100000:.1f}L</div>
            <span class="badge bg">All-time savings</span>
        </div>""", unsafe_allow_html=True)
    with k2:
        i = kpis["income"]
        st.markdown(f"""<div class="card kpi">
            <div class="orb" style="background:#10b981;box-shadow:0 0 60px #10b981"></div>
            <div class="kpi-label">Income This Month</div>
            <div class="kpi-value">{C}{i:,.0f}</div>
            {delta(i, kpis['prev_income'])}
        </div>""", unsafe_allow_html=True)
    with k3:
        e = kpis["expenses"]
        st.markdown(f"""<div class="card kpi">
            <div class="orb" style="background:#f43f5e;box-shadow:0 0 60px #f43f5e"></div>
            <div class="kpi-label">Expenses This Month</div>
            <div class="kpi-value">{C}{e:,.0f}</div>
            {delta(e, kpis['prev_expenses'])}
        </div>""", unsafe_allow_html=True)
    with k4:
        sr = kpis["savings_rate"]
        cls = "bg" if sr>=20 else ("ba" if sr>=10 else "br")
        tip = "✓ On track" if sr>=20 else ("⚠ Aim for 20%" if sr>=10 else "⚠ Too low")
        st.markdown(f"""<div class="card kpi">
            <div class="orb" style="background:#a855f7;box-shadow:0 0 60px #a855f7"></div>
            <div class="kpi-label">Savings Rate</div>
            <div class="kpi-value">{sr:.1f}%</div>
            <span class="badge {cls}">{tip}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    rw  = kpis["runway"]
    sav = kpis["savings"]
    rw_cls = "bg" if rw>=6 else "br"
    st.markdown(f"""
    <div class="card" style="padding:18px 24px;margin-bottom:18px">
        <div style="display:flex;gap:48px;flex-wrap:wrap;align-items:center">
            <div>
                <div class="kpi-label">Cash Runway</div>
                <span style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700">
                    {rw:.1f} months
                </span>
                &nbsp;<span class="badge {rw_cls}">{'✓ 6-month goal met' if rw>=6 else '⚠ Below 6-month goal'}</span>
            </div>
            <div>
                <div class="kpi-label">Saved This Month</div>
                <span style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#10b981">
                    {C}{sav:,.0f}
                </span>
            </div>
            <div>
                <div class="kpi-label">Budgets Active</div>
                <span style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700">
                    {len(D['budgets'])} categories
                </span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    ca, cb = st.columns([3,2])
    with ca:
        st.markdown('<div class="sh">Cash Flow</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_sankey(df), use_container_width=True)
    with cb:
        st.markdown('<div class="sh">Expense Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_expense_pie(df), use_container_width=True)

    st.plotly_chart(chart_monthly_bar(df), use_container_width=True)

    # Budget tracker
    if D["budgets"] and not df.empty:
        st.markdown('<div class="sh">Budget vs Actual (This Month)</div>', unsafe_allow_html=True)
        today  = pd.Timestamp.today()
        cur_m  = today.to_period("M")
        cur_exp= df[(df["type"]=="Expense")&(df["date"].dt.to_period("M")==cur_m)]
        bc = st.columns(min(len(D["budgets"]), 3))
        for i, (cat, budget) in enumerate(D["budgets"].items()):
            actual = cur_exp[cur_exp["category"]==cat]["amount"].sum()
            pct    = min(actual/budget, 1.0) if budget > 0 else 0
            col    = "#f43f5e" if pct>0.9 else ("#f59e0b" if pct>0.7 else "#10b981")
            with bc[i%3]:
                st.markdown(f"""
                <div class="card" style="padding:14px 16px">
                    <div style="font-size:.82rem;font-weight:600;margin-bottom:6px">{cat}</div>
                    <div style="display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);margin-bottom:6px">
                        <span>Spent: {C}{actual:,.0f}</span>
                        <span>Limit: {C}{budget:,.0f}</span>
                    </div>
                    <div class="pbar-wrap">
                        <div class="pbar-fill" style="width:{pct*100:.0f}%;background:linear-gradient(90deg,{col}88,{col})"></div>
                    </div>
                    <div style="font-size:.72rem;color:{col};margin-top:4px">{pct*100:.0f}% used</div>
                </div>""", unsafe_allow_html=True)


# ── Add Transaction ────────────────────────────────────────────
def page_add():
    C = D["profile"]["currency"]
    st.markdown('<div class="ptitle">Add Transaction</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Record income, expenses, or savings instantly</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">➕ NEW ENTRY</span>', unsafe_allow_html=True)

    with st.form("add_txn", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1: txn_type = st.selectbox("Type", ["Expense","Income","Savings"])
        with c2: txn_date = st.date_input("Date", value=date.today())
        c3,c4 = st.columns(2)
        with c3:
            cats = INCOME_CATS if txn_type=="Income" else (SAVINGS_CATS if txn_type=="Savings" else EXPENSE_CATS)
            category = st.selectbox("Category", cats)
        with c4:
            amount = st.number_input(f"Amount ({C})", min_value=1.0, step=100.0)
        note = st.text_input("Note (optional)", placeholder="e.g. Monthly rent, Zomato…")
        if st.form_submit_button("💾  Save", use_container_width=True, type="primary"):
            D["transactions"].append({
                "date":str(txn_date),"type":txn_type,
                "category":category,"amount":float(amount),"note":note,
            })
            st.success(f"✅ Saved: {txn_type} {C}{amount:,.0f} — {category}")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sh">Quick Add</div>', unsafe_allow_html=True)
    st.caption("Pre-fill common recurring entries.")
    qa = st.columns(4)
    quick = [("💼 Salary","Income","Salary"),("📈 SIP","Savings","Mutual Fund / SIP"),
             ("🏠 Rent","Expense","Rent / EMI"),("🛒 Groceries","Expense","Groceries")]
    for col,(lbl,t,c) in zip(qa,quick):
        with col:
            if st.button(lbl, use_container_width=True):
                D["transactions"].append({
                    "date":str(date.today()),"type":t,"category":c,
                    "amount":0.0,"note":"Quick add — update amount in Transactions",
                })
                st.info(f"'{lbl}' added. Update amount in 📋 Transactions.")
                st.rerun()


# ── Transactions ledger ────────────────────────────────────────
def page_transactions():
    C = D["profile"]["currency"]
    st.markdown('<div class="ptitle">Transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Full ledger · filter · delete</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">📋 LEDGER</span>', unsafe_allow_html=True)

    df = txn_df()
    if df.empty:
        st.info("No transactions yet. Go to ➕ Add Transaction.")
        return

    fc1,fc2,fc3 = st.columns(3)
    with fc1:
        f_type = st.multiselect("Type", ["Income","Expense","Savings"],
                                default=["Income","Expense","Savings"])
    with fc2:
        all_cats = sorted(df["category"].unique())
        f_cat = st.multiselect("Category", all_cats, default=all_cats)
    with fc3:
        months = ["All"] + sorted(df["date"].dt.to_period("M").astype(str).unique(), reverse=True)
        f_month = st.selectbox("Month", months)

    filtered = df[df["type"].isin(f_type) & df["category"].isin(f_cat)]
    if f_month != "All":
        filtered = filtered[filtered["date"].dt.to_period("M").astype(str)==f_month]

    inc = filtered[filtered["type"]=="Income"]["amount"].sum()
    exp = filtered[filtered["type"]=="Expense"]["amount"].sum()
    sav = filtered[filtered["type"]=="Savings"]["amount"].sum()
    s1,s2,s3 = st.columns(3)
    s1.metric("Income",   f"{C}{inc:,.0f}")
    s2.metric("Expenses", f"{C}{exp:,.0f}")
    s3.metric("Savings",  f"{C}{sav:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)
    disp = filtered.copy()
    disp["date"] = disp["date"].dt.strftime("%d %b %Y")
    disp = disp.rename(columns={"date":"Date","type":"Type","category":"Category",
                                 "amount":"Amount","note":"Note"})
    st.dataframe(disp[["Date","Type","Category","Amount","Note"]],
                 use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("✏️  Edit a transaction amount"):
        if D["transactions"]:
            opts = [f"{t['date']} | {t['type']} | {t['category']} | {C}{float(t['amount']):,.0f}"
                    for t in D["transactions"]]
            sel = st.selectbox("Select", opts, key="edit_sel")
            new_a = st.number_input(f"New amount ({C})", min_value=0.0, step=100.0, key="edit_amt")
            if st.button("Update amount", type="primary"):
                idx = opts.index(sel)
                D["transactions"][idx]["amount"] = float(new_a)
                st.success("Updated!")
                st.rerun()

    with st.expander("🗑️  Delete a transaction"):
        if D["transactions"]:
            opts2 = [f"{t['date']} | {t['type']} | {t['category']} | {C}{float(t['amount']):,.0f}"
                     for t in D["transactions"]]
            sel2 = st.selectbox("Select", opts2, key="del_sel")
            if st.button("Delete", type="primary", key="del_btn"):
                D["transactions"].pop(opts2.index(sel2))
                st.success("Deleted.")
                st.rerun()


# ── Analytics ──────────────────────────────────────────────────
def page_analytics():
    C = D["profile"]["currency"]
    st.markdown('<div class="ptitle">Analytics & Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Patterns · anomaly detection · wealth projection</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">📊 ANALYTICS</span>', unsafe_allow_html=True)

    df   = txn_df()
    kpis = compute_kpis(df)

    # Net Worth Forecast
    st.markdown('<div class="sh">Net Worth Forecast</div>', unsafe_allow_html=True)
    current_nw  = max(kpis["net_worth"], 0.0)
    monthly_sav = kpis["savings"] if kpis["savings"] > 0 else 0.0

    if current_nw == 0 and monthly_sav == 0:
        st.info("Add savings transactions or investments to see your forecast.")
    else:
        fc1, fc2 = st.columns(2)
        with fc1:
            proj_ret = st.slider("Annual Return (%)", 4.0, 24.0, 12.0, 0.5, key="pr")
        with fc2:
            proj_yr  = st.slider("Horizon (years)", 1, 20, 5, 1, key="py")

        # chart_forecast returns (fig, final_value)
        fig_fc, final_val = chart_forecast(current_nw, monthly_sav, proj_yr, proj_ret)
        st.plotly_chart(fig_fc, use_container_width=True)

        mult = (final_val/current_nw) if current_nw > 0 else 0.0
        m1,m2,m3 = st.columns(3)
        m1.markdown(f"""<div class="card" style="min-height:80px">
            <div class="kpi-label">Projected Net Worth</div>
            <div class="kpi-value" style="font-size:1.4rem">{C}{final_val/100000:.1f}L</div>
        </div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="card" style="min-height:80px">
            <div class="kpi-label">Wealth Multiplier</div>
            <div class="kpi-value" style="font-size:1.4rem">{mult:.2f}×</div>
        </div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="card" style="min-height:80px">
            <div class="kpi-label">Monthly Savings Input</div>
            <div class="kpi-value" style="font-size:1.4rem">{C}{monthly_sav:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Spending Heatmap
    st.markdown('<div class="sh">Spending Heatmap</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_heatmap(df), use_container_width=True)

    st.divider()

    # Anomaly detection
    st.markdown('<div class="sh">⚠️ Spending Anomalies</div>', unsafe_allow_html=True)
    st.caption("Categories >20% above their rolling 3-month average.")
    anomalies = detect_anomalies(df)
    if anomalies.empty:
        st.success("✅ No anomalies detected. Spending looks consistent.")
    else:
        for _, row in anomalies.iterrows():
            pct   = float(row["pct"])
            color = "#f43f5e" if pct>50 else "#f59e0b"
            avg   = float(row["rolling_avg"]) if not pd.isna(row["rolling_avg"]) else 0.0
            st.markdown(f"""
            <div class="arow">
                <div>
                    <strong style="color:#f0f4ff">{row['category']}</strong>
                    <span style="color:var(--muted);margin-left:10px;font-size:.8rem">{row['month_str']}</span>
                </div>
                <div style="display:flex;gap:18px;align-items:center">
                    <span>{C}{float(row['amount']):,.0f}</span>
                    <span style="color:var(--muted);font-size:.8rem">avg {C}{avg:,.0f}</span>
                    <span style="color:{color};font-weight:700">+{pct:.0f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sh">Savings Rate Trend</div>', unsafe_allow_html=True)
    st.plotly_chart(chart_savings_trend(df), use_container_width=True)


# ── Investments ────────────────────────────────────────────────
def page_investments():
    C = D["profile"]["currency"]
    st.markdown('<div class="ptitle">Investments</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Portfolio tracker · P&amp;L · allocation</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">💼 INVESTMENTS</span>', unsafe_allow_html=True)

    with st.expander("➕  Add Investment"):
        with st.form("add_inv"):
            ia, ib = st.columns(2)
            with ia: n = st.text_input("Fund / Asset name", placeholder="e.g. Nifty 50 Index Fund")
            with ib: cls = st.selectbox("Asset Class",["Equity","Debt / Bonds","Gold","Cash / FD","Real Estate","Crypto","US Stocks","Other"])
            ic, id_ = st.columns(2)
            with ic: inv = st.number_input(f"Invested ({C})", min_value=0.0, step=500.0)
            with id_: cur_val = st.number_input(f"Current Value ({C})", min_value=0.0, step=500.0)
            dt = st.date_input("Start date", value=date.today())
            if st.form_submit_button("Save", use_container_width=True, type="primary"):
                if n.strip():
                    D["investments"].append({"name":n.strip(),"class":cls,
                                              "invested":float(inv),"current":float(cur_val),
                                              "date":str(dt)})
                    st.success(f"✅ {n} saved!"); st.rerun()
                else: st.warning("Enter a name.")

    idf = inv_df()
    if idf.empty:
        st.info("No investments yet. Add your first above.")
        return

    ti = idf["invested"].sum(); tc = idf["current"].sum()
    pnl = tc-ti; pp = (pnl/ti*100) if ti>0 else 0
    k1,k2,k3 = st.columns(3)
    k1.markdown(f"""<div class="card kpi"><div class="kpi-label">Total Invested</div>
        <div class="kpi-value">{C}{ti:,.0f}</div></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="card kpi"><div class="kpi-label">Current Value</div>
        <div class="kpi-value">{C}{tc:,.0f}</div></div>""", unsafe_allow_html=True)
    pc = "bg" if pnl>=0 else "br"
    k3.markdown(f"""<div class="card kpi"><div class="kpi-label">Total P&L</div>
        <div class="kpi-value" style="color:{'#10b981' if pnl>=0 else '#f43f5e'}">
            {'▲' if pnl>=0 else '▼'} {C}{abs(pnl):,.0f}</div>
        <span class="badge {pc}">{pp:+.2f}%</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns([2,3])
    with ca: st.plotly_chart(chart_asset_donut(idf), use_container_width=True)
    with cb:
        st.markdown('<div class="sh">Holdings</div>', unsafe_allow_html=True)
        d2 = idf.copy()
        d2["P&L"]   = d2["current"]-d2["invested"]
        d2["P&L %"] = ((d2["P&L"]/d2["invested"])*100).round(2)
        d2["invested"] = d2["invested"].apply(lambda x: f"{C}{x:,.0f}")
        d2["current"]  = d2["current"].apply(lambda x: f"{C}{x:,.0f}")
        d2["P&L"] = d2.apply(lambda r: f"{'▲' if r['P&L']>=0 else '▼'} {C}{abs(r['P&L']):,.0f}", axis=1)
        d2 = d2.rename(columns={"name":"Asset","class":"Class","invested":"Invested","current":"Value"})
        st.dataframe(d2[["Asset","Class","Invested","Value","P&L","P&L %"]],
                     use_container_width=True, hide_index=True)

    with st.expander("✏️  Update current value"):
        if D["investments"]:
            opts = [f"{i['name']}" for i in D["investments"]]
            sel  = st.selectbox("Select", opts, key="upd_inv")
            nv   = st.number_input(f"New current value ({C})", min_value=0.0, step=500.0, key="upd_nv")
            if st.button("Update", type="primary", key="upd_btn"):
                D["investments"][opts.index(sel)]["current"] = float(nv)
                st.success("Updated!"); st.rerun()

    with st.expander("🗑️  Delete an investment"):
        if D["investments"]:
            opts2 = [f"{i['name']} ({i['class']})" for i in D["investments"]]
            sel2  = st.selectbox("Select", opts2, key="del_inv")
            if st.button("Delete", type="primary", key="del_inv_btn"):
                D["investments"].pop(opts2.index(sel2))
                st.success("Deleted."); st.rerun()


# ── Goals ──────────────────────────────────────────────────────
def page_goals():
    C = D["profile"]["currency"]
    st.markdown('<div class="ptitle">Goals</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Track what you\'re saving toward</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">🎯 GOALS</span>', unsafe_allow_html=True)

    COLORS = ["#00d4ff","#a855f7","#10b981","#f59e0b","#f43f5e","#6366f1","#ec4899"]
    with st.expander("➕  Add Goal"):
        with st.form("add_goal"):
            ga,gb = st.columns(2)
            with ga: gn = st.text_input("Goal name", placeholder="e.g. Emergency Fund")
            with gb: gt = st.number_input(f"Target ({C})", min_value=100.0, step=1000.0)
            gc,gd = st.columns(2)
            with gc: gcu = st.number_input(f"Saved so far ({C})", min_value=0.0, step=500.0)
            with gd: gdl = st.text_input("Deadline", placeholder="e.g. Dec 2025")
            gcol = st.selectbox("Colour", COLORS)
            if st.form_submit_button("Save Goal", use_container_width=True, type="primary"):
                if gn.strip():
                    D["goals"].append({"name":gn.strip(),"target":float(gt),
                                        "current":float(gcu),"deadline":gdl,"color":gcol})
                    st.success(f"✅ Goal '{gn}' added!"); st.rerun()

    gdf = goals_df()
    if gdf.empty:
        st.info("No goals yet. Add your first goal above.")
        return

    cols = st.columns(2)
    for i, (_, g) in enumerate(gdf.iterrows()):
        pct  = min(g["current"]/g["target"], 1.0) if g["target"]>0 else 0
        col  = g["color"]
        rem  = max(g["target"]-g["current"], 0)
        with cols[i%2]:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:.98rem;font-weight:600;margin-bottom:4px">{g['name']}</div>
                <div style="font-size:.8rem;color:var(--muted);margin-bottom:10px">
                    🎯 {C}{g['target']:,.0f} &nbsp;·&nbsp; 📅 {g['deadline']}
                </div>
                <div style="display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:6px">
                    <span style="font-weight:600">{C}{g['current']:,.0f} saved</span>
                    <span style="color:var(--muted)">{C}{rem:,.0f} to go</span>
                </div>
                <div class="pbar-wrap">
                    <div class="pbar-fill" style="width:{pct*100:.1f}%;background:linear-gradient(90deg,{col}88,{col})"></div>
                </div>
                <div style="font-size:.75rem;color:{col};margin-top:6px;font-weight:600">
                    {pct*100:.1f}% complete
                </div>
            </div>""", unsafe_allow_html=True)

    with st.expander("✏️  Update goal progress"):
        gnms = [g["name"] for g in D["goals"]]
        sel  = st.selectbox("Goal", gnms)
        namt = st.number_input(f"New saved amount ({C})", min_value=0.0, step=500.0)
        if st.button("Update", type="primary", key="upd_goal"):
            D["goals"][gnms.index(sel)]["current"] = float(namt)
            st.success("Updated!"); st.rerun()

    with st.expander("🗑️  Delete a goal"):
        gnms2 = [g["name"] for g in D["goals"]]
        sel2  = st.selectbox("Goal", gnms2, key="del_goal2")
        if st.button("Delete goal", type="primary", key="del_goal_btn"):
            D["goals"].pop(gnms2.index(sel2))
            st.success("Deleted."); st.rerun()


# ── Tax (80C) ──────────────────────────────────────────────────
def page_tax():
    C    = D["profile"]["currency"]
    LIMIT= 150000
    st.markdown('<div class="ptitle">Tax Strategy</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Section 80C tracker · deduction optimiser (India)</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">🧾 TAX</span>', unsafe_allow_html=True)

    with st.expander("➕  Add 80C Investment"):
        with st.form("add_tax"):
            ta,tb = st.columns(2)
            with ta: tn = st.selectbox("Instrument",["PPF","ELSS Mutual Fund","LIC / Term Insurance",
                "EPF (voluntary)","NSC","Sukanya Samriddhi","Home Loan Principal",
                "Tax Saver FD","NPS","Other 80C"])
            with tb: tv = st.number_input(f"Amount ({C})", min_value=0.0, step=500.0)
            if st.form_submit_button("Save", use_container_width=True, type="primary"):
                D["tax_80c"].append({"instrument":tn,"invested":float(tv)})
                st.success("Saved!"); st.rerun()

    tdf   = tax_df()
    total = min(tdf["invested"].sum(), LIMIT) if not tdf.empty else 0
    rem   = max(LIMIT-total, 0)
    slab  = D["profile"].get("tax_slab", 30)
    saved = total*(slab/100)
    pct   = total/LIMIT

    k1,k2,k3 = st.columns(3)
    k1.markdown(f"""<div class="card kpi">
        <div class="kpi-label">80C Invested</div>
        <div class="kpi-value">{C}{total:,.0f}</div>
        <span class="badge {'bg' if pct>=1 else 'ba'}">{'✅ Maxed!' if pct>=1 else f'{C}{rem:,.0f} remaining'}</span>
    </div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="card kpi">
        <div class="kpi-label">Section 80C Limit</div>
        <div class="kpi-value">{C}1,50,000</div>
        <span class="badge ba">IT Act</span>
    </div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="card kpi">
        <div class="kpi-label">Tax Saved ({slab}% slab)</div>
        <div class="kpi-value">{C}{saved:,.0f}</div>
        <span class="badge bg">Old regime</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:.85rem">
            <span style="color:var(--muted)">{C}0</span>
            <span style="font-weight:600">{C}{total:,.0f} of {C}1,50,000</span>
            <span style="color:var(--muted)">{C}1,50,000</span>
        </div>
        <div class="pbar-wrap" style="height:16px">
            <div class="pbar-fill" style="width:{min(pct,1)*100:.1f}%"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:.82rem">
            <span style="color:#10b981">{pct*100:.1f}% utilised</span>
            <span style="color:#f59e0b">Remaining: {C}{rem:,.0f}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    if not tdf.empty:
        st.markdown('<div class="sh">Instruments</div>', unsafe_allow_html=True)
        for _, row in tdf.iterrows():
            st.markdown(f"""
            <div class="card" style="padding:12px 20px;display:flex;justify-content:space-between;align-items:center">
                <div style="font-weight:600;font-size:.9rem">{row['instrument']}</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:600">{C}{row['invested']:,.0f}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh">💡 Tax Tips</div>', unsafe_allow_html=True)
    tips = [
        ("80CCD(1B)", f"Extra {C}50,000 NPS deduction above the 80C cap."),
        ("80D — Health Insurance", f"Up to {C}25,000 deduction on health insurance premiums."),
        ("HRA Exemption", "Structure rent allowance to maximise Section 10(13A)."),
        ("LTCG Harvesting", f"Book {C}1L/year equity gains tax-free under Section 112A."),
        ("New vs Old Regime", "Compare both regimes before filing. New regime may suit you."),
    ]
    for title, desc in tips:
        st.markdown(f"""
        <div class="card" style="padding:12px 18px">
            <div style="font-weight:600;font-size:.88rem;margin-bottom:3px">📌 {title}</div>
            <div style="font-size:.82rem;color:var(--muted)">{desc}</div>
        </div>""", unsafe_allow_html=True)

    with st.expander("🗑️  Delete a 80C entry"):
        if D["tax_80c"]:
            opts = [f"{t['instrument']} — {C}{float(t['invested']):,.0f}" for t in D["tax_80c"]]
            sel  = st.selectbox("Select", opts)
            if st.button("Delete", type="primary", key="del_tax"):
                D["tax_80c"].pop(opts.index(sel)); st.success("Deleted."); st.rerun()


# ── Settings ───────────────────────────────────────────────────
def page_settings():
    st.markdown('<div class="ptitle">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Profile · budgets · danger zone</div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">⚙️ SETTINGS</span>', unsafe_allow_html=True)

    st.markdown('<div class="sh">Profile</div>', unsafe_allow_html=True)
    with st.form("prof"):
        nn = st.text_input("Your name", value=D["profile"].get("name",""))
        curr_opts = ["₹ (INR)","$ (USD)","€ (EUR)","£ (GBP)"]
        cur_curr  = D["profile"].get("currency","₹")
        curr_idx  = next((i for i,x in enumerate(curr_opts) if x.startswith(cur_curr)), 0)
        nc = st.selectbox("Currency", curr_opts, index=curr_idx)
        ns = st.selectbox("Tax slab (%)",[0,5,10,15,20,25,30],
                          index=[0,5,10,15,20,25,30].index(D["profile"].get("tax_slab",30)))
        if st.form_submit_button("Save Profile", type="primary"):
            D["profile"]["name"]     = nn.strip()
            D["profile"]["currency"] = nc.split()[0]
            D["profile"]["tax_slab"] = ns
            st.success("Profile saved!"); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sh">Monthly Budgets</div>', unsafe_allow_html=True)
    with st.form("budgets"):
        nb = {}
        bc = st.columns(2)
        for i, cat in enumerate(EXPENSE_CATS):
            with bc[i%2]:
                v = st.number_input(cat, min_value=0,
                                    value=int(D["budgets"].get(cat,0)), step=500, key=f"bs_{cat}")
                if v > 0: nb[cat] = v
        if st.form_submit_button("Save Budgets", type="primary", use_container_width=True):
            D["budgets"] = nb; st.success("Budgets saved!"); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sh">⚠️ Danger Zone</div>', unsafe_allow_html=True)
    st.warning("This permanently erases ALL data. Export a JSON backup first.")
    if st.button("🔴  Reset Everything", type="primary"):
        st.session_state.data = default_data()
        st.session_state.page = "🏠  Dashboard"
        st.rerun()


# ============================================================
# 10. MAIN
# ============================================================
def main():
    inject_css()
    init_state()

    if not D.get("setup_done"):
        render_onboarding()
        return

    render_sidebar()
    p = st.session_state.page

    if   "Dashboard"    in p: page_dashboard()
    elif "Add"          in p: page_add()
    elif "Transaction"  in p: page_transactions()
    elif "Analytics"    in p: page_analytics()
    elif "Investments"  in p: page_investments()
    elif "Goals"        in p: page_goals()
    elif "Tax"          in p: page_tax()
    elif "Settings"     in p: page_settings()


if __name__ == "__main__":
    main()
