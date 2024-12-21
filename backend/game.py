from question_generator import QuestionGenerator

class TriviaGame:
    def __init__(self):
        self.score = 0
        self.question_generator = QuestionGenerator()

    def play(self):
        print("Welcome to AI Trivia!")
        print("===================")
        
        print("\nSelect a category (or press Enter for random):")
        print("Examples: History, Science, Sports, Movies, Geography, etc.")
        category = input("Category: ").strip()
        
        while True:
            # Keep trying until we get a valid question
            while True:
                question_data = self.question_generator.generate_question(
                    category if category else None
                )
                # Break only if we have valid data
                if question_data and 'Invalid response format received' not in str(question_data):
                    break
                # Otherwise, silently continue trying
                continue

            try:
                # Print just the question text
                print(f"\n{question_data['question'].strip()}")
                # Print each option on a new line, ensuring they're properly formatted
                for option in question_data['options']:
                    print(option.strip())
            except (KeyError, TypeError) as e:
                print("Sorry, there was an error displaying the question. Trying again...")
                continue

            answer = input("\nYour answer (A/B/C/D) or 'q' to quit: ").upper()
            
            if answer == 'Q':
                break
            
            ## Extract just the letter from the correct_answer if it contains the full answer text
            correct_letter = question_data['correct_answer']
            if ')' in correct_letter:
                correct_letter = correct_letter.split(')')[0].strip()
            
            if answer == correct_letter:
                print("Correct! 🎉")
                self.score += 1
            else:
                print(f"Sorry, the correct answer was {question_data['correct_answer']}")

            print(f"Current score: {self.score}")

        print(f"\nGame Over! Final score: {self.score}")
