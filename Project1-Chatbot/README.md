# Rule-Based Support Chatbot

## Project Overview

Welcome to our **Rule-Based Support Chatbot**! 🎉 This is an exciting Python-powered chatbot designed to provide automated customer support with a touch of personality. The chatbot can:

- Greet users with a warm welcome
- Tell you the current time
- Introduce itself and tell you about its capabilities
- Lighten your day with hilarious jokes
- Provide helpful information about what it can do
- Remember your name for a personalized experience
- Handle thank you messages gracefully
- Say goodbye when you're ready to leave

## Technical Implementation

This project showcases some amazing technical concepts:

### 1. Object-Oriented Programming (OOP) ✨
We've created a powerful `SupportBot` class that encapsulates all the chatbot logic in a clean, maintainable way:
```python
class SupportBot:
    def __init__(self):
        # Setup patterns and responses
```

### 2. Regex Pattern Matching 🔍
We leverage Python's awesome `re` module to intelligently detect user intentions:
```python
self.support_responses = {
    'greeting': r'.*\b(hello|hi|hey)\b.*',
    'time_query': r'.*\b(time|clock)\b.*',
    'jokes': r'.*\b(joke|funny)\b.*',
}
```

### 3. Intent Handlers 🎯
Each intent gets its own dedicated method for clean, organized code:
- `handle_greeting()` - Welcomes users warmly
- `handle_time_query()` - Shows you the current time
- `handle_jokes()` - Shares hilarious jokes
- `handle_personalization()` - Remembers your name
- And many more exciting features!

### 4. Random Response Variation 🌈
We use `random.choice()` to keep conversations fresh and natural - you'll never get the same response twice!

## How to Run

Ready to try it out? Here's how to get started:

```bash
python chatbot.py
```

## Project Structure

Here's what's included in this exciting project:

- `chatbot.py` - The main chatbot implementation 🚀
- `index.html` - A beautiful web interface for the chatbot
- `test_chatbot.py` - Comprehensive unit tests
- `requirements.txt` - Python dependencies

## Technologies Used

- **Python 3.x** - The powerhouse behind our chatbot
- **re (Regular Expressions)** - For smart pattern matching
- **datetime** - For time-related features
- **random** - For adding variety to responses


