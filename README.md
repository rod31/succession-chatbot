# Succession Chatbot

**Chat with the Roy family from _Succession_!**

> “Words are just, what? Nothing… complicated airflow.”  
> — Kendall Roy

This project brings _Succession’s_ razor-sharp dialogue to life with an AI-powered chatbot. Built on four seasons of Roy family scripts, it uses FAISS to surface the most on-brand lines and a fine-tuned OpenAI model to stitch them into real-time conversation. The sleek Streamlit interface means you can pick Roman, Shiv, Kendall, or Logan and jump straight into the chaos.

What makes _Succession_ so hypnotic is its **weaponized language**. As the [Wall Street Journal](https://www.wsj.com/arts-culture/television/the-weaponized-language-of-succession-eb97357f) points out, every curse, double-entendre, and clipped syllable is engineered to convey power, paranoia, and performance. Nerdwriter’s [deep-dive video](https://www.youtube.com/watch?v=REhlyvtiIhQ) breaks down how each Roy uses vocabulary as a character voice—whether it’s Roman’s biting sarcasm, Shiv’s steely precision, or Kendall’s tortured earnestness.

I built this chatbot out of a fascination for how **word choice** and **speech patterns** reveal inner worlds. By indexing thousands of italicized lines with FAISS and guiding GPT-4o-mini with curated quotes, the app doesn’t just mimic the Roys’ tone—it **channels their personality**. In Shiv's words,  
> “This project doesn’t just mimic speech; it channels the very soul of what makes the Roys, well, the Roys.”
> 

My inspiration to build this project comes from my deep fascination with how personality comes through in language. The result is a chatbot that **feels** like the characters in this show. Or, using shiv's words, "This project doesn’t just mimic speech; it channels the very soul of what makes the Roys, well, the Roys."

---

## 📺 Live Demo

[Try the Succession Chatbot here](https://succession-chatbot.streamlit.app/)

<p align="center">
  <img src="./screenshots/interface2.png" alt="Succession Chatbot Interface" width="600">
  <img src="./screenshots/interface1.png" width="600">
</p>

---

## 🔍 Features

- **Character Selection**: Choose which Roy family member you want to chat with.  
- **Smart Reply Mode**: Retrieves contextually relevant quotes using FAISS + SentenceTransformer embeddings to guide GPT responses.  
- **Roy Parrot Mode**: A keyword-matching fallback that mimics signature one-liners.  
- **Session History**: Maintains chat history during your session for full conversational context.  
- **Custom Prompt Engineering**: Uses targeted system prompts to replicate each character’s tone, including humor, sarcasm, and trademark curses.

---

## 🛠️ Tech Stack

- **Streamlit**: UI framework  
- **OpenAI API**: GPT-4o-mini for dynamic responses  
- **FAISS**: Vector similarity retrieval  
- **SentenceTransformer**: Embedding generation (`all-MiniLM-L6-v2`)  
- **PyMuPDF (fitz)**: Extracting and marking up italicized dialogue from PDFs  
- **Python**: Core scripting, regex heuristics, and pipeline glue

---

