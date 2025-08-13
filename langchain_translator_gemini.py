import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Set up Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Prompts
main_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{input}"),
])

word_prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate each word from {input_language} to {output_language} in this sentence:"),
    ("human", "{input}")
])

# ✅ Updated to handle multiple languages for synonyms/antonyms
extra_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a multilingual language assistant.
Given a {input_language} sentence, respond in {output_language}.

1. Provide a short definition (3–4 lines) **in {output_language}**.
2. Identify important words (nouns, verbs, adjectives) **in {output_language}**.
3. For each word, list:
   - Type (Noun/Verb/Adjective)
   - Synonyms in {output_language}
   - Antonyms in {output_language}

Follow this exact format:

Definition:
- ...

Vocabulary:
Word: <actual word>
Type: <Noun/Verb/Adjective>
Synonyms: [word1, word2]
Antonyms: [word1, word2]

⚠️ No emojis, stars, or extra symbols. Keep format exact.
"""),
    ("human", "{input}")
])

# Output parser
output_parser = StrOutputParser()

# Chains
chain = main_prompt | llm | output_parser
word_chain = word_prompt | llm | output_parser
extra_chain = extra_prompt | llm | output_parser

# Streamlit UI
st.title('🌐 Langchain Translator using Gemini')

# Session state setup
if "last_translation" not in st.session_state:
    st.session_state.last_translation = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# Input & button
col1, col2 = st.columns([4, 1])
with col1:
    input_text = st.text_input("✍️ Enter text in any language:", key="input_text")
with col2:
    st.markdown("<div style='margin-top: 1.9em;'>", unsafe_allow_html=True)
    translate_button = st.button("🔁 Translate", key="translate_button")
    st.markdown("</div>", unsafe_allow_html=True)

# Language selection
languages = [
    "Urdu", "German", "French", "Spanish", "Arabic",
    "Hindi", "Chinese", "Russian", "Turkish", "Japanese"
]
selected_language = st.selectbox("🌍 Select language to translate to:", languages)

# Process input
if input_text and selected_language:
    # 🌐 Translation
    response = chain.invoke({
        "input_language": "English",  # Assuming input is English
        "output_language": selected_language,
        "input": input_text
    })
    st.session_state.last_translation = {
        "input": input_text,
        "output": response,
        "language": selected_language
    }
    st.session_state.edit_mode = False

    # ✅ Translated Output
    st.markdown("### 🌐 Translated Output")
    st.write(response)

    # 📘 Word-by-word
    with st.expander("📘 Word-by-word translation"):
        word_response = word_chain.invoke({
            "input_language": "English",
            "output_language": selected_language,
            "input": input_text
        })
        st.write(word_response)

    # 🧠 Definition & Vocabulary (NOW in selected_language)
    extra_response = extra_chain.invoke({
        "input": input_text,
        "input_language": "English",
        "output_language": selected_language
    })

    # --- Parsing ---
    definition_part = ""
    vocab_lines = []

    if "Vocabulary:" in extra_response:
        definition_part, vocab_section = extra_response.split("Vocabulary:", 1)
        vocab_lines = vocab_section.strip().split("\n")
    else:
        lines = extra_response.splitlines()
        collecting_vocab = False
        for line in lines:
            if "Definition:" in line:
                collecting_vocab = False
                definition_part += line + "\n"
            elif line.strip().startswith("Word:"):
                collecting_vocab = True
                vocab_lines.append(line)
            elif collecting_vocab:
                vocab_lines.append(line)
            else:
                definition_part += line + "\n"

    # 🧠 Definition
    with st.expander("🧠 Definition"):
        st.markdown(definition_part.strip() if definition_part.strip() else "No definition found.")

    # ✅ Synonyms
    synonyms_output = []
    current_word = ""
    for line in vocab_lines:
        line = line.strip()
        if line.startswith("Word:"):
            current_word = line.replace("Word: ", "").strip()
        elif line.startswith("Synonyms:"):
            synonyms_output.append(f"**{current_word}** → {line}")
    with st.expander("✅ Synonyms"):
        st.markdown("\n".join(f"- {syn}" for syn in synonyms_output) if synonyms_output else "No synonyms found.")

    # ❌ Antonyms
    antonyms_output = []
    current_word = ""
    for line in vocab_lines:
        line = line.strip()
        if line.startswith("Word:"):
            current_word = line.replace("Word: ", "").strip()
        elif line.startswith("Antonyms:"):
            antonyms_output.append(f"**{current_word}** → {line}")
    with st.expander("❌ Antonyms"):
        st.markdown("\n".join(f"- {ant}" for ant in antonyms_output) if antonyms_output else "No antonyms found.")

# 📝 Saved Translations
if st.session_state.last_translation:
    with st.expander("📝 Saved Translation History"):
        last = st.session_state.last_translation
        if not st.session_state.edit_mode:
            st.markdown(f"**Input:** {last['input']}")
            st.markdown(f"**Language:** {last['language']}")
            st.markdown(f"**Output:** {last['output']}")
            if st.button("✏️ Edit Translation"):
                st.session_state.edit_mode = True
        else:
            new_translation = st.text_area("Edit the translated output:", value=last['output'])
            if st.button("💾 Save Edited Translation"):
                st.session_state.last_translation['output'] = new_translation
                st.session_state.edit_mode = False
                st.success("✅ Translation updated!")






