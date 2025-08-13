## 🌐 LangChain Translator using Gemini

This is a **Streamlit-based language translation and vocabulary assistant** built using **LangChain** and **Google Gemini** (`gemini-2.0-flash`).
It allows you to translate text into multiple languages, view word-by-word translations, and get detailed vocabulary breakdowns including **definitions**, **synonyms**, and **antonyms**.

---

### 🚀 Features

* **Multi-language Translation**
  Translates text into popular languages like Urdu, German, French, Spanish, Arabic, Hindi, Chinese, Russian, Turkish, and Japanese.

* **Word-by-Word Translation**
  Displays each word’s translation for deeper understanding.

* **Definition & Vocabulary Analysis**
  Provides a short definition and identifies important words with their **type**, **synonyms**, and **antonyms**.

* **Translation History**
  Saves your last translation and allows editing directly within the app.

---

<img width="756" height="580" alt="image" src="https://github.com/user-attachments/assets/db95d131-9136-4ee9-a408-eea5d68fabb4" />

---

## 🚀 Live Demo
[Click here to try the Translator App](https://langchaintranslator-bigyxqwdcqebewvshj5owd.streamlit.app/)

---

### 🛠️ Tech Stack

* **Python 3.10+**
* [Streamlit](https://streamlit.io/) – UI framework
* [LangChain](https://www.langchain.com/) – Prompt and chain management
* [Google Gemini API](https://ai.google.dev/) – Language model for translation and text analysis
* `python-dotenv` – Environment variable management

---

### 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ZaidRauf11/langchain-translator.git
   cd langchain-translator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root with your Google API key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

---

### ▶️ Usage

Run the app:

```bash
streamlit run langchain_translator_gemini.py
```

1. Enter text in any language.
2. Select the output language from the dropdown.
3. Click **Translate**.
4. Explore:

   * **🌐 Translated Output**
   * **📘 Word-by-Word Translation**
   * **🧠 Definition**
   * **✅ Synonyms**
   * **❌ Antonyms**

---

### 📂 Project Structure

```
.
├── langchain_translator_gemini.py                # Main Streamlit app
├── requirements.txt                              # Python dependencies
├── .env                                          # Environment variables (Google API key)
└── README.md                                     # Documentation
```

---

### ⚠️ Notes

* Requires a valid **Google API Key** with access to **Gemini 2.0** models.
* Translation quality depends on the model and may vary.
* The vocabulary breakdown relies on the model's parsing, so format consistency is enforced via custom prompt engineering.

