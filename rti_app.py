import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Multi-Standard RTI Tracker",
    page_icon="📊",
    layout="wide"
)

# --- PRE-LOADED RTI PLAN TEMPLATES ---
PLAN_TEMPLATES = {
    "TEKS 1.3.D / CCSS 1.0A.C.6 - Fact Strategies within 20": {
        "standard": "TEKS 1.3.D / CCSS 1.0A.C.6",
        "subject": "Math",
        "condition": "Addition & subtraction expressions within 20 (ten-frames, number bonds, cards)",
        "behavior": "apply basic fact strategies (including making 10, decomposing to 10, and doubles/near doubles) to solve accurately",
        "benchmarks": [
            "Benchmark 1: Make 10 (Addition) with addends 7, 8, 9",
            "Benchmark 2: Decompose to 10 (Subtraction) with minuends 11-19",
            "Benchmark 3: Flexible Fact Fluency within 20"
        ],
        "strategies": ["Make 10 (Add)", "Decompose to 10 (Sub)", "Doubles / Near Doubles", "Mixed Strategies"],
        "error_types": [
            "None / Independent",
            "Combinations to 10 Error (Forgot 10-partner)",
            "Incorrect Decomposition (Split number wrong)",
            "Bridge Lost Step (Forgot remaining part)",
            "Operation Sign Error (Added instead of subtracted)",
            "Counting on 1s Fallback (Finger counting)"
        ]
    },
    "TEKS 1.5.B / CCSS 1.NBT.A.1 - Skip Counting to 120": {
        "standard": "TEKS 1.5.B / CCSS 1.NBT.A.1",
        "subject": "Math",
        "condition": "Sets up to 120 concrete objects or pictorial representations grouped in sets of 2, 5, or 10",
        "behavior": "skip count by twos, fives, and tens to determine the correct total quantity",
        "benchmarks": [
            "Benchmark 1: Tens to 120 (base-ten rods, filled 10-frames)",
            "Benchmark 2: Fives to 120 (tallies, nickels, 5-frame arrays)",
            "Benchmark 3: Twos to 120 (paired items, dot-strips)"
        ],
        "strategies": ["Skip Count 10s", "Skip Count 5s", "Skip Count 2s", "Mixed Intervals"],
        "error_types": [
            "None / Independent",
            "Pattern Switch Error (Switches interval mid-count)",
            "Rote Sequence Error (Misses number in sequence)",
            "Tracking Error (Counts group twice or skips)",
            "Century Bridge Error (Stumbles crossing 100)",
            "Group Size Misidentification"
        ]
    },
    "TEKS ELAR 2.2.A.iv / CCSS RF.2.3 - Phoneme Manipulation": {
        "standard": "TEKS ELAR 2.2.A.iv / CCSS RF.2.3",
        "subject": "ELAR",
        "condition": "Spoken single-syllable words (CVC, CCVC, CVCC) presented orally without visual print",
        "behavior": "orally add, delete, and substitute initial, final, and medial phonemes to produce the correct new word",
        "benchmarks": [
            "Benchmark 1: Add or delete initial and final phonemes in CVC/CCVC words",
            "Benchmark 2: Delete or substitute medial vowel sounds",
            "Benchmark 3: Rapid 3-step phoneme chaining across all positions"
        ],
        "strategies": ["Phoneme Addition", "Phoneme Deletion", "Phoneme Substitution", "Medial Vowel Swap / Chaining"],
        "error_types": [
            "None / Independent",
            "Co-articulation / Blending Error",
            "Vowel Quality Shift (Alters short/long sound)",
            "Positional Confusion (Initial vs Final/Medial)",
            "Auditory Memory Overload",
            "Incomplete Cluster Split (Deletes full blend)"
        ]
    }
}

# --- INITIALIZE SESSION STATE ---
if "plans" not in st.session_state:
    st.session_state.plans = PLAN_TEMPLATES.copy()

if "students" not in st.session_state:
    st.session_state.students = {}

# --- SIDEBAR: NAVIGATION & SETUP ---
st.sidebar.title("📊 RTI Multi-Plan Manager")

# 1. Select Active Plan Template
plan_keys = list(st.session_state.plans.keys())
selected_plan_key = st.sidebar.selectbox("🎯 Select Active Plan Template:", plan_keys)
active_plan = st.session_state.plans[selected_plan_key]

st.sidebar.markdown("---")

# 2. Add New Custom Plan Template
with st.sidebar.expander("➕ Add Custom Plan Template", expanded=False):
    custom_title = st.text_input("Plan Name / Key:")
    custom_std = st.text_input("Standard Code:")
    custom_cond = st.text_area("Condition:")
    custom_beh = st.text_area("Target Behavior:")
    custom_strats = st.text_input("Strategies (comma separated):", value="Strategy 1, Strategy 2")
    custom_errors = st.text_input("Errors (comma separated):", value="None, Error A, Error B")
    
    if st.button("Save Plan Template") and custom_title:
        st.session_state.plans[custom_title] = {
            "standard": custom_std,
            "subject": "Custom",
            "condition": custom_cond,
            "behavior": custom_beh,
            "benchmarks": ["Benchmark 1", "Benchmark 2", "Benchmark 3"],
            "strategies": [s.strip() for s in custom_strats.split(",")],
            "error_types": [e.strip() for e in custom_errors.split(",")]
        }
        st.success(f"Added plan template: {custom_title}")
        st.rerun()

st.sidebar.markdown("---")

# 3. Add / Select Active Student
with st.sidebar.expander("👤 Student Roster Setup", expanded=True):
    new_student_name = st.text_input("Add New Student Name:")
    if st.button("Add Student") and new_student_name:
        if new_student_name not in st.session_state.students:
            st.session_state.students[new_student_name] = {
                "active_plan": selected_plan_key,
                "baseline": 30.0,
                "target_date": datetime.date.today() + datetime.timedelta(weeks=8),
                "logs": []
            }
            st.success(f"Added {new_student_name}!")
            st.rerun()

student_list = list(st.session_state.students.keys())
if student_list:
    selected_student = st.sidebar.selectbox("Active Student:", student_list)
    student_data = st.session_state.students[selected_student]
else:
    st.sidebar.warning("Please add a student to begin.")
    st.stop()

st.sidebar.markdown("---")

# 4. Backup & Restore Data
with st.sidebar.expander("💾 CSV Backup & Restore", expanded=False):
    all_logs = []
    for s_name, s_info in st.session_state.students.items():
        for log in s_info["logs"]:
            entry = log.copy()
            entry["Student"] = s_name
            all_logs.append(entry)
            
    if all_logs:
        export_df = pd.DataFrame(all_logs)
        csv_buffer = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Progress Data (CSV)",
            data=csv_buffer,
            file_name=f"rti_progress_all_students_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.caption("No progress logs recorded yet.")

    uploaded_file = st.file_uploader("⬆️ Restore CSV Backup", type=["csv"])
    if uploaded_file is not None:
        try:
            imported_df = pd.read_csv(uploaded_file)
            for s_name in imported_df["Student"].unique():
                if s_name not in st.session_state.students:
                    st.session_state.students[s_name] = {
                        "active_plan": selected_plan_key,
                        "baseline": 30.0,
                        "target_date": datetime.date.today() + datetime.timedelta(weeks=8),
                        "logs": []
                    }
                st.session_state.students[s_name]["logs"] = imported_df[imported_df["Student"] == s_name].to_dict('records')
            st.success("Data successfully restored!")
            st.rerun()
        except Exception:
            st.error("Error loading CSV file.")

navigation = st.sidebar.radio("Module Navigation:", ["1. SMART Goal & Plan View", "2. Progress Monitoring & Logs"])


# ==============================================================================
# MODULE 1: SMART GOAL & PLAN VIEW
# ==============================================================================
if navigation == "1. SMART Goal & Plan View":
    st.title("🎯 RTI Plan Blueprint")
    st.subheader(f"Active Plan: {selected_plan_key}")
    
    col1, col2 = st.columns(2)
    with col1:
        student_data["baseline"] = st.number_input("Baseline Accuracy (%)", min_value=0.0, max_value=100.0, value=float(student_data["baseline"]))
    with col2:
        student_data["target_date"] = st.date_input("Target Date", value=student_data["target_date"])

    st.markdown("---")
    st.markdown("### Official Individualized SMART Goal")
    st.markdown(f"""
    > **SMART Goal Statement:**  
    > By **{student_data['target_date'].strftime('%B %d, %Y')}**, when presented with **{active_plan['condition']}**, **{selected_student}** will **{active_plan['behavior']}** with **80% accuracy across 4 out of 5 consecutive progress monitoring trials**.
    """)

    st.markdown("---")
    st.markdown("### Sequential Benchmarks")
    for b in active_plan["benchmarks"]:
        st.write(f"- {b}")


# ==============================================================================
# MODULE 2: PROGRESS MONITORING & LOGS
# ==============================================================================
elif navigation == "2. Progress Monitoring & Logs":
    st.title("📈 Progress Monitoring")
    st.caption(f"Student: **{selected_student}** | Target Standard: **{active_plan['standard']}**")

    st.subheader("Record Weekly Trial Probe")
    with st.form("log_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            wk = st.number_input("Week #", min_value=1, max_value=16, value=len(student_data["logs"]) + 1)
            dt = st.date_input("Date", value=datetime.date.today())
        with c2:
            strat = st.selectbox("Focus Strategy / Sub-skill", active_plan["strategies"])
            score = st.number_input("Score Correct (out of 5)", min_value=0, max_value=5, value=4)
        with c3:
            prompt = st.selectbox("Prompt Level", ["I - Independent", "V - Verbal Prompt", "G - Gestural/Visual", "P - Physical Model"])
        with c4:
            err = st.selectbox("Primary Diagnostic Error", active_plan["error_types"])

        if st.form_submit_button("Submit Trial Data"):
            acc = (score / 5.0) * 100.0
            student_data["logs"].append({
                "Student": selected_student,
                "Standard": active_plan["standard"],
                "Week": int(wk),
                "Date": dt.strftime("%Y-%m-%d"),
                "Strategy": strat,
                "Score": f"{score}/5",
                "Accuracy": acc,
                "Prompt Level": prompt,
                "Primary Error": err
            })
            st.success("Trial logged!")
            st.rerun()

    st.markdown("---")
    st.subheader("Progress Chart & History")
    
    logs = student_data["logs"]
    if logs:
        df = pd.DataFrame(logs)
        chart_df = pd.DataFrame({
            "Week": [0] + df["Week"].tolist(),
            "Accuracy (%)": [student_data["baseline"]] + df["Accuracy"].tolist()
        }).set_index("Week")
        
        st.line_chart(chart_df)
        st.dataframe(df[["Week", "Date", "Strategy", "Score", "Accuracy", "Prompt Level", "Primary Error"]], use_container_width=True)
    else:
        st.info("No logs recorded for this student yet.")
