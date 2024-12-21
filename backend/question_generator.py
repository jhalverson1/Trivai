from openai import OpenAI
import os
import json
import logging
import re

logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class QuestionGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not found in environment variables")

    def _parse_question(self, content: str) -> dict:
        """Parse the OpenAI response into a structured question format."""
        try:
            # Clean up the content and join any split lines
            content = ' '.join(content.split())
            # Split on pipe character
            parts = content.split('|')
            
            if len(parts) != 6:
                logger.error(f"Invalid response format: {content}")
                return None
            
            question, *options, correct = parts
            # Clean up the options
            cleaned_options = []
            for opt in options:
                # Remove the letter prefix and any whitespace
                cleaned_opt = opt.strip()
                match = re.match(r'^[A-D]\)\s*(.+)$', cleaned_opt)
                if match:
                    cleaned_opt = match.group(1).strip()
                cleaned_options.append(cleaned_opt)

            # Extract just the letter from "Correct:X"
            correct_match = re.search(r'Correct:([A-D])', correct)
            if not correct_match:
                logger.error(f"Invalid correct answer format: {correct}")
                return None
            correct_letter = correct_match.group(1)
            
            logger.info(f"Successfully parsed question: {question}")
            logger.info(f"Options: {cleaned_options}")
            logger.info(f"Correct answer: {correct_letter}")
            
            return {
                "question": question.strip(),
                "options": [f"{letter}) {opt}" for letter, opt in zip(['A', 'B', 'C', 'D'], cleaned_options)],
                "correct_answer": correct_letter
            }
        except Exception as e:
            logger.error(f"Error parsing question: {str(e)}")
            return None

    def generate_question(self, category=None, max_retries=2):
        """Generate a trivia question with limited retries."""
        if not OPENAI_API_KEY:
            raise Exception("OpenAI API key is not configured")

        base_prompt = """Generate a trivia question in this exact format:
Question|A) Option1|B) Option2|C) Option3|D) Option4|Correct:Letter

Rules:
1. Use a single line with pipe separators
2. No newlines in the response
3. Options must start with A), B), C), or D)
4. Correct answer must be just the letter (A, B, C, or D)"""

        if category:
            base_prompt += f"\n\nThe question MUST be about {category}."

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a trivia question generator."},
                        {"role": "user", "content": base_prompt}
                    ],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                logger.info(f"Raw response: {content}")
                parsed = self._parse_question(content)
                
                if parsed:
                    return parsed
                
                logger.warning(f"Failed to parse question on attempt {attempt + 1}")
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate question after {max_retries} attempts")
        
        raise Exception("Failed to generate a valid question")
