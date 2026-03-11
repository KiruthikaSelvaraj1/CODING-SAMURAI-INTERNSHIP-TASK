# Rule-Based Support Chatbot

A Python-powered rule-based chatbot that provides automated customer support with intelligent intent detection and natural responses.

## Features

- **Smart Greetings** - Welcomes users with friendly, varied responses
- **Time Information** - Provides current time on request
- **Bot Introduction** - Tells users about itself and its capabilities
- **Entertainment** - Shares programming jokes to lighten the mood
- **Personalization** - Remembers user names for conversational context
- **Help System** - Lists all available commands and features
- **Gratitude Handling** - Responds warmly to thanks and appreciation
- **Graceful Exit** - Handles goodbye messages professionally
- **Unknown Intent Handling** - Gracefully manages unrecognized inputs

## Technical Implementation

### Architecture

The chatbot follows Object-Oriented Programming (OOP) principles with a modular class-based design:

```python
class SupportBot:
    def __init__(self):
        # Initialize response patterns and configurations
```

### Intent Detection

Uses regex pattern matching for efficient and accurate user intent recognition:

```python
self.support_responses = {
    'greeting': r'.*\b(hello|hi|hey|greetings|welcome)\b.*',
    'time_query': r'.*\b(time|clock|what\'s the time)\b.*',
    'about_bot': r'.*\b(who are you|your name|what are you|about you)\b.*',
    'help_request': r'.*\b(help|what can you do|capabilities|features)\b.*',
    'jokes': r'.*\b(joke|funny|laugh|humor)\b.*',
    'personalization': r'.*\b(my name is|i\'m|call me)\b.*',
    'gratitude': r'.*\b(thanks|thank you|appreciate)\b.*'
}
```

### Response System

- **Dedicated Handlers** - Each intent has a specialized method for clean separation of concerns
- **Random Variation** - Uses `random.choice()` to provide diverse responses
- **User Memory** - Extracts and stores user information for personalization

## Getting Started

### Prerequisites

- Python 3.x installed on your system

###No external dependencies required - uses only Python standard library modules (datetime, random, re)Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Chatbot

```bash
python chatbot.py
```

## Project Structure

```
Project1-Chatbot/
├── chatbot.py          # Main chatbot implementation
├── index.html          # Web interface
├── test_chatbot.py     # Unit tests
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Key Components

| File | Description |
|------|-------------|
| `chatbot.py` | Core chatbot logic with SupportBot class |
| `index.html` | Interactive web-based chat interface |
| `test_chatbot.py` | Test suite for validating functionality |
| `requirements.txt` | Lists all Python package dependenciand main chat loop |
| `test_chatbot.py` | Automated test suite demonstrating all chatbot features |
| `requirements.txt` | Python dependency information |
| `index.html` | Web-based interface |
| `README.md` | Project documentation
- **Python 3.x** - Primary programming lanintent pattern matching
- **datetime Module** - Current time operations
- **random Module** - Response randomization for varied interactionsions
- **random** - Response randomization

## Sample Conversation

```
You: hello
Bot: Hello! Welcome! How can I help you today?

You: what's the time?
Bot: The current time is 14:35:22
o are you?
Bot: I'm a rule-based support chatbot created for the Coding Samurai internship!

You: what's the time?
Bot: The current time is 14:35:22

You: tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: my name is John
Bot: Nice to meet you, John! How can I assist you?

You: thanks
Bot: You're welcome! Feel free to ask me anything!
Bot: Thank you for reaching out. Have a great day!
```

## License
This project is for educational purposes.


This project is for educational purposes.

