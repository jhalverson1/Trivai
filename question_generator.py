from openai import OpenAI
from config import OPENAI_API_KEY

class QuestionGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_question(self, category=None):
        prompt = "Generate a trivia question with 4 multiple choice options and indicate the correct answer. "
        if category:
            prompt += f"The category should be {category}. "
        prompt += "Format the response as: Question|A) OptionB) Option2|C) Option3|D) Option4|Correct:Letter"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            parsed = self._parse_question(response.choices[0].message.content)
            if parsed is None:
                return self.generate_question(category)  # Try again if parsing failed
            return parsed
        except Exception as e:
            print(f"Error generating question: {e}")
            return None

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
