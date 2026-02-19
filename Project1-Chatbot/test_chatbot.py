"""
Test script for the Rule-Based Chatbot
Demonstrates all features without requiring interactive input
"""

from chatbot import SupportBot

def test_chatbot():
    """Run test cases for the chatbot."""
    
    # Create bot instance
    bot = SupportBot()
    
    test_cases = [
        "Hello",
        "Hi there",
        "What's your name?",
        "Who are you?",
        "What time is it?",
        "Help",
        "What can you do?",
        "Tell me a joke",
        "Make me laugh",
        "My name is Alex",
        "Thanks",
        "Thank you",
        "Goodbye",
    ]
    
    print("=" * 60)
    print("CHATBOT TEST RESULTS")
    print("=" * 60)
    
    for user_input in test_cases:
        response = bot.match_reply(user_input)
        print(f"\n-> User: {user_input}")
        print(f"-> Bot: {response}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_chatbot()
