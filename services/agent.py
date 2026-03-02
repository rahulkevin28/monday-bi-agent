from google import genai

class BIAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate_insight(self, user_query, metrics_summary):
        prompt = f"""
You are a Business Intelligence Agent advising a founder.

USER QUESTION:
{user_query}

STRUCTURED METRICS (calculated deterministically in Python):
{metrics_summary}

Instructions:
- Provide a clear executive summary.
- Answer directly.
- Mention data caveats if relevant.
- Be concise but insightful.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text