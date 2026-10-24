
import random
from datetime import datetime

def alexa_answer(question):
    question = question.lower().strip()

    if "today" in question or "date" in question:
        today = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {today}."

    elif "fun fact" in question:
        facts = [
            "Honey can remain edible for a very long time when stored properly.",
            "Octopuses have three hearts.",
            "The Earth revolves around the Sun."
        ]
        return random.choice(facts)

    elif "motivate" in question or "motivation" in question:
        return "Believe in yourself. Keep learning and never give up."

    elif "artificial intelligence" in question or question == "what is ai":
        return (
            "Artificial intelligence is technology that helps "
            "computers perform tasks that usually require human intelligence."
        )

    elif "information" in question or "daily tip" in question:
        return (
            "Today's tip: Learn something new, stay organized, "
            "and take short breaks while studying."
        )

    elif "hello" in question or "hi" in question:
        return "Hello! I am your personal Alexa-style assistant."

    elif "your name" in question:
        return "You can call me My Alexa."

    elif "help" in question:
        return (
            "You can ask me about today's date, fun facts, "
            "motivation, artificial intelligence, or daily tips."
        )

    elif "bye" in question or "exit" in question:
        return "Goodbye! Have a wonderful day."

    else:
        return (
            "Sorry, I don't know that answer yet. "
            "Please try another question."
        )

print("=" * 40)
print("       WELCOME TO MY ALEXA")
print("=" * 40)
print("Ask a question or type 'exit' to stop.")

while True:
    question = input("\nYou: ")

    if question.lower().strip() in ["exit", "quit", "bye"]:
        print("Alexa: Goodbye! Have a wonderful day.")
        break

    answer = alexa_answer(question)
    print("Alexa:", answer)


