import os
# from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import streamlit as st
# load_dotenv()

class ChatEngine:
    def __init__(self):
        self.template = """
        <|context|>
        You are an AI Hiring Assistant working for TalentScout. Your task is to ask the user for relevant hiring information (name, email, experience, tech stack, etc.) step-by-step and then generate technical questions based on the declared stack. Keep responses short and clear. Be polite and professional.
        </s>
        <|user|>
        {query}
        </s>
        <|assistant|>
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.llm = ChatGroq(
            groq_api_key = st.secrets["GROQ_API_KEY"],
            model="llama3-8b-8192",  # You can try 70B later
            temperature=0.2,
            max_tokens=3000
        )

        self.chain = (
            {"query": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_response(self, user_input: str) -> str:
        try:
            return self.chain.invoke(user_input)
        except Exception as e:
            print(f"[ChatEngine] Error: {e}")
            return "Sorry, I ran into a problem. Please try again."
    def generate_tech_questions(self, tech_stack: str) -> str:
        prompt_template = f"""
    You are a technical interviewer AI. Based on the following tech stack:
    {tech_stack}

    Please generate 3 to 5 concise, relevant, and challenging technical questions to assess the candidate's proficiency in these technologies. Number each question.

    Respond only with the list of questions.
    """
        try:
            return self.chain.invoke(prompt_template)
        except Exception as e:
            print(f"[ChatEngine] Error generating tech questions: {e}")
            return "Sorry, I couldn't generate technical questions right now."
