import os
import openai
from openai import OpenAI
import json
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class QuestionGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=self.api_key)
        self.used_questions = set()  # Track used questions

    def generate_question(self, category=None):
        try:
            logger.info(f"Generating question for category: {category}")
            
            # Keep trying until we get a unique question
            max_attempts = 3
            for _ in range(max_attempts):
                data = self._generate_and_parse_question(category)
                
                if data:
                    question_text = data['question'].strip()
                    if question_text not in self.used_questions:
                        self.used_questions.add(question_text)
                        return data
                    else:
                        logger.info("Duplicate question generated, trying again...")
                        continue
            
            logger.error("Failed to generate unique question after max attempts")
            return None

        except Exception as e:
            logger.error(f"Error generating question: {e}")
            return None

    def _generate_and_parse_question(self, category):
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        prompt = self._build_prompt(category)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a trivia question generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return self._parse_response(response.choices[0].message.content)

    def _build_prompt(self, category):
        base_prompt = """Generate a multiple-choice trivia question with 4 UNIQUE options (A, B, C, D).
        Each answer option must be different from the others.
        Format the response as a JSON object with these fields:
        - question: the question text
        - correct_answer: the letter of the correct answer (A, B, C, or D)
        - options: array of 4 strings, each starting with the letter (A), (B), etc."""

        if category:
            base_prompt += f"\nThe question should be about: {category}"

        return base_prompt

    def _parse_response(self, response_text):
        try:
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

            # Validate unique options
            options = [opt.split(')')[1].strip() for opt in data['options']]
            if len(options) != len(set(options)):
                logger.error("Duplicate answer options detected")
                return None

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
