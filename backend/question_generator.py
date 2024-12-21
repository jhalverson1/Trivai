import os
import openai
import json
import logging

logger = logging.getLogger(__name__)

class QuestionGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        openai.api_key = self.api_key

    def generate_question(self, category=None):
        try:
            logger.info(f"Generating question for category: {category}")
            if not self.api_key:
                raise ValueError("OpenAI API key not configured")

            prompt = self._build_prompt(category)
            logger.info("Calling OpenAI API")
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a trivia question generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            logger.info("Received response from OpenAI")
            result = self._parse_response(response.choices[0].message.content)
            if not result:
                logger.error("Failed to parse OpenAI response")
                raise ValueError("Invalid response format from OpenAI")
                
            return result

        except Exception as e:
            logger.error(f"Error generating question: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")

    def _build_prompt(self, category):
        base_prompt = """Generate a multiple-choice trivia question with 4 options (A, B, C, D).
        Format the response as a JSON object with these fields:
        - question: the question text
        - correct_answer: the letter of the correct answer (A, B, C, or D)
        - options: array of 4 strings, each starting with the letter (A), (B), etc."""

        if category:
            base_prompt += f"\nThe question should be about: {category}"

        return base_prompt

    def _parse_response(self, response_text):
        try:
            # Find the JSON part of the response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start == -1 or end == 0:
                logger.error("No JSON found in response")
                return None

            json_str = response_text[start:end]
            data = json.loads(json_str)
            
            required_fields = ['question', 'correct_answer', 'options']
            if not all(field in data for field in required_fields):
                logger.error(f"Missing required fields in response: {data}")
                return None

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
