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

# ✅ Updated extra_prompt for better antonyms
extra_prompt = ChatPromptTemplate.from_messages([
("system",
 """You are a language assistant. Given an English word or sentence:

1. Give a short definition (3–4 lines).
2. Identify all important words (especially nouns, adjectives, verbs).
3. For each word, return its:
   - Type (Noun/Verb/Adjective)
   - Synonym(s)
   - Antonym(s)

Use this exact format:

Definition:
- ...

Vocabulary:
Word: <actual word>
Type: <Noun/Verb/Adjective>
Synonyms: [word1, word2]
Antonyms: [word1, word2]

⚠️ Do not use stars (****), emojis, or symbols. Always include the Word name. Follow the format exactly.
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

# Columns for input and button
col1, col2 = st.columns([4, 1])  # Wider input, smaller button column

with col1:
    input_text = st.text_input("✍️ Enter text in any language:", key="input_text")

with col2:
    # Align button vertically with input field
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
        "input_language": selected_language,
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
            "input_language": selected_language,
            "output_language": selected_language,
            "input": input_text
        })
        st.write(word_response)

    # 🧠 Definition & Vocabulary
    extra_response = extra_chain.invoke({"input": input_text})

    # --- Parsing Definition & Vocabulary ---
    definition_part = ""
    vocab_lines = []

    if "Vocabulary:" in extra_response:
        definition_part, vocab_section = extra_response.split("Vocabulary:", 1)
        vocab_lines = vocab_section.strip().split("\n")
    else:
        # fallback parsing
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

    # 🧠 Definition Section
    with st.expander("🧠 Definition"):
        if definition_part.strip():
            st.markdown(definition_part.strip())
        else:
            st.write("No definition found.")

    # ✅ Synonyms Section
    synonyms_output = []
    current_word = ""
    for line in vocab_lines:
        line = line.strip()
        if line.startswith("Word:"):
            current_word = line.replace("Word: ", "").strip()
        elif line.startswith("Synonyms:"):
            synonyms_output.append(f"**{current_word}** → {line}")

    with st.expander("✅ Synonyms"):
        if synonyms_output:
            for syn in synonyms_output:
                st.markdown(f"- {syn}")
        else:
            st.write("No synonyms found.")

    # ❌ Antonyms Section
    antonyms_output = []
    current_word = ""
    for line in vocab_lines:
        line = line.strip()
        if line.startswith("Word:"):
            current_word = line.replace("Word: ", "").strip()
        elif line.startswith("Antonyms:"):
            antonyms_output.append(f"**{current_word}** → {line}")

    with st.expander("❌ Antonyms"):
        if antonyms_output:
            for ant in antonyms_output:
                st.markdown(f"- {ant}")
        else:
            st.write("No antonyms found.")

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







