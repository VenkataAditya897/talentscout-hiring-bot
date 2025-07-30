
# 🤖 TalentScout Hiring Assistant

An AI-powered chatbot built with Streamlit for intelligent candidate screening and technical evaluation, created as part of the **AI/ML Internship Assignment** for TalentScout.

---

## 🧠 Project Overview

**TalentScout Hiring Assistant** is a conversational AI that:
- Greets candidates and collects essential hiring details (name, email, etc.).
- Dynamically generates technical questions based on the declared tech stack.
- Stores user data and responses securely in a local SQLite database.
- Handles exit phrases gracefully and ensures conversation quality.

This tool simulates an initial round of candidate screening using LLMs.

---

## 📦 Features

- Clean Streamlit UI for seamless user interaction
- Input validation and polite fallback prompts
- Custom LLM prompts to generate tech-specific questions
- Conversation context tracking
- SQLite storage with masked sensitive info
- Admin dashboard for reviewing/exporting candidate data

---
## 🚀 Live Demo

🌐 Try the AI Hiring Assistant:
**[Live Streamlit App](https://talentscout-hiring-bot-venkata-aditya-gopalapuram.streamlit.app/)**  
Interact with the bot as a candidate and experience the automated interview process.

> 🔒 **Note:** The recruiter/admin dashboard (`admin_view.py`) is not deployed online.  

---

## 🖥️ Installation Instructions

### 1. Clone this Repository
```bash
git clone https://github.com/yourusername/talentscout-hiring-bot.git
cd talentscout-hiring-bot
```

### 2. Create a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app/main.py
```

### 5. Admin Dashboard (Export CSV)
```bash
streamlit run app/admin_view.py
```

---

## 📄 Usage Guide

### 🎙️ Candidate Flow
1. Click **"Start Interview"**.
2. Answer clearly (e.g., `John Doe`, `Python, React` — no full sentences).
3. Receive 3–5 technical questions tailored to your tech stack.
4. Exit at any time using phrases like `exit`, `thank you`, `stop`, etc.

### 📊 Admin Flow
- View saved candidate info, tech stack, and answers.
- Download CSVs for candidates, questions, and answers via buttons.

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Streamlit** – UI interface
- **SQLite** – Local data storage
- **LangChain + Groq API** – LLM-based question generation
- **Pandas** – Data handling and export

---

## 🧠 Prompt Design

Prompts are carefully structured to:
- Ask for direct answers only (no extra fluff like “My name is...”).
- Generate tech questions per declared tech (e.g., Python, Django).
- Validate and fallback when inputs are unclear.

---

## 🔐 Data Privacy & Security

- Data is saved locally in SQLite DB under `data/` directory.
- GDPR-safe for simulated interviews.

---


## 👨‍💻 Author

**Venkata Aditya Gopalapuram**  
Email: [venkataaditya897@gmail.com](mailto:venkataaditya897@gmail.com)  
GitHub: [@VenkataAditya897](https://github.com/VenkataAditya897)

---

