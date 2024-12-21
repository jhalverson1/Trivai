from openai import OpenAI
from config import OPENAI_API_KEY

class QuestionGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_question(self, category=None):
        if not OPENAI_API_KEY:
            print("OpenAI API key is not set")
            raise Exception("OpenAI API key is not configured")

        base_prompt = """Generate a trivia question that is:
1. Focused on well-established historical facts, scientific concepts, or cultural knowledge
2. Clear and unambiguous
3. Have 4 distinct multiple choice options
4. Include one clearly correct answer"""

        if category:
            base_prompt += f"\n\nThe question MUST be about {category}."
        
        base_prompt += "\n\nFormat: Question|A) Option1|B) Option2|C) Option3|D) Option4|Correct:Letter"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a trivia question generator."},
                    {"role": "user", "content": base_prompt}
                ]
            )
            parsed = self._parse_question(response.choices[0].message.content)
            if parsed is None:
                return self.generate_question(category)  # Try again if parsing failed
            return parsed
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            raise Exception(f"Failed to generate question: {str(e)}")

    def _parse_question(self, response):
        try:
            parts = response.split('|')
            if len(parts) < 6:
                return None
            
            return {
                'question': parts[0].strip(),
                'options': [opt.strip() for opt in parts[1:5]],
                'correct_answer': parts[5].replace('Correct:', '').strip()
            }
        except Exception as e:
            return None
