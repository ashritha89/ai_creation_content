from typing import Optional
from openai import OpenAI

class ContentGenerator:
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def build_prompt(
        self,
        user_instruction: str,
        content_type: str,
        tone: str,
        audience: str,
        length: str,
        extra_notes: Optional[str],
        style: Optional[str],
        mode: str
    ) -> str:
        if mode == "Idea to Structured Content":
            return f"""You are a content strategist.

1. Clarify the idea
2. Suggest 3 angles
3. Write final {content_type}

Idea: {user_instruction}
Tone: {tone}
Audience: {audience}
Length: {length}
Style: {style or "Default"}
Notes: {extra_notes or "None"}
"""
        
        return f"""Generate a {content_type}

Instruction: {user_instruction}
Tone: {tone}
Audience: {audience}
Length: {length}
Style: {style or "Default"}
Notes: {extra_notes or "None"}
"""
    
    def generate_content(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Content generation failed: {str(e)}")
