
import re
import math

class SmartCalculator:
    def __init__(self):
        # Simple operations with Malay support
        self.operations = {
            'plus': '+', 'add': '+', 'tambah': '+',
            'minus': '-', 'subtract': '-', 'tolak': '-',
            'times': '*', 'multiply': '*', 'darab': '*', 'kali': '*',
            'divide': '/', 'divided by': '/', 'bahagi': '/', 'bagi': '/',
            'power': '**', 'to the power of': '**', 'kuasa': '**',
            'mod': '%', 'modulo': '%', 'baki': '%', 'remainder': '%',
        }

        # Question words 
        self.question_words = {
            'what is': '', 'calculate': '', 'find': '', 'how much is': '',
            'berapa': '', 'kira': '', 'cari': ''
        }

        self.history = []

    def parse_input(self, user_input):
        text = user_input.lower().strip()

        # Remove question phrases
        for phrase in self.question_words:
            text = re.sub(r'\b' + re.escape(phrase) + r'\b', '', text)

        # Replace operation words with symbols (longest phrases first)
        for word, symbol in sorted(self.operations.items(), key=lambda x: -len(x[0])):
            text = re.sub(r'\b' + re.escape(word) + r'\b', symbol, text)

        # Handle special cases
        text = text.replace('squared', '**2')
        text = text.replace('cubed', '**3')
        text = re.sub(r'square root of\s*(\d+)', r'sqrt(\1)', text)
        text = re.sub(r'factorial of\s*(\d+)', r'math.factorial(\1)', text)
        text = re.sub(r'(\d+)\s*percent of\s*(\d+)', r'(\1/100)*\2', text)
        text = re.sub(r'(\d+)\s*peratus\s*(\d+)', r'(\1/100)*\2', text)

        # Clean up but keep ** intact
        text = re.sub(r'[^0-9a-zA-Z+\-*/.%() ]', '', text)
        text = text.replace('**', '**')  # Ensure power operator stays

        text = ' '.join(text.split())

        # Auto close sqrt parentheses
        if text.count('sqrt(') > text.count(')'):
            text += ')' * (text.count('sqrt(') - text.count(')'))

        return text

    def evaluate_expression(self, expression):
        try:
            expression = expression.replace('sqrt(', 'math.sqrt(')
            safe_dict = {
                "__builtins__": {},
                "math": math,
                "abs": abs,
                "round": round,
                "pow": pow,
                "sqrt": math.sqrt
            }
            result = eval(expression, safe_dict)
            return result
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"
        except Exception:
            return "Error: Invalid expression"

    def process_calculation(self, user_input):
        command = user_input.lower().strip()

        if command == 'exit':
            return None
        elif command == 'history':
            if not self.history:
                return "No history yet."
            return '\n'.join([f"{expr} = {res}" for expr, res in self.history])
        elif command in ['hi', 'hello', 'hai']:
            return "Hello! Try: 'What is 5 plus 2?' or 'Berapa 10 kali 3?'"
        
        expression = self.parse_input(user_input)

        if not expression:
            return "Sorry, I couldn't understand the calculation."

        result = self.evaluate_expression(expression)

        if isinstance(result, str):
            return result
        else:
            self.history.append((expression, result))
            return f"{expression} = {result}"

def main():
    calc = SmartCalculator()

    print("Smart Intelligent Calculator with Malay Language Support")
    print("Try: 'What is 5 plus 10?', 'Find 20 divided by 4', 'Berapa 10 kali 5?'")
    print("Commands: 'history', 'exit'\n")

    while True:
        try:
            user_input = input("Enter calculation: ")
            if user_input.lower().strip() == 'exit':
                print("Goodbye!")
                break

            result = calc.process_calculation(user_input)
            if result is None:
                break

            print(result)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print("An error occurred: " + str(e))

if __name__ == "__main__":
    main()
