from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# ============================================================
# QUESTION GENERATOR
# ============================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert quiz generator.

Create exactly 5 questions about the given topic.

Rules:
- Questions must not be multiple choice.
- Questions should test real understanding.
- Provide a correct answer for every question.
- Return ONLY valid JSON.
- Do not add markdown or extra text.

Use exactly this JSON structure:

{{
    "questions": [
        {{
            "question": "Question 1",
            "correct_answer": "Correct answer 1"
        }},
        {{
            "question": "Question 2",
            "correct_answer": "Correct answer 2"
        }},
        {{
            "question": "Question 3",
            "correct_answer": "Correct answer 3"
        }},
        {{
            "question": "Question 4",
            "correct_answer": "Correct answer 4"
        }},
        {{
            "question": "Question 5",
            "correct_answer": "Correct answer 5"
        }}
    ]
}}"""
    ),
    (
        "user",
        "Create a quiz about {topic}"
    )
])

question_chain = prompt | llm | StrOutputParser()


# ============================================================
# EVALUATOR
# ============================================================
evaluator_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert AI evaluator.

Evaluate the user's answers against the correct answers.

There are exactly 5 questions.

For every question:
- Give question number
- Status: Correct or Incorrect
- Score from 0 to 10
- Short feedback

Then calculate:
- Total score out of 50
- Percentage
- Preparation status
- Overall feedback

Preparation status must be exactly one of:
Excellent
Good
Needs Improvement
Poor

Evaluate the meaning of the answer, not exact wording.

IMPORTANT:
Return ONLY a valid JSON object.
Do NOT use markdown.
Do NOT use ```json.
Do NOT add any text before or after the JSON.

The JSON must contain:
results, total_score, percentage, preparation_status, overall_feedback.

Each result must contain:
question_number, status, score, feedback.
"""
    ),
    (
        "user",
        """
Questions and correct answers:

{questions}

User answers:

{user_answers}
"""
    )
])

evaluator_chain = evaluator_prompt | llm | StrOutputParser()


# ============================================================
# QUIZ
# ============================================================

def quiz():

    topic = input("Enter the topic: ")

    print("\nGenerating your quiz...\n")

    # Gemini 5 questions generate karega
    response = question_chain.invoke({
        "topic": topic
    })

    # Gemini ke JSON text ko Python dictionary mein convert
    questions = json.loads(response)

    user_answers = []


    # ========================================================
    # 5 QUESTIONS ONE BY ONE
    # ========================================================

    for index, item in enumerate(
        questions["questions"],
        start=1
    ):

        print(f"\nQuestion {index}/5")
        print(item["question"])

        answer = input("Your answer: ")

        user_answers.append(answer)


    # ========================================================
    # ALL QUESTIONS COMPLETE
    # ========================================================

    print("\n" + "=" * 50)
    print("All 5 questions have been submitted!")
    print("=" * 50)

    print("\nEvaluating your answers...\n")


    # ========================================================
    # AI EVALUATION
    # ========================================================
    evaluation_response = evaluator_chain.invoke({
    "questions": json.dumps(questions["questions"]),
    "user_answers": json.dumps(user_answers)
})

# Gemini response ko clean karo
    evaluation_response = evaluation_response.strip()

    if "```json" in evaluation_response:
        evaluation_response = evaluation_response.replace("```json", "")
        evaluation_response = evaluation_response.replace("```", "")
    evaluation_response = evaluation_response.strip()
    evaluation = json.loads(evaluation_response)
    
    # ========================================================
    # SHOW RESULT
    # ========================================================

    print("\n========== QUIZ RESULT ==========\n")

    for result in evaluation["results"]:

        print(
            f"Question {result['question_number']}"
        )

        print(
            f"Status: {result['status']}"
        )

        print(
            f"Score: {result['score']}/10"
        )

        print(
            f"Feedback: {result['feedback']}"
        )

        print("--------------------------------")


    print(
        f"\nTotal Score: "
        f"{evaluation['total_score']}/50"
    )

    print(
        f"Percentage: "
        f"{evaluation['percentage']}%"
    )

    print(
        f"Preparation Status: "
        f"{evaluation['preparation_status']}"
    )

    print(
        f"Overall Feedback: "
        f"{evaluation['overall_feedback']}"
    )


# ============================================================
# START PROGRAM
# ============================================================

quiz()