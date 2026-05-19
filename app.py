import streamlit as st
import pandas as pd
from database import conn, cursor

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Goal Tracker", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ---------------- KPI CARD ----------------
def kpi_card(title, value, color="#1F6FEB"):
    st.markdown(f"""
    <div style="
        background:white;
        border:1px solid #D6E6FF;
        padding:16px;
        border-radius:14px;
        text-align:center;
        box-shadow:0px 2px 8px rgba(0,0,0,0.05);
    ">
        <h4 style="color:{color}; margin:0;">{title}</h4>
        <h2 style="margin:5px 0; color:#0B1F3A;">{value}</h2>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #F5F9FF !important;
    color: #0B1F3A !important;
}

section[data-testid="stSidebar"] {
    background-color: #DCEBFF !important;
}

h1,h2,h3 {
    color:#1F6FEB !important;
}

.stButton > button {
    background:#1F6FEB !important;
    color:white !important;
    border-radius:10px !important;
}

.block {
    background:white;
    border:1px solid #D6E6FF;
    padding:12px;
    border-radius:12px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LANDING PAGE ----------------
if not st.session_state.logged_in:

    st.title("🎯 Goal Tracking System")

    st.markdown("""
    <div style="text-align:center;padding:30px;background:white;border-radius:12px;border:1px solid #D6E6FF;">
        <h1>Welcome to Goal Tracker</h1>
        <p>Employee Goals • Manager Tracking • Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI CARDS (FEATURE SHOWCASE)
    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("Goal Management", "Create & Track")

    with col2:
        kpi_card("Manager Review", "Approve & Return")

    with col3:
        kpi_card("Quarter System", "Q1–Q4 Tracking")

    # LOGIN
    st.sidebar.header("Login")

    with st.sidebar.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        cursor.execute("""
        SELECT * FROM employees
        WHERE name=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.rerun()
        else:
            st.error("Wrong credentials")

# ---------------- LOGGED IN ----------------
if st.session_state.logged_in:

    st.sidebar.write(f"👤 {st.session_state.username}")
    st.sidebar.write(f"🎭 {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    role = st.session_state.role.lower()

    # =====================================================
    # EMPLOYEE (UNCHANGED LOGIC + KPI ADDED)
    # =====================================================
    if role == "employee":

        st.header("👨‍💼 Employee Dashboard")

        # ---------------- KPI ----------------
        cursor.execute("SELECT COUNT(*) FROM goals WHERE employee_name=?",
                       (st.session_state.username,))
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM goals WHERE employee_name=? AND approved=1",
                       (st.session_state.username,))
        approved = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM goals WHERE employee_name=? AND approved=0",
                       (st.session_state.username,))
        pending = cursor.fetchone()[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            kpi_card("Total Goals", total)

        with col2:
            kpi_card("Approved", approved, "#2EA043")

        with col3:
            kpi_card("Pending", pending, "#D29922")

        st.divider()

        # ---------------- CREATE GOAL ----------------
        st.subheader("Create Goal")

        if total >= 8:
            st.error("Max 8 goals allowed")
            st.stop()

        with st.form("goal_form"):
            title = st.text_input("Goal Title")
            target = st.number_input("Target", min_value=0)
            weight = st.number_input("Weightage", 10, 100)
            submit = st.form_submit_button("Add Goal")

        if submit:
            cursor.execute("""
            INSERT INTO goals (employee_name, title, target, weightage)
            VALUES (?, ?, ?, ?)
            """, (st.session_state.username, title, target, weight))
            conn.commit()
            st.success("Goal added")
            st.rerun()

        # ---------------- TABLE ----------------
        st.subheader("📊 My Goals")

        cursor.execute("""
        SELECT id, title, target, weightage,
               q1_status, q2_status, q3_status, q4_status
        FROM goals
        WHERE employee_name=?
        """, (st.session_state.username,))

        goals = cursor.fetchall()

        data = []
        for g in goals:
            data.append([g[0], g[1], g[4], g[5], g[6], g[7]])

        df = pd.DataFrame(data, columns=["ID", "Goal", "Q1", "Q2", "Q3", "Q4"])
        st.dataframe(df, use_container_width=True)

        # ---------------- UPDATE ----------------
        st.subheader("Update Quarterly Status")

        if goals:
            goal_map = {g[0]: g[1] for g in goals}

            gid = st.selectbox("Select Goal", list(goal_map.keys()),
                               format_func=lambda x: f"{x} - {goal_map[x]}")

            quarter = st.selectbox("Quarter",
                                   ["q1_status", "q2_status", "q3_status", "q4_status"])

            status = st.selectbox("Status",
                                  ["Not Started", "On Track", "Completed"])

            if st.button("Save Update"):
                cursor.execute(f"""
                UPDATE goals
                SET {quarter}=?
                WHERE id=?
                """, (status, gid))
                conn.commit()
                st.success("Updated")

        # ---------------- CARDS ----------------
        st.subheader("Goal Cards")

        for g in goals:
            st.markdown(f"""
            <div class="block">
                <b>{g[1]}</b><br>
                Q1: {g[4]} | Q2: {g[5]} | Q3: {g[6]} | Q4: {g[7]}
            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # MANAGER (FULL RESTORED + KPI ADDED)
    # =====================================================
    elif role == "manager":

        st.header("👨‍💼 Manager Dashboard")

        cursor.execute("""
        SELECT name FROM employees
        WHERE manager_name=?
        """, (st.session_state.username,))

        team = cursor.fetchall()

        if not team:
            st.warning("No team assigned")
            st.stop()

        # ---------------- KPI ----------------
        team_size = len(team)
        total_goals = 0
        approved = 0

        for t in team:
            emp = t[0]

            cursor.execute("SELECT COUNT(*), SUM(approved) FROM goals WHERE employee_name=?",
                           (emp,))
            r = cursor.fetchone()

            total_goals += r[0] or 0
            approved += r[1] or 0

        approval_rate = round((approved / total_goals) * 100, 2) if total_goals else 0

        col1, col2, col3 = st.columns(3)

        with col1:
            kpi_card("Team Size", team_size)

        with col2:
            kpi_card("Total Goals", total_goals, "#D29922")

        with col3:
            kpi_card("Approval %", f"{approval_rate}%", "#2EA043")

        st.divider()

        # ---------------- TEAM VIEW (RESTORED) ----------------
        st.subheader("Team Goals Overview")

        for t in team:

            emp = t[0]
            st.markdown(f"## 👤 {emp}")

            cursor.execute("""
            SELECT * FROM goals
            WHERE employee_name=?
            """, (emp,))

            goals = cursor.fetchall()

            if not goals:
                st.info("No goals submitted")
                continue

            for g in goals:

                with st.expander(f"🎯 {g[2]} (ID: {g[0]})"):

                    st.write("Target:", g[3])
                    st.write("Weight:", g[4])
                    st.write("Status:", "Approved" if g[5] else "Pending")

                    if g[5] == 0:

                        comment = st.text_input("Manager Comment", key=f"c{g[0]}")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            if st.button(f"Save {g[0]}"):
                                cursor.execute("""
                                UPDATE goals
                                SET manager_comments=?
                                WHERE id=?
                                """, (comment, g[0]))
                                conn.commit()

                        with col2:
                            if st.button(f"Approve {g[0]}"):
                                cursor.execute("""
                                UPDATE goals
                                SET approved=1, locked=1
                                WHERE id=?
                                """, (g[0],))
                                conn.commit()

                        with col3:
                            if st.button(f"Return {g[0]}"):
                                cursor.execute("""
                                UPDATE goals
                                SET approved=0, locked=0
                                WHERE id=?
                                """, (g[0],))
                                conn.commit()

                    else:
                        st.success("Locked")