from openai import OpenAI

class ContentEvaluator:
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def evaluate_content(self, content: str, content_type: str, tone: str) -> str:
        prompt = f"""Evaluate the content:

{content}

Return a structured evaluation with:
- Clarity Score (1-10)
- Engagement Score (1-10)
- Tone Match ({tone}) (1-10)
- Platform Fit ({content_type}) (1-10)
- Overall Verdict (brief summary)

Format the response clearly with scores and brief explanations.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Evaluation failed: {str(e)}"
