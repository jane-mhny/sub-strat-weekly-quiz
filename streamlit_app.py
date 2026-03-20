import streamlit as st
import pandas as pd
import json

# --- 1. SET UP THE APP BASICS ---
st.set_page_config(page_title="Team Metrics Quiz", page_icon="🏆")
st.title("🏆 Weekly Team Metrics Quiz")

# This creates a "memory" for the app so scores don't disappear when the page refreshes
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = {}
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None

# --- 2. ADMIN SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Admin Panel")
    password = st.text_input("Admin Password", type="password")
    
    if password == "metrics2026": # You can change this "password" to whatever you want!
        st.success("Admin Access Granted")
        
        # Upload New Quiz
        uploaded_file = st.file_uploader("Upload Weekly JSON Quiz", type=['json'])
        if uploaded_file is not None:
            raw_data = json.load(uploaded_file)
            if isinstance(raw_data, str):
                st.session_state.quiz_data = json.loads(raw_data)
            else:
                st.session_state.quiz_data = raw_data
            st.info("New Quiz Loaded!")

        # Reset Leaderboard
        if st.button("🚨 Reset All Scores"):
            st.session_state.leaderboard = {}
            st.rerun()
    else:
        st.warning("Enter password to upload quizzes.")

# --- 3. THE QUIZ INTERFACE ---
if st.session_state.quiz_data is None:
    st.info("👋 Welcome! Waiting for the Admin to upload this week's quiz...")
else:
    team_name = st.text_input("Enter your Team Name to begin:", "")

    if team_name:
        st.divider()
        score = 0
        # This handles the specific "folder" structure in your JSON
        quiz_list = st.session_state.quiz_data[0]['questions']
        
        with st.form("quiz_form"):
            for i, q in enumerate(quiz_list):
                st.write(f"**Q{i+1}: {q['question']}**")
                # We show the options text directly
                answer = st.radio("Select an answer:", q['options'], key=f"q{i}")
                if answer == q['answer']:
                    score += 1
            
            submitted = st.form_submit_button("Submit Results")
            
            if submitted:
                st.session_state.leaderboard[team_name] = score
                st.balloons()
                st.success(f"Great job {team_name}! You scored {score}/{len(quiz_list)}")

# --- 4. THE LEADERBOARD ---
st.divider()
st.header("📊 Current Leaderboard")
if st.session_state.leaderboard:
    # Turns the scores into a nice table
    df = pd.DataFrame(list(st.session_state.leaderboard.items()), columns=['Team', 'Score'])
    df = df.sort_values(by='Score', ascending=False)
    st.table(df)
else:
    st.write("No scores yet. Be the first!")
