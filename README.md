# 🤖 AI Quiz Evaluator

An AI-powered quiz application built with **Python, LangChain, and Google Gemini**.

The application generates a 5-question quiz based on a topic provided by the user. The user answers the questions one by one, and after all 5 answers are submitted, Gemini evaluates the answers and provides individual scores, feedback, total score, percentage, and overall preparation status.

---

## 🚀 Features

- 🤖 AI-generated quiz questions
- 📚 User can choose any topic
- ❓ Generates exactly 5 questions
- ✍️ User answers questions one by one
- 🧠 AI evaluates answers based on meaning
- 📊 Individual score for every question
- 💬 Feedback for every answer
- 🎯 Total score out of 50
- 📈 Percentage calculation
- 📝 Overall preparation status
- 💡 Overall preparation feedback
- 🔗 Built using LangChain
- ⚡ Uses Google Gemini

---

## 🛠️ Technologies Used

- Python
- LangChain
- Google Gemini
- `langchain-google-genai`
- Python Dotenv
- JSON

---

## 🔄 How It Works

```text
User enters a topic
        ↓
Google Gemini generates 5 questions
        ↓
User answers Question 1
        ↓
User answers Question 2
        ↓
User answers Question 3
        ↓
User answers Question 4
        ↓
User answers Question 5
        ↓
AI evaluates all answers
        ↓
Individual scores + feedback
        ↓
Total Score /50
        ↓
Percentage
        ↓
Preparation Status
        ↓
Overall Feedback
