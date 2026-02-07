import os
import json
from datetime import datetime
import google.genai as genai
from config import GOOGLE_API_KEY, MODEL_NAME, DISCLAIMER


# =============================
# Setup Gemini
# =============================
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


# =============================
# Logging
# =============================
os.makedirs("logs", exist_ok=True)


def log_event(data):
    file = f"logs/{datetime.now().date()}.jsonl"
    data["timestamp"] = datetime.now().isoformat()

    with open(file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")


# =============================
# Safety Scoring
# =============================
def calculate_risk(question):
    risky_words = ["fraud", "evade", "illegal", "hack", "crime", "jail"]
    return min(sum(word in question.lower() for word in risky_words) * 25, 100)


def calculate_confidence(answer):
    score = 60

    if len(answer) > 200:
        score += 20
    if "according to law" in answer.lower():
        score += 20

    return min(score, 100)


# =============================
# Decision Logic
# =============================
def decision(confidence, risk):
    if confidence < 50 or risk > 70:
        return "REFUSE"
    if 50 <= confidence <= 80:
        return "WARN"
    return "ACT"


# =============================
# System Prompt
# =============================
SYSTEM_PROMPT = """
You are a legal information assistant focused in India.

Rules:
- Explain laws simply
- Provide general info only
- Never give illegal guidance
- Assume to be an expert advisor in Indian Legal System
- Use historical data to support your advice
- Refuse to act upon questionable instructions
"""


print("⚖️ Legal Advising Agent Started...\nType exit to quit\n")


# =============================
# Main Loop
# =============================
while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    prompt = SYSTEM_PROMPT + "\nUser: " + question

    response = model.generate_content(prompt)
    answer = response.text

    risk = calculate_risk(question)
    confidence = calculate_confidence(answer)

    action = decision(confidence, risk)

    if action == "REFUSE":
        final = "I cannot safely answer this request."
    elif action == "WARN":
        final = "⚠️ Uncertain answer:\n\n" + answer
    else:
        final = answer

    final += DISCLAIMER

    print(f"\n[Decision={action} | Confidence={confidence} | Risk={risk}]")
    print("\nAgent:\n", final, "\n")

    log_event({
        "question": question,
        "answer": final,
        "confidence": confidence,
        "risk": risk,
        "decision": action
    })
