from openai import OpenAI

class ContentRepurposer:
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def repurpose_content(self, content: str) -> str:
        prompt = f"""Repurpose this content into:
1. LinkedIn Post (professional, engaging)
2. Professional Email (clear, actionable)
3. Short Ad Copy (compelling, concise)

Original Content:
{content}

Format each repurposed version clearly with headers.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Repurposing failed: {str(e)}"
