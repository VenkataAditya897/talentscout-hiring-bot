import streamlit as st
from streamlit_chat import message
from chat_engine import ChatEngine
from context_manager import ContextManager
import random
from data_handler import create_tables, insert_candidate, insert_questions, insert_answer  

create_tables()

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = ChatEngine()
if "context" not in st.session_state:
    st.session_state.context = ContextManager()
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []  # list of generated questions
if "current_tech_q_idx" not in st.session_state:
    st.session_state.current_tech_q_idx = 0
if "interview_complete" not in st.session_state:
    st.session_state.interview_complete = False

# UI
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("Helping you hire smarter, faster.")

fallback_phrases = [
    "Sorry, I didn't quite get that.",
    "Could you please rephrase?",
    "I’m here to help with your interview, please answer the question.",
]

st.info("🔒 Your information is stored securely and used only for recruitment simulation purposes.")

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg_{i}")

# Start chat
if not st.session_state.chat_started:
    if st.button("Start Interview"):
        field = st.session_state.context.next_field()
        st.session_state.messages.append({
        "role": "assistant",
        "content": "Please respond with only the answer — no extra sentences like 'My name is...' or 'I am from...'. Let's keep it short and clear ✅"
    })
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.context.questions[field]})
        st.session_state.chat_started = True
        st.rerun()
else:
    if user_input := st.chat_input("Type your response here..."):

        user_input_lower = user_input.lower()
        exit_keywords = ["exit", "quit", "bye", "cancel", "stop","thank you"]

        # --- Insert: Global exit keyword detection ---
        if any(kw in user_input_lower for kw in exit_keywords):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Thank you for your time! We’ll be in touch soon. 👋"
            })
            # Optionally reset chat state
            st.session_state.chat_started = False
            st.rerun()
        # --- End exit handling ---

        st.session_state.messages.append({"role": "user", "content": user_input})
        if st.session_state.interview_complete:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "The interview is already complete. We will notify you via email if there is an update."
            })
            st.rerun()

        current_field = st.session_state.context.next_field()
        if current_field:
            # Validate user input
            if st.session_state.context.validate(current_field, user_input):
                st.session_state.context.update_response(current_field, user_input)

                next_field = st.session_state.context.next_field()
                if next_field:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": st.session_state.context.questions[next_field]
                    })
                else:
                    summary = st.session_state.context.summary()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Thanks for the info! Here's a quick summary:\n\n{summary}\n\nNow, let me generate some technical questions based on your tech stack. Please answer one at a time."
                    })

                    tech_stack = st.session_state.context.responses.get("tech_stack", "")
                    # questions = st.session_state.chat_engine.generate_tech_questions(tech_stack)
                    # st.session_state.messages.append({
                    #     "role": "assistant",
                    #     "content": questions
                    # })
                    questions_text = st.session_state.chat_engine.generate_tech_questions(tech_stack)
                    questions_list = [q.strip() for q in questions_text.split('\n') if q.strip() and q[0].isdigit()]
                    st.session_state.tech_questions = questions_list
                    st.session_state.current_tech_q_idx = 0

                    # Ask first technical question
                    first_q = st.session_state.tech_questions[0]
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": first_q
                    })

                    if not st.session_state.get("interview_complete", False):
                        candidate_data = st.session_state.context.responses
                        candidate_id = insert_candidate(candidate_data)
                        st.session_state.candidate_id = candidate_id
                    # --- Phase 6: Save candidate data and questions securely ---
                    

                        st.info("🔒 Your information has been securely saved for recruitment purposes.")
                    # --- End DB handling ---

            else:
                
                # --- Insert: Fallback for invalid input with randomized polite prompts ---
                fallback_msg = random.choice(fallback_phrases)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"{fallback_msg}\n\n{st.session_state.context.questions[current_field]}"
                })
                # --- End fallback ---
        elif st.session_state.tech_questions and not st.session_state.interview_complete:
            # Current question index
            idx = st.session_state.current_tech_q_idx
            question = st.session_state.tech_questions[idx]
            answer = user_input
            insert_answer(st.session_state.candidate_id, question, answer)

            # Store candidate answer (you can extend data_handler to save answers if desired)
            # For now, just acknowledge
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Thanks for your answer to question {idx+1}."
            })

            # Move to next question
            idx += 1
            if idx < len(st.session_state.tech_questions):
                st.session_state.current_tech_q_idx = idx
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": st.session_state.tech_questions[idx]
                })
            else:
                # All tech questions done
                st.session_state.interview_complete = True
                # Save questions to DB
                questions_list = st.session_state.tech_questions
                insert_questions(st.session_state.candidate_id, questions_list)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "The interview is complete! We will notify you via email if there is any update. Thank you for your time."
                })

        st.rerun()
