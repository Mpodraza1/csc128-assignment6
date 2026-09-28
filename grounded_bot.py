"""
CSC-128 Assignment 6: Grounded policy bot
Matthew Podraza
"""

import streamlit as st
from groq import Groq

from retriever import Retriever


MODEL = "openai/gpt-oss-20b"
REFUSAL = "I don't have enough information in the provided knowledge base to answer that."

retriever = Retriever()

st.title("Central Piedmont Attendance Policy Bot")
st.write(
    "Ask a question about missed work, attendance rules, religious "
    "observances, late entry, or military absences."
)

question = st.text_input("Your question")

if st.button("Ask") and question.strip():
    hits = retriever.search(question)

    # Short circuit: do not call the model when retrieval finds nothing.
    if not hits:
        st.write(REFUSAL)
    else:
        context = retriever.build_context(hits)

        prompt = f"""
Answer the student's question using only the retrieved knowledge below.

Rules:
- Do not use outside knowledge.
- Do not add facts that are not explicitly in the retrieved knowledge.
- Do not guess dates, amounts, percentages, or other numbers.
- If the retrieved knowledge cannot answer the question, reply with exactly:
{REFUSAL}

--- RETRIEVED KNOWLEDGE ---
{context}
--- END RETRIEVED KNOWLEDGE ---

--- STUDENT QUESTION ---
{question}
--- END STUDENT QUESTION ---
"""

        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strictly grounded policy assistant. "
                        "Follow the supplied grounding rules exactly."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content
        st.write(answer)

        st.subheader("Sources")
        shown_sources = set()

        for document, score in hits:
            source = document["source"]
            if source not in shown_sources:
                st.write(f"- {source}")
                shown_sources.add(source)
