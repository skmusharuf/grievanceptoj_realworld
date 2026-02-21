from flask import Flask, request, jsonify
import google.generativeai as genai
import os, re, json

app = Flask(__name__)


genai.configure(api_key="AIzaSyAqXZHmEcgaYDIV0XidhTUieYyH04YPDxI")  
MODEL_NAME = "gemini-2.5-flash"


GEMINI_PROMPT = """
You are an advanced multilingual grievance classification AI for a public complaint management system.

You will receive a complaint written in English, Hindi, or Telugu.
If not in English, translate it internally (do NOT show the translation).

Your task:
1. Identify the correct department:
   - CM Office (Miscellaneous)
   - Development Authority
   - Municipal
   - Police
   - Public Works Department
   - Transport
2. Determine if it is Critical or Non-Critical.
   - Critical → urgent or safety-related (accident, harassment, violence, fire, injury, etc.)
   - Non-Critical → routine issues (garbage, water supply, road repair, paperwork delays, etc.)
3. Output strictly in this JSON format only:
{
  "department": "<one of the 6>",
  "criticality": "<Critical or Non-Critical>",
  "confidence_reason": "<short reason for your choice>",
  "confidence_score": <number 0–100>
}
4. If unclear or incomplete, return:
{
  "department": "Invalid",
  "criticality": "None",
  "confidence_reason": "Complaint unclear or incomplete",
  "confidence_score": 0
}

Now classify the following complaint:
<<<USER_COMPLAINT>>>
"""

@app.route("/api/classify", methods=["POST"])
def classify_complaint():
    try:
        data = request.json
        description = data.get("description", "").strip()

        if not description or len(description) < 3:
            return jsonify({
                "department": "Invalid",
                "criticality": "None",
                "confidence_reason": "Complaint too short or unclear",
                "confidence_score": 0
            }), 200

        # Construct prompt
        prompt = GEMINI_PROMPT.replace("<<<USER_COMPLAINT>>>", description)

        # Call Gemini 2.5-Pro
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        print("\n🧠 Raw Gemini Response:\n", text_response)

        # Extract JSON safely
        match = re.search(r'\{[\s\S]*\}', text_response)
        if match:
            result = json.loads(match.group())
        else:
            result = {
                "department": "Invalid",
                "criticality": "None",
                "confidence_reason": "Could not parse Gemini output",
                "confidence_score": 0
            }

        return jsonify(result), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({
            "error": "Classification failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)