# =============================================================================
# PERSONAL FINANCE OS — Fully Personalised & Local Storage Ready
# =============================================================================
# Features : 100% User Data (No prebuilt dummies), JSON Import/Export,
#            Dynamic Data Editors, Glassmorphism UI, Error-Safe Analytics.
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="My Finance OS", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# =============================================================================
# 1. STATE MANAGEMENT & DATA PERSISTENCE
# =============================================================================

def init_session_state():
    """Initialize empty user data in session state if it doesn't exist."""
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "My"
    
    if 'transactions' not in st.session_state:
        st.session_state.transactions = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
        st.session_state.transactions['Date'] = pd.to_datetime(st.session_state.transactions['Date'])
        
    if 'investments' not in st.session_state:
        st.session_state.investments = pd.DataFrame(columns=["Asset Name", "Category", "Invested Amount", "Current Value"])
        
    if 'goals' not in st.session_state:
        st.session_state.goals = pd.DataFrame(columns=["Goal Name", "Target Amount", "Current Amount", "Deadline"])

def export_data_to_json():
    """Serialize session state dataframes to JSON for download."""
    data = {
        "user_name": st.session_state.user_name,
        "transactions": st.session_state.transactions.assign(Date=st.session_state.transactions['Date'].dt.strftime('%Y-%m-%d')).to_dict(orient="records"),
        "investments": st.session_state.investments.to_dict(orient="records"),
        "goals": st.session_state.goals.assign(Deadline=st.session_state.goals['Deadline'].astype(str)).to_dict(orient="records")
    }
    return json.dumps(data, indent=4)

def import_data_from_json(json_string):
    """Deserialize JSON and update session state."""
    try:
        data = json.loads(json_string)
        st.session_state.user_name = data.get("user_name", "My")
        
        tx_df = pd.DataFrame(data.get("transactions", []))
        if not tx_df.empty and 'Date' in tx_df.columns:
            tx_df['Date'] = pd.to_datetime(tx_df['Date'])
        st.session_state.transactions = tx_df if not tx_df.empty else pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
        
        st.session_state.investments = pd.DataFrame(data.get("investments", []), columns=["Asset Name", "Category", "Invested Amount", "Current Value"])
        st.session_state.goals = pd.DataFrame(data.get("goals", []), columns=["Goal Name", "Target Amount", "Current Amount", "Deadline"])
        
        return True
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
        return False

# Initialize state on boot
init_session_state()

# =============================================================================
# 2. GLASSMORPHISM CSS INJECTION
# =============================================================================
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root {
        --bg-primary:   #0a0e1a;
        --glass-bg:     rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.12);
        --accent-cyan:  #00d4ff;
        --accent-violet:#a855f7;
        --accent-green: #10b981;
        --accent-rose:  #f43f5e;
        --text-primary: #f0f4ff;
        --text-muted:   rgba(200, 210, 240, 0.6);
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 40%, #130f23 70%, #0d1520 100%);
        background-attachment: fixed;
        font-family: 'DM Sans', sans-serif; color: var(--text-primary);
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 26, 0.85) !important; backdrop-filter: blur(20px) !important; border-right: 1px solid var(--glass-border) !important;
    }
    .metric-card {
        background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 16px;
        backdrop-filter: blur(12px); padding: 24px; position: relative; overflow: hidden; min-height: 130px;
    }
    .metric-label { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; }
    .metric-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--text-primary); }
    .page-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #f0f4ff, var(--accent-cyan)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;}
    .section-header { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 600; margin: 20px 0 15px 0; border-bottom: 1px solid var(--glass-border); padding-bottom: 8px;}
    
    /* Make st.data_editor blend with glassmorphism */
    [data-testid="stDataFrame"] { background: var(--glass-bg); border-radius: 10px; border: 1px solid var(--glass-border); padding: 10px;}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 3. KPI CALCULATIONS (Safe handlers for empty data)
# =============================================================================
def compute_kpis():
    tx = st.session_state.transactions.dropna(subset=['Amount', 'Type'])
    inv = st.session_state.investments.dropna(subset=['Current Value'])
    goals = st.session_state.goals.dropna(subset=['Current Amount'])
    
    # Defaults
    income, expenses, savings = 0.0, 0.0, 0.0
    
    if not tx.empty:
        # Get current month data
        current_month = datetime.today().replace(day=1)
        # Ensure Date column is datetime
        tx['Date'] = pd.to_datetime(tx['Date'])
        cm_tx = tx[tx['Date'] >= current_month]
        
        income = cm_tx[cm_tx['Type'] == 'Income']['Amount'].sum()
        expenses = cm_tx[cm_tx['Type'] == 'Expense']['Amount'].sum()
        savings = cm_tx[cm_tx['Type'] == 'Savings']['Amount'].sum()
        
    net_worth = inv['Current Value'].sum() + goals['Current Amount'].sum()
    savings_rate = (savings / income * 100) if income > 0 else 0.0
    
    return {
        "net_worth": net_worth,
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate
    }

# =============================================================================
# 4. CHART GENERATORS (Error-Safe)
# =============================================================================
CHART_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8d2f0"), margin=dict(l=10, r=10, t=30, b=10))

def fig_sankey():
    tx = st.session_state.transactions.dropna(subset=['Amount', 'Type', 'Category'])
    if tx.empty:
        return go.Figure().update_layout(title="Add transactions in the Ledger to see Cash Flow", **CHART_LAYOUT)
        
    # Aggregate by Type and Category for current month
    current_month = datetime.today().replace(day=1)
    cm_tx = tx[pd.to_datetime(tx['Date']) >= current_month]
    
    if cm_tx.empty:
        return go.Figure().update_layout(title="No transactions this month yet.", **CHART_LAYOUT)

    income_total = cm_tx[cm_tx['Type'] == 'Income']['Amount'].sum()
    expenses = cm_tx[cm_tx['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
    savings = cm_tx[cm_tx['Type'] == 'Savings'].groupby('Category')['Amount'].sum()

    labels = ["Total Income"] + list(expenses.index) + list(savings.index)
    sources = []
    targets = []
    values = []
    
    idx = 1
    for cat, val in expenses.items():
        if val > 0: sources.append(0); targets.append(idx); values.append(val); idx+=1
    for cat, val in savings.items():
        if val > 0: sources.append(0); targets.append(idx); values.append(val); idx+=1

    if not sources: # Only income, no outflows
         return go.Figure().update_layout(title="Add expenses/savings to see flow.", **CHART_LAYOUT)

    fig = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color="#00d4ff"),
        link=dict(source=sources, target=targets, value=values, color="rgba(255,255,255,0.2)")
    ))
    fig.update_layout(title_text="Current Month Cash Flow", **CHART_LAYOUT)
    return fig

def fig_monthly_trend():
    tx = st.session_state.transactions.dropna(subset=['Amount', 'Type', 'Date'])
    if tx.empty:
        return go.Figure().update_layout(title="No data for trend chart", **CHART_LAYOUT)
        
    tx['Month'] = pd.to_datetime(tx['Date']).dt.to_period('M').astype(str)
    monthly = tx.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
    
    color_map = {"Income": "#00d4ff", "Expense": "#f43f5e", "Savings": "#10b981"}
    fig = px.bar(monthly, x="Month", y="Amount", color="Type", barmode="group", color_discrete_map=color_map)
    fig.update_layout(**CHART_LAYOUT)
    return fig

# =============================================================================
# 5. PAGE RENDERERS
# =============================================================================

def render_dashboard():
    kpis = compute_kpis()
    name = st.session_state.user_name
    
    st.markdown(f'<div class="page-title">{name}\'s Dashboard</div>', unsafe_allow_html=True)
    st.caption("Your high-level financial overview.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card"><div class="metric-label">Total Net Worth</div><div class="metric-value">₹{kpis['net_worth']:,.0f}</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><div class="metric-label">This Month's Savings</div><div class="metric-value" style="color:#10b981">₹{kpis['savings']:,.0f}</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card"><div class="metric-label">Savings Rate</div><div class="metric-value" style="color:#00d4ff">{kpis['savings_rate']:.1f}%</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.plotly_chart(fig_sankey(), use_container_width=True)
    with col_b:
        st.plotly_chart(fig_monthly_trend(), use_container_width=True)

def render_ledger():
    st.markdown('<div class="page-title">Transaction Ledger</div>', unsafe_allow_html=True)
    st.caption("Add, edit, or delete your income and expenses. Changes save automatically.")
    
    st.markdown('<div class="section-header">Record Transactions</div>', unsafe_allow_html=True)
    
    # Dynamic Data Editor - Acts like Excel
    edited_df = st.data_editor(
        st.session_state.transactions,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", required=True),
            "Type": st.column_config.SelectboxColumn("Type", options=["Income", "Expense", "Savings"], required=True),
            "Category": st.column_config.TextColumn("Category (e.g., Salary, Rent, Groceries)", required=True),
            "Amount": st.column_config.NumberColumn("Amount (₹)", min_value=0, format="%d", required=True)
        },
        key="tx_editor"
    )
    
    # Update state if changed
    if not edited_df.equals(st.session_state.transactions):
        st.session_state.transactions = edited_df

def render_investments():
    st.markdown('<div class="page-title">Portfolio & Goals</div>', unsafe_allow_html=True)
    st.caption("Track your wealth accumulation and target milestones.")
    
    tab1, tab2 = st.tabs(["💼 Current Portfolio", "🎯 Savings Goals"])
    
    with tab1:
        st.markdown('<div class="section-header">Manage Investments</div>', unsafe_allow_html=True)
        edited_inv = st.data_editor(
            st.session_state.investments,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Asset Name": st.column_config.TextColumn("Asset Name", required=True),
                "Category": st.column_config.SelectboxColumn("Category", options=["Equity", "Debt", "Real Estate", "Crypto", "Cash", "Other"], required=True),
                "Invested Amount": st.column_config.NumberColumn("Invested (₹)", min_value=0),
                "Current Value": st.column_config.NumberColumn("Current Value (₹)", min_value=0, required=True)
            },
            key="inv_editor"
        )
        if not edited_inv.equals(st.session_state.investments):
            st.session_state.investments = edited_inv
            
        # Quick summary chart
        inv_clean = st.session_state.investments.dropna(subset=['Current Value', 'Category'])
        if not inv_clean.empty and inv_clean['Current Value'].sum() > 0:
            fig = px.pie(inv_clean, values='Current Value', names='Category', hole=0.5, title="Asset Allocation")
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        st.markdown('<div class="section-header">Manage Goals</div>', unsafe_allow_html=True)
        edited_goals = st.data_editor(
            st.session_state.goals,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Goal Name": st.column_config.TextColumn("Goal Name", required=True),
                "Target Amount": st.column_config.NumberColumn("Target (₹)", min_value=1, required=True),
                "Current Amount": st.column_config.NumberColumn("Saved So Far (₹)", min_value=0, required=True),
                "Deadline": st.column_config.DateColumn("Deadline Date")
            },
            key="goal_editor"
        )
        if not edited_goals.equals(st.session_state.goals):
            st.session_state.goals = edited_goals
            
        # Progress bars
        goals_clean = st.session_state.goals.dropna(subset=['Target Amount', 'Current Amount', 'Goal Name'])
        if not goals_clean.empty:
            for _, row in goals_clean.iterrows():
                pct = min(row['Current Amount'] / row['Target Amount'], 1.0)
                st.markdown(f"**{row['Goal Name']}** (₹{row['Current Amount']:,.0f} / ₹{row['Target Amount']:,.0f})")
                st.progress(pct)

def render_analytics():
    st.markdown('<div class="page-title">Analytics & Forecasting</div>', unsafe_allow_html=True)
    st.caption("Insights based on your actual data.")
    
    kpis = compute_kpis()
    tx = st.session_state.transactions.dropna(subset=['Amount', 'Type', 'Date'])
    
    st.markdown('<div class="section-header">Wealth Forecaster</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    
    with col1:
        annual_return = st.slider("Expected Annual Return (%)", min_value=0.0, max_value=25.0, value=10.0, step=0.5)
        years = st.slider("Years to Project", min_value=1, max_value=30, value=5)
        
    with col2:
        if kpis['net_worth'] == 0 and kpis['savings'] == 0:
            st.info("💡 Add investments or monthly savings to see your wealth forecast.")
        else:
            monthly_r = (annual_return / 100) / 12
            months = years * 12
            dates = [datetime.today() + timedelta(days=30 * i) for i in range(months + 1)]
            
            # Use average monthly savings from last 3 months, or current month if short history
            avg_savings = kpis['savings'] # Simplified for robustness
            
            vals = [kpis['net_worth']]
            for _ in range(months):
                vals.append(vals[-1] * (1 + monthly_r) + avg_savings)
                
            fig = go.Figure(go.Scatter(x=dates, y=vals, mode="lines", line=dict(color="#a855f7", width=3), fill="tozeroy", fillcolor="rgba(168,85,247,0.1)"))
            fig.update_layout(title=f"Projected Net Worth: ₹{vals[-1]:,.0f} in {years} years", **CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Anomaly Detection (Spikes in Spending)</div>', unsafe_allow_html=True)
    if tx.empty or len(pd.to_datetime(tx['Date']).dt.to_period('M').unique()) < 2:
        st.info("💡 Need at least 2 months of transaction history to detect unusual spending.")
    else:
        # Safe anomaly logic
        try:
            expenses = tx[tx['Type'] == 'Expense'].copy()
            expenses['Date'] = pd.to_datetime(expenses['Date'])
            expenses['Month'] = expenses['Date'].dt.to_period('M')
            monthly_cat = expenses.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
            
            # Simple avg comparison
            cat_avg = monthly_cat.groupby('Category')['Amount'].mean().reset_index().rename(columns={'Amount': 'Avg'})
            current_month = datetime.today().to_period('M')
            current_spend = monthly_cat[monthly_cat['Month'] == current_month]
            
            merged = pd.merge(current_spend, cat_avg, on='Category')
            merged['Diff %'] = ((merged['Amount'] - merged['Avg']) / merged['Avg']) * 100
            
            anomalies = merged[merged['Diff %'] > 20] # Flag if 20% higher than average
            
            if anomalies.empty:
                st.success("✅ No unusual spending detected this month compared to your averages.")
            else:
                for _, row in anomalies.iterrows():
                    st.warning(f"⚠️ **{row['Category']}**: You spent ₹{row['Amount']:,.0f} this month. This is {row['Diff %']:.0f}% higher than your average of ₹{row['Avg']:,.0f}.")
        except Exception as e:
            st.info("Not enough consistent data to run anomaly detection yet. Keep logging!")

def render_settings():
    st.markdown('<div class="page-title">Settings & Data Backup</div>', unsafe_allow_html=True)
    st.caption("Manage your profile and secure your data locally.")
    
    st.markdown('<div class="section-header">Profile</div>', unsafe_allow_html=True)
    new_name = st.text_input("Your Name", value=st.session_state.user_name)
    if new_name != st.session_state.user_name:
        st.session_state.user_name = new_name
        st.success("Name updated!")
        st.rerun()

    st.markdown('<div class="section-header">Local Data Backup</div>', unsafe_allow_html=True)
    st.write("Since this app does not use a database, your data resets when the server sleeps. **Download your data before leaving**, and upload it when you return.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📥 Export Data")
        json_str = export_data_to_json()
        st.download_button(
            label="Download My Data (JSON)",
            file_name=f"{st.session_state.user_name}_finance_backup.json",
            mime="application/json",
            data=json_str,
            type="primary"
        )
        
    with col2:
        st.subheader("📤 Import Data")
        uploaded_file = st.file_uploader("Upload previous JSON backup", type=["json"])
        if uploaded_file is not None:
            if st.button("Restore Data"):
                json_content = uploaded_file.getvalue().decode("utf-8")
                if import_data_from_json(json_content):
                    st.success("Data restored successfully!")
                    st.rerun()
                    
    st.markdown('<div class="section-header" style="color:#f43f5e">Danger Zone</div>', unsafe_allow_html=True)
    if st.button("Wipe All Data (Reset App)", type="primary"):
        st.session_state.clear()
        st.rerun()

# =============================================================================
# 6. APP ROUTING
# =============================================================================
def main():
    inject_css()
    
    with st.sidebar:
        st.markdown(f"<h2>💎 {st.session_state.user_name}'s OS</h2>", unsafe_allow_html=True)
        st.divider()
        nav = st.radio("Navigation", ["📊 Dashboard", "📝 Ledger (Input)", "💼 Portfolio & Goals", "📈 Analytics", "⚙️ Settings & Backup"], label_visibility="collapsed")
        
    if "Dashboard" in nav: render_dashboard()
    elif "Ledger" in nav: render_ledger()
    elif "Portfolio" in nav: render_investments()
    elif "Analytics" in nav: render_analytics()
    elif "Settings" in nav: render_settings()

if __name__ == "__main__":
    main()
