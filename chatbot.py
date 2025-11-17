import json
import openai
import time
import random
import sys
from config import API_KEY
from colorama import init, Fore, Style

# Initialize colors
init(autoreset=True)

FAQ_FILE = "faqs.json"

# Load FAQs
try:
    with open(FAQ_FILE, "r") as f:
        faqs = json.load(f)
except FileNotFoundError:
    faqs = []

def save_faq(question, answer):
    faqs.append({"question": question, "answer": answer})
    with open(FAQ_FILE, "w") as f:
        json.dump(faqs, f, indent=4)

def bot_typing(text):
    # Random "thinking..." before typing
    dots = random.randint(1, 3)
    print(Fore.MAGENTA + "Bot is thinking", end="", flush=True)
    for _ in range(dots):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

    # Type answer with random speed
    print(Fore.MAGENTA + "Bot: ", end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(random.uniform(0.02, 0.05))
    print()

def get_answer(user_question):
    # Check offline first
    for faq in faqs:
        if user_question.lower() in faq["question"].lower():
            return faq["answer"]

    # Offline fallback if no API or quota
    if not API_KEY or API_KEY == "your_openai_api_key_here":
        print(Fore.CYAN + "🤖 I don't know this one yet. Can you teach me?")
        user_answer = input(Fore.YELLOW + "You (teach me): " + Style.RESET_ALL).strip()
        if user_answer:
            save_faq(user_question, user_answer)
            # Optional joke/fun fact
            fun_jokes = [
                "Did you know? Cats can make over 100 sounds! 🐱",
                "Joke: Why did the computer show up late to work? It had a hard drive! 💻",
                "Fun fact: Honey never spoils 🍯",
                "Joke: Why do programmers prefer dark mode? Because light attracts bugs! 🐛"
            ]
            joke = random.choice(fun_jokes)
            return f"Thanks! I learned: {user_answer}\n{joke}"
        else:
            return "No answer given, maybe next time!"

    # Online GPT
    try:
        openai.api_key = API_KEY
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_question}],
            max_tokens=150
        )
        answer = response.choices[0].message.content
        save_faq(user_question, answer)
        return answer
    except Exception:
        return "🤖 Cannot answer online right now. Using offline FAQ."

# Friendly startup
print(Fore.CYAN + "👋 Hi! I am FAQ Bot. Type 'exit' to quit.")
print(Fore.GREEN + "💬 Ask me anything!")

# Main chat loop
while True:
    question = input(Fore.YELLOW + "You: " + Style.RESET_ALL)
    if question.lower() == "exit":
        print(Fore.CYAN + "Bye! See you later 😎")
        break
    answer = get_answer(question)
    bot_typing(answer)
