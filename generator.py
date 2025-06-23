# imports
import streamlit as st
from docx import Document  # from handling word documents
import PyPDF2 # for PDF reading
from openai import OpenAI  # OpenRouter client for Claude


# API initializer
client = OpenAI(
    api_key="", #API code (for openAI) -> DELETED
    base_url="https://openrouter.ai/api/v1"
)


# title and subheading UI
st.title("📚 STUDIZ")
st.subheader("Your AI-powered question generator 🤖")


# selecting diffuculty
difficulty = st.radio(
    "Select difficulty level for the questions:",
    ("Easy", "Medium", "Hard")
)


# text extraction function
def extract_text(file):
    file_type = file.type

    if file_type.endswith("pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([p.extract_text() or "" for p in reader.pages])

    elif file_type.endswith("plain"):
        return file.read().decode("utf-8", errors="ignore")

    elif file_type.endswith("document"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    return "❌ Unsupported file format"


# questions generator function
def generate_questions(text):
    response = client.chat.completions.create(
        model="anthropic/claude-3-sonnet-20240229",
        messages=[
            {"role": "system", "content": "You're a helpful tutor."},
            {"role": "user", "content": f"Make 5 ~ 10 {difficulty.lower()} level quiz questions from this text:\n\n{text}"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content


# file upload (click to upload)
uploaded_file = st.file_uploader(
    "📎 Upload a file (PDF, TXT, DOCX, or Image)",
    type=["pdf", "txt", "docx", "jpg", "jpeg", "png", "gif", "bmp"]
)


# on file upload (text extraction + question generation)
if uploaded_file:
    content = extract_text(uploaded_file)
    st.text_area("📄 Extracted Text:", content, height=800)


    # button for generating questions
    if st.button("Generate Questions"):
        with st.spinner("⏳ Please wait a few moments while your questions are being generated"):
            questions = generate_questions(content)


        # listing out the questions generated
        st.markdown("### 🧠 Questions:")
        for q in questions.split('\n'):
            if q.strip():
                st.write("- " + q.strip())
