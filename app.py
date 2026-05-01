# =========================
# QARD-E-HASAN FINTECH APP
# =========================

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Resolve CSV paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def csv_path(f):
    return os.path.join(BASE_DIR, f)

def safe_save(df, filename):
    try:
        df.to_csv(csv_path(filename), index=False)
        return True
    except PermissionError:
        st.error(f"Cannot save '{filename}' — close it in Excel or any other program and try again.")
        return False

st.set_page_config(
    page_title="Qard-e-Hasan",
    page_icon="Q",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif !important;
}
.stApp {
    background: #f0fdf9;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f766e !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebarNav"] {
    padding-top: 0;
}

/* ── Sidebar radio buttons → nav items ── */
[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 2px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex !important;
    align-items: center;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    color: rgba(255,255,255,0.7) !important;
    background: transparent !important;
    border: none !important;
    transition: background 0.15s;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [aria-checked="true"] {
    background: rgba(255,255,255,0.15) !important;
    color: #fff !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] span {
    font-size: 13px;
}
[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none;
}

/* ── Sidebar text inputs ── */
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.1) !important;
    border: 0.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: rgba(255,255,255,0.4) !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: rgba(255,255,255,0.5) !important;
    box-shadow: none !important;
}

/* ── Sidebar selectbox ── */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.1) !important;
    border: 0.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #0f766e !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: background 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #14b8a6 !important;
}

/* ── Main content inputs ── */
.stTextInput input, .stNumberInput input {
    border: 0.5px solid #d1d5db !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    color: #111827 !important;
    background: #fff !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #14b8a6 !important;
    box-shadow: 0 0 0 2px rgba(20,184,166,0.15) !important;
}
.stSelectbox > div > div {
    border: 0.5px solid #d1d5db !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #0f766e !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #fff;
    border: 0.5px solid #d1fae5;
    border-radius: 14px;
    padding: 16px 20px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Sora', sans-serif !important;
    font-size: 12px !important;
    color: #6b7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #111827 !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border: 0.5px solid #d1fae5 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Success / error / info ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
}
.stSuccess {
    background: #d1fae5 !important;
    border: 0.5px solid #a7f3d0 !important;
    color: #065f46 !important;
    border-radius: 12px !important;
}
.stError {
    background: #fee2e2 !important;
    border: 0.5px solid #fca5a5 !important;
    color: #991b1b !important;
    border-radius: 12px !important;
}

/* ── Dividers ── */
hr {
    border-color: #d1fae5 !important;
    margin: 16px 0 !important;
}

/* ── Sidebar bottom action buttons ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.8) !important;
    border: 0.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    text-align: left !important;
    margin-bottom: 6px !important;
    transition: background 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    color: #fff !important;
}
/* Logout button — red tint */
[data-testid="stSidebar"] .stButton:last-child > button {
    background: rgba(239,68,68,0.15) !important;
    border-color: rgba(239,68,68,0.3) !important;
    color: #fca5a5 !important;
}
[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(239,68,68,0.25) !important;
    color: #fff !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Tabs (Sign In / Sign Up) ── */
[data-testid="stTabs"] {
    border: none !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1.5px solid #d1fae5 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 24px !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #0f766e !important;
    border-bottom: 2px solid #0f766e !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: #0f766e !important;
    height: 2px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data(ttl=1)
def load_data():
    users = pd.read_csv(csv_path("users.csv"))
    loans = pd.read_csv(csv_path("loans.csv"))
    wallet = pd.read_csv(csv_path("wallet.csv"))
    transactions = pd.read_csv(csv_path("transactions.csv"))
    return users, loans, wallet, transactions

users, loans, wallet, transactions = load_data()

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# -------------------------
# LOGIN / SIGNUP PAGE
# -------------------------
if not st.session_state.logged_in:
    col_left, col_mid, col_right = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("""
        <div style="text-align:center;padding:48px 0 28px;">
            <div style="font-family:'Sora',sans-serif;font-size:28px;font-weight:600;color:#0f766e;">Qard-e-Hasan</div>
            <div style="font-size:13px;color:#6b7280;margin-top:6px;letter-spacing:0.3px;">Interest-Free Finance Platform</div>
        </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_signup = st.tabs(["Sign In", "Sign Up"])

        # ── SIGN IN ──
        with tab_signin:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:500;color:#374151;margin-bottom:4px;'>Username</div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", key="login_user", label_visibility="collapsed")
            st.markdown("<div style='font-size:13px;font-weight:500;color:#374151;margin-bottom:4px;margin-top:12px;'>Password</div>", unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass", label_visibility="collapsed")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Sign In", key="btn_signin"):
                u = users[(users['username'] == username) & (users['password'] == password)]
                if not u.empty:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            st.markdown("""
            <div style="margin-top:20px;font-size:12px;color:#6b7280;text-align:center;">
                Sharia-compliant &nbsp;·&nbsp; Zero Interest &nbsp;·&nbsp; Trusted Finance
            </div>
            """, unsafe_allow_html=True)

        # ── SIGN UP ──
        with tab_signup:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;font-weight:500;color:#374151;margin-bottom:4px;'>Username</div>", unsafe_allow_html=True)
            new_username = st.text_input("Username", placeholder="Choose a username", key="reg_user", label_visibility="collapsed")
            st.markdown("<div style='font-size:13px;font-weight:500;color:#374151;margin-bottom:4px;margin-top:12px;'>Password</div>", unsafe_allow_html=True)
            new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_pass", label_visibility="collapsed")
            st.markdown("<div style='font-size:13px;font-weight:500;color:#374151;margin-bottom:4px;margin-top:12px;'>Confirm Password</div>", unsafe_allow_html=True)
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="reg_confirm", label_visibility="collapsed")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Create Account", key="btn_signup"):
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif new_username in users['username'].values:
                    st.error("Username already exists. Please choose another.")
                else:
                    new_id = int(users['user_id'].max()) + 1 if not users.empty else 1
                    new_user_row = {"user_id": new_id, "username": new_username, "password": new_password, "role": "user"}
                    users.loc[len(users)] = new_user_row
                    safe_save(users, "users.csv")

                    new_wallet_row = {"username": new_username, "balance": 0}
                    wallet_df = pd.read_csv(csv_path("wallet.csv"))
                    wallet_df.loc[len(wallet_df)] = new_wallet_row
                    safe_save(wallet_df, "wallet.csv")

                    st.success("Account created successfully. Please sign in.")
            st.markdown("""
            <div style="margin-top:20px;font-size:12px;color:#6b7280;text-align:center;">
                By registering you agree to our interest-free lending terms.
            </div>
            """, unsafe_allow_html=True)

    st.stop()

# -------------------------
# SIDEBAR — logged in
# -------------------------
with st.sidebar:
    initials = st.session_state.user[:2].upper()
    st.markdown(f"""
    <div style="padding:20px 16px 0;">
        <div style="font-family:'Sora',sans-serif;font-size:20px;font-weight:600;color:#fff;letter-spacing:-0.5px;">Qard-e-Hasan</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.5);letter-spacing:0.5px;text-transform:uppercase;margin-bottom:16px;">Interest-Free Finance</div>
        <div style="background:rgba(255,255,255,0.08);border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:32px;height:32px;border-radius:50%;background:#14b8a6;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:#fff;">{initials}</div>
            <div>
                <div style="font-size:13px;font-weight:500;color:#fff;">{st.session_state.user.capitalize()}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.5);">Member</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["◈  Dashboard", "✦  Apply Loan", "◉  Wallet", "≡  Transactions"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:0 0 10px 0;'>", unsafe_allow_html=True)

    if st.button("Admin Panel", key="btn_admin"):
        st.session_state.go_admin = True

    if st.button("Logout", key="btn_logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.go_admin = False
        st.rerun()

# Determine active page
if st.session_state.get("go_admin"):
    page = "Admin"
else:
    st.session_state.go_admin = False
    page = menu.split("  ", 1)[1].strip()

# Reload fresh data each render
users = pd.read_csv(csv_path("users.csv"))
loans = pd.read_csv(csv_path("loans.csv"))
wallet = pd.read_csv(csv_path("wallet.csv"))
transactions = pd.read_csv(csv_path("transactions.csv"))

user_wallet = wallet[wallet['username'] == st.session_state.user]
user_loans = loans[loans['username'] == st.session_state.user]
user_txn = transactions[transactions['username'] == st.session_state.user]

balance = int(user_wallet['balance'].values[0]) if not user_wallet.empty else 0

# -------------------------
# DASHBOARD
# -------------------------
if page == "Dashboard":
    import plotly.express as px
    import plotly.graph_objects as go

    name = st.session_state.user.capitalize()
    st.markdown(f"""
    <div style="margin-bottom:6px;">
        <span style="font-family:'Sora',sans-serif;font-size:24px;font-weight:600;color:#0f766e;">Dashboard</span>
    </div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:24px;">Welcome, {name}. Here is your financial overview.</div>
    """, unsafe_allow_html=True)

    active_loans   = len(user_loans[user_loans['status'] == 'Approved'])
    pending_loans  = len(user_loans[user_loans['status'] == 'Pending'])
    total_borrowed = int(user_loans['amount'].sum()) if not user_loans.empty else 0
    total_txn      = len(user_txn)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Wallet Balance",      f"PKR {balance:,}")
    c2.metric("Total Borrowed",      f"PKR {total_borrowed:,}")
    c3.metric("Active Loans",        active_loans)
    c4.metric("Total Transactions",  total_txn)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Row 1: Transaction trend + Loan status ──
    chart_col1, chart_col2 = st.columns([1.6, 1])

    with chart_col1:
        st.markdown("""
        <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:4px;">Transaction Activity</div>
            <div style="font-size:12px;color:#6b7280;margin-bottom:12px;">Monthly inflow vs outflow</div>
        """, unsafe_allow_html=True)

        if not user_txn.empty:
            txn_df = user_txn.copy()
            txn_df['date'] = pd.to_datetime(txn_df['date'], errors='coerce')
            txn_df['month'] = txn_df['date'].dt.to_period('M').astype(str)
            txn_df['direction'] = txn_df['type'].apply(
                lambda t: 'Inflow' if t.lower() in ['deposit', 'credit', 'disbursement'] else 'Outflow'
            )
            grouped = txn_df.groupby(['month', 'direction'])['amount'].sum().reset_index()
            fig_bar = px.bar(
                grouped, x='month', y='amount', color='direction',
                color_discrete_map={'Inflow': '#0d9488', 'Outflow': '#f87171'},
                barmode='group', labels={'amount': 'PKR', 'month': '', 'direction': ''}
            )
            fig_bar.update_layout(
                margin=dict(l=0, r=0, t=0, b=0), height=220,
                plot_bgcolor='#fff', paper_bgcolor='#fff',
                font=dict(family='Sora', size=12, color='#374151'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#f0fdf9', showgrid=True)
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='font-size:13px;color:#6b7280;padding:16px 0;'>No transaction data available.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown("""
        <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:4px;">Loan Status</div>
            <div style="font-size:12px;color:#6b7280;margin-bottom:12px;">Breakdown by status</div>
        """, unsafe_allow_html=True)

        if not user_loans.empty:
            status_counts = user_loans['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            color_map = {'Approved': '#0d9488', 'Pending': '#f59e0b', 'Rejected': '#ef4444'}
            fig_pie = px.pie(
                status_counts, names='status', values='count',
                color='status', color_discrete_map=color_map, hole=0.55
            )
            fig_pie.update_traces(textposition='outside', textinfo='percent+label',
                                  marker=dict(line=dict(color='#fff', width=2)))
            fig_pie.update_layout(
                margin=dict(l=0, r=0, t=0, b=0), height=220,
                paper_bgcolor='#fff', showlegend=False,
                font=dict(family='Sora', size=12, color='#374151')
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='font-size:13px;color:#6b7280;padding:16px 0;'>No loan data available.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 2: Cumulative balance + Recent transactions ──
    chart_col3, chart_col4 = st.columns([1.6, 1])

    with chart_col3:
        st.markdown("""
        <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:4px;">Cumulative Balance Over Time</div>
            <div style="font-size:12px;color:#6b7280;margin-bottom:12px;">Running wallet balance across transactions</div>
        """, unsafe_allow_html=True)

        if not user_txn.empty:
            bal_df = user_txn.copy()
            bal_df['date'] = pd.to_datetime(bal_df['date'], errors='coerce')
            bal_df = bal_df.sort_values('date')
            bal_df['signed'] = bal_df.apply(
                lambda r: r['amount'] if r['type'].lower() in ['deposit', 'credit', 'disbursement'] else -r['amount'], axis=1
            )
            bal_df['cumulative'] = bal_df['signed'].cumsum()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=bal_df['date'], y=bal_df['cumulative'],
                mode='lines+markers', line=dict(color='#0d9488', width=2.5),
                marker=dict(color='#0d9488', size=6),
                fill='tozeroy', fillcolor='rgba(13,148,136,0.08)'
            ))
            fig_line.update_layout(
                margin=dict(l=0, r=0, t=0, b=0), height=200,
                plot_bgcolor='#fff', paper_bgcolor='#fff',
                font=dict(family='Sora', size=12, color='#374151'),
                xaxis=dict(showgrid=False, title=''),
                yaxis=dict(gridcolor='#f0fdf9', title='PKR')
            )
            st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("<div style='font-size:13px;color:#6b7280;padding:16px 0;'>No data to display.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col4:
        st.markdown("""
        <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:16px;">Recent Transactions</div>
        """, unsafe_allow_html=True)

        if user_txn.empty:
            st.markdown("<div style='font-size:13px;color:#6b7280;padding:8px 0;'>No transactions yet.</div>", unsafe_allow_html=True)
        else:
            for _, row in user_txn.tail(5).iterrows():
                is_in = row['type'].lower() in ['deposit', 'credit', 'disbursement']
                dot_bg      = "#d1fae5" if is_in else "#fee2e2"
                arrow       = "↓" if is_in else "↑"
                amount_color = "#059669" if is_in else "#dc2626"
                sign        = "+" if is_in else "−"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:0.5px solid #f3f4f6;">
                    <div style="width:30px;height:30px;border-radius:50%;background:{dot_bg};display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;">{arrow}</div>
                    <div style="flex:1;">
                        <div style="font-size:12px;font-weight:500;color:#111827;">{row['type'].capitalize()}</div>
                        <div style="font-size:11px;color:#6b7280;">{row['date']}</div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:500;color:{amount_color};">{sign}{int(row['amount']):,}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# APPLY LOAN
# -------------------------
elif page == "Apply Loan":
    st.markdown("""
    <div style="font-family:'Sora',sans-serif;font-size:24px;font-weight:600;color:#0f766e;margin-bottom:6px;">Apply for a Loan</div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:24px;">Submit a Qard-e-Hasan application — interest-free, always.</div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("""
        <div style="background:#f0fdf9;border:0.5px solid #a7f3d0;border-radius:10px;padding:12px 16px;margin-bottom:20px;">
            <div style="font-size:12px;color:#065f46;font-weight:500;">Zero interest &nbsp;·&nbsp; Sharia-compliant &nbsp;·&nbsp; Flexible repayment</div>
        </div>
        """, unsafe_allow_html=True)

        amount = st.number_input("Loan Amount (PKR)", min_value=1000, step=500, value=5000)
        duration = st.selectbox("Repayment Duration", [3, 6, 12], format_func=lambda x: f"{x} months")
        purpose = st.text_input("Purpose (optional)", placeholder="e.g. Medical, Education, Business")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Submit Application →"):
            new_loan = {
                "loan_id": len(loans) + 1,
                "username": st.session_state.user,
                "amount": amount,
                "duration": duration,
                "status": "Pending"
            }
            loans.loc[len(loans)] = new_loan
            safe_save(loans, "loans.csv")
            st.success(f"Application submitted — PKR {amount:,} for {duration} months")

# -------------------------
# WALLET
# -------------------------
elif page == "Wallet":
    st.markdown("""
    <div style="font-family:'Sora',sans-serif;font-size:24px;font-weight:600;color:#0f766e;margin-bottom:6px;">My Wallet</div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:24px;">Manage your Qard-e-Hasan balance.</div>
    """, unsafe_allow_html=True)

    name = st.session_state.user.capitalize()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f766e,#14b8a6);border-radius:18px;padding:28px 32px;color:#fff;position:relative;overflow:hidden;margin-bottom:24px;max-width:480px;">
        <div style="font-size:12px;color:rgba(255,255,255,0.7);letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;">Available Balance</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:36px;font-weight:600;">PKR {balance:,}</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px;">Last updated: {datetime.now().strftime('%d %b %Y')}</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:16px;">{name} · Member Account</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;max-width:480px;">
        <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:14px;">Wallet Details</div>
    """, unsafe_allow_html=True)

    rows = [
        ("Account holder", name),
        ("Account type", "Qard-e-Hasan"),
        ("Current balance", f"PKR {balance:,}"),
    ]
    for label, val in rows:
        is_balance = label == "Current balance"
        val_style = "font-family:'JetBrains Mono',monospace;font-weight:600;color:#0f766e;" if is_balance else "font-weight:500;"
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:9px 0;border-bottom:0.5px solid #f3f4f6;font-size:13px;">
            <span style="color:#6b7280;">{label}</span>
            <span style="{val_style}">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# TRANSACTIONS
# -------------------------
elif page == "Transactions":
    st.markdown("""
    <div style="font-family:'Sora',sans-serif;font-size:24px;font-weight:600;color:#0f766e;margin-bottom:6px;">Transactions</div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:24px;">Your complete transaction history.</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#374151;">All Transactions</div>
            <div style="font-size:12px;color:#6b7280;">{len(user_txn)} records</div>
        </div>
    """, unsafe_allow_html=True)

    if user_txn.empty:
        st.markdown("<div style='font-size:13px;color:#6b7280;padding:8px 0;'>No transactions found.</div>", unsafe_allow_html=True)
    else:
        for _, row in user_txn.iterrows():
            is_in = row['type'].lower() in ['deposit', 'credit', 'disbursement']
            dot_bg = "#d1fae5" if is_in else "#fee2e2"
            arrow = "↓" if is_in else "↑"
            amount_color = "#059669" if is_in else "#dc2626"
            sign = "+" if is_in else "−"
            txn_id = f"TXN-{int(row['txn_id']):03d}" if 'txn_id' in row else ""
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:0.5px solid #f3f4f6;">
                <div style="width:36px;height:36px;border-radius:50%;background:{dot_bg};display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">{arrow}</div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:500;color:#111827;">{row['type'].capitalize()}</div>
                    <div style="font-size:11px;color:#6b7280;margin-top:2px;">{row['date']} · {txn_id}</div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:500;color:{amount_color};">{sign} PKR {int(row['amount']):,}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# ADMIN
# -------------------------
elif page == "Admin":
    st.markdown("""
    <div style="font-family:'Sora',sans-serif;font-size:24px;font-weight:600;color:#0f766e;margin-bottom:6px;">Admin Panel</div>
    <div style="font-size:13px;color:#6b7280;margin-bottom:24px;">Review and approve loan applications.</div>
    """, unsafe_allow_html=True)

    total = len(loans)
    pending = len(loans[loans['status'] == 'Pending'])
    approved = len(loans[loans['status'] == 'Approved'])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Applications", total)
    c2.metric("Pending Review", pending)
    c3.metric("Approved", approved)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff;border:0.5px solid #d1fae5;border-radius:14px;padding:20px 24px;">
        <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:16px;">Loan Applications</div>
    """, unsafe_allow_html=True)

    for _, row in loans.iterrows():
        status = row['status']
        if status == 'Approved':
            pill_bg, pill_color = "#d1fae5", "#065f46"
        elif status == 'Pending':
            pill_bg, pill_color = "#fef3c7", "#92400e"
        else:
            pill_bg, pill_color = "#fee2e2", "#991b1b"

        col_info, col_amt, col_status, col_action = st.columns([3, 2, 1.5, 1.5])
        with col_info:
            st.markdown(f"""
            <div style="padding:10px 0;">
                <div style="font-size:13px;font-weight:500;color:#111827;">#{int(row['loan_id']):03d} · {row['username']}</div>
                <div style="font-size:11px;color:#6b7280;margin-top:2px;">{row['duration']} months</div>
            </div>
            """, unsafe_allow_html=True)
        with col_amt:
            st.markdown(f"""
            <div style="padding:10px 0;font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600;color:#111827;">
                PKR {int(row['amount']):,}
            </div>
            """, unsafe_allow_html=True)
        with col_status:
            st.markdown(f"""
            <div style="padding:10px 0;">
                <span style="font-size:11px;font-weight:600;padding:4px 10px;border-radius:20px;background:{pill_bg};color:{pill_color};">{status}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_action:
            if status == 'Pending':
                if st.button("Approve", key=f"approve_{row['loan_id']}"):
                    loans.loc[loans['loan_id'] == row['loan_id'], 'status'] = "Approved"
                    safe_save(loans, "loans.csv")

                    amt = row['amount']
                    user = row['username']
                    wallet.loc[wallet['username'] == user, 'balance'] += amt
                    safe_save(wallet, "wallet.csv")
                    st.success(f"Loan #{int(row['loan_id']):03d} approved. PKR {int(amt):,} credited to account.")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)