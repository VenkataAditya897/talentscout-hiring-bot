import streamlit as st
import sqlite3
import pandas as pd
import os
import shutil
import os
import tempfile
# Adjust this path if your DB is elsewhere
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'candidates.db')

def load_candidates():
    conn = sqlite3.connect(DB_PATH)
    candidates_df = pd.read_sql_query("SELECT * FROM candidates", conn)
    conn.close()
    return candidates_df

def load_questions():
    conn = sqlite3.connect(DB_PATH)
    questions_df = pd.read_sql_query("SELECT * FROM candidate_questions", conn)
    conn.close()
    return questions_df

def load_answers():
    conn = sqlite3.connect(DB_PATH)
    answers_df = pd.read_sql_query("SELECT * FROM candidate_answers", conn)
    conn.close()
    return answers_df

def load_merged_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        c.id AS candidate_id,
        c.full_name,
        c.email,
        c.phone,
        c.experience,
        c.position,
        c.location,
        c.tech_stack,
        c.timestamp AS candidate_timestamp,
        q.id AS question_id,
        q.question,
        a.answer,
        a.timestamp AS answer_timestamp
    FROM candidates c
    LEFT JOIN candidate_questions q ON c.id = q.candidate_id
    LEFT JOIN candidate_answers a ON c.id = a.candidate_id AND q.question = a.question
    ORDER BY c.id, q.id
    """
    merged_df = pd.read_sql_query(query, conn)
    conn.close()
    return merged_df

st.title("🎯 TalentScout Admin Dashboard")

candidates_df = load_candidates()
questions_df = load_questions()
answers_df = load_answers()
merged_df = load_merged_data()

st.subheader("Candidates")
st.dataframe(candidates_df)


st.subheader("Merged Candidate Data")
st.dataframe(merged_df)

# Export CSV for each table
st.markdown("---")
st.header("Export Data to CSV")

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv_candidates = convert_df(candidates_df)
csv_merged = convert_df(merged_df)

st.download_button(
    label="Download Candidates CSV",
    data=csv_candidates,
    file_name='candidates.csv',
    mime='text/csv',
)



st.download_button(
    label="Download Merged Data CSV",
    data=csv_merged,
    file_name='merged_candidate_data.csv',
    mime='text/csv',
)
