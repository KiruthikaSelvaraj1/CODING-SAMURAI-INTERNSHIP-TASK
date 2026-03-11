"""
Rule-Based Support Chatbot (Class-Based with Regex)
Project 1: Artificial Intelligence Internship - Beginner Level

This chatbot uses:
- Class-based architecture (OOP)
- Regex pattern matching for intent detection
- Multiple handler methods for different queries
- Random response selection for variety
"""

import random
import re
from datetime import datetime


class SupportBot:
    """A support chatbot using rule-based logic and regex patterns."""
    
    def __init__(self):
        """Initialize the chatbot with response patterns and exit commands."""
        # Exit command patterns
        self.exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "farewell")
        
        # Support response patterns (intent -> regex pattern)
        self.support_responses = {
            'greeting': r'.*\b(hello|hi|hey|greetings|welcome)\b.*',
            'time_query': r'.*\b(time|clock|what\'s the time)\b.*',
            'about_bot': r'.*\b(who are you|your name|what are you|about you)\b.*',
            'help_request': r'.*\b(help|what can you do|capabilities|features)\b.*',
            'jokes': r'.*\b(joke|funny|laugh|humor)\b.*',
            'personalization': r'.*\b(my name is|i\'m|call me)\b.*',
            'gratitude': r'.*\b(thanks|thank you|appreciate)\b.*'
        }
    
    def greet(self):
        """Greet the user when starting."""
        print("\n" + "=" * 60)
        print("Welcome to the Rule-Based Support Chatbot!")
        print("=" * 60)
        print("Type 'help' to see available commands or 'goodbye' to exit.\n")
    
    def handle_greeting(self):
        """Handle greeting responses."""
        responses = (
            "Hello! Welcome! How can I help you today?",
            "Hi there! Great to meet you. What can I assist with?",
            "Greetings! How may I be of service?"
        )
        return random.choice(responses)
    
    def handle_time_query(self):
        """Handle time-related queries."""
        current_time = datetime.now().strftime("%H:%M:%S")
        responses = (
            f"The current time is {current_time}",
            f"Right now it's {current_time}",
            f"It's {current_time} at the moment"
        )
        return random.choice(responses)
    
    def handle_about_bot(self):
        """Handle questions about the bot."""
        responses = (
            "I'm a rule-based support chatbot created for the Coding Samurai internship!",
            "I'm a helpful chatbot assistant. I can answer questions and help you with various tasks.",
            "I'm a support bot built with Python using regex pattern matching."
        )
        return random.choice(responses)
    
    def handle_help_request(self):
        """Handle help requests."""
        return (
            "I can help you with:\n"
            "- Greetings (say hello, hi, etc.)\n"
            "- Tell you the current time\n"
            "- Answer questions about me\n"
            "- Tell you jokes\n"
            "- Remember your name\n"
            "- General chat\n"
            "Type 'goodbye' to exit"
        )
    
    def handle_jokes(self):
        """Handle joke requests."""
        jokes = (
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why did the developer go broke? Because he used up all his cache!",
            "Why do Python developers wear glasses? Because they don't like C#!",
            "Why do Java developers wear glasses? Because they don't C#!"
        )
        return random.choice(jokes)
    
    def handle_personalization(self, reply):
        """Handle personalization (user's name)."""
        name_match = re.search(r'(?:my name is|i\'m|call me)\s+(\w+)', reply, re.IGNORECASE)
        if name_match:
            name = name_match.group(1)
            responses = (
                f"Nice to meet you, {name}! How can I assist you?",
                f"Great to know you, {name}! What can I help with?",
                f"Pleasure to meet you, {name}!"
            )
            return random.choice(responses)
        return "I didn't quite catch that. Can you tell me your name again?"
    
    def handle_gratitude(self):
        """Handle gratitude expressions."""
        responses = (
            "You're welcome! Feel free to ask me anything!",
            "My pleasure! Happy to help!",
            "Always glad to assist!"
        )
        return random.choice(responses)
    
    def handle_no_match_intent(self):
        """Handle unknown inputs."""
        responses = (
            "I didn't quite understand that. Can you rephrase?",
            "Sorry, I'm not sure about that. Can you provide more details?",
            "I'm still learning. Type 'help' to see what I can do!"
        )
        return random.choice(responses)
    
    def match_reply(self, reply):
        """Match user input to pattern and return appropriate response."""
        reply_lower = reply.lower()
        
        # Check each intent pattern
        for intent, pattern in self.support_responses.items():
            if re.search(pattern, reply_lower):
                if intent == 'greeting':
                    return self.handle_greeting()
                elif intent == 'time_query':
                    return self.handle_time_query()
                elif intent == 'about_bot':
                    return self.handle_about_bot()
                elif intent == 'help_request':
                    return self.handle_help_request()
                elif intent == 'jokes':
                    return self.handle_jokes()
                elif intent == 'personalization':
                    return self.handle_personalization(reply_lower)
                elif intent == 'gratitude':
                    return self.handle_gratitude()
        
        # Default response
        return self.handle_no_match_intent()
    
    def make_exit(self, reply):
        """Check if user wants to exit."""
        for command in self.exit_commands:
            if command in reply.lower():
                print("Thank you for reaching out. Have a great day!")
                return True
        return False
    
    def chat(self):
        """Main chat loop."""
        self.greet()
        
        while True:
            # Get user input
            reply = input("You: ").strip()
            
            # Skip empty input
            if not reply:
                continue
            
            # Check for exit command
            if self.make_exit(reply):
                break
            
            # Get and display response
            response = self.match_reply(reply)
            print(f"Bot: {response}\n")


def main():
    """Main function to run the chatbot."""
    bot = SupportBot()
    bot.chat()


if __name__ == "__main__":
    main()
