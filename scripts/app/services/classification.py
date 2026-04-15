"""Complaint classification service using Gemini AI"""

import json
import re
import google.generativeai as genai
from app.config import MODEL_NAME, GEMINI_PROMPT, GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def classify_complaint_gemini(description):
    """Classify complaint using Gemini LLM"""
    try:
        if not description or len(description) < 3:
            return "Invalid", "None"

        prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        print("\nGemini raw response:\n", text_response)

        match = re.search(r'\{[\s\S]*\}', text_response)
        if match:
            result = json.loads(match.group())
            category = result.get("department", "General")
            criticality = result.get("criticality", "Non-Critical")
        else:
            category = "Invalid"
            criticality = "None"

        return category, criticality

    except Exception as e:
        print("Error in Gemini classification:", e)
        return "Invalid", "None"
