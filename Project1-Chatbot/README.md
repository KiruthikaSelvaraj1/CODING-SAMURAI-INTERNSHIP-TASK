# Project 1: Rule-Based Support Chatbot (Upgraded)

## Overview
A rule-based support chatbot created as part of the Coding Samurai AI Internship (Level 1 - Beginner).

The chatbot uses **class-based architecture** and **regex pattern matching** to respond to user inputs. It can greet users, answer basic questions, tell jokes, and provide help information.

## Architecture Features
✅ **Class-Based Design** (OOP Principles)  
✅ **Regex Pattern Matching** (using Python `re` module)  
✅ **Multiple Intent Handlers** (separate methods for each intent)  
✅ **Random Response Variation** (uses `random.choice()` for variety)  
✅ **Clean Code Structure** (easy to extend and maintain)  

## Skills Learned
- Object-Oriented Programming (Classes and Methods)
- Regex pattern matching and `re.search()`
- Conditional statements (if/elif/else)
- String manipulation and processing
- User input handling
- Program flow control
- Function organization and architecture

## Features
✅ Greeting responses (hello, hi, hey, greetings)  
✅ Tell the current time  
✅ Introduce itself  
✅ Tell random jokes  
✅ Provide help information  
✅ Personalized responses based on user name  
✅ Graceful exit handling  
✅ Varied responses (multiple options for each response type)  

## How to Run

### Prerequisites
- Python 3.x installed on your system

### Running the Interactive Chatbot
```bash
python chatbot.py
```

### Running the Demo (All Features)
```bash
python demo.py
```

### Running Tests
```bash
python test_chatbot.py
```

## Example Interactions
```
You: Hello
Bot: Hi there! Great to meet you. What can I assist with?

You: What's your name?
Bot: I'm a rule-based support chatbot created for the Coding Samurai internship!

You: What time is it?
Bot: Right now it's 11:35:12

You: Tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: My name is Sarah
Bot: Nice to meet you, sarah! How can I assist you?

You: Thanks
Bot: My pleasure! Happy to help!

You: Goodbye
Bot: Thank you for reaching out. Have a great day!
```

## Project Structure
```
Project1-Chatbot/
├── chatbot.py          # Main chatbot with SupportBot class
├── demo.py             # Simple demo script for video
├── test_chatbot.py     # Automated test script
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Code Explanation

### Main Components

1. **SupportBot Class**
   - Initialization: Stores exit commands and regex patterns
   - Pattern matching: Uses `re.search()` for intent detection

2. **Intent Handlers** (Methods)
   - `handle_greeting()` - Greeting responses
   - `handle_time_query()` - Time display
   - `handle_about_bot()` - Bot information
   - `handle_help_request()` - Available features
   - `handle_jokes()` - Random jokes
   - `handle_personalization()` - User name extraction
   - `handle_gratitude()` - Thank you responses
   - `handle_no_match_intent()` - Unknown input handling

3. **Main Methods**
   - `match_reply()` - Matches input to intents using regex
   - `make_exit()` - Checks if user wants to exit
   - `chat()` - Main chat loop
   - `greet()` - Greeting message

### Regex Patterns Used
```python
'greeting': r'.*\b(hello|hi|hey|greetings|welcome)\b.*'
'time_query': r'.*\b(time|clock|what\'s the time)\b.*'
'about_bot': r'.*\b(who are you|your name|what are you|about you)\b.*'
'jokes': r'.*\b(joke|funny|laugh|humor)\b.*'
'personalization': r'.*\b(my name is|i\'m|call me)\b.*'
```

## Future Enhancements
- Add more regex patterns for new intents
- Implement sentiment analysis
- Add database of responses
- Integrate with NLP library (NLTK, spaCy)
- Add conversation history/persistence
- Implement context awareness

## Technologies Used
- Python 3.x
- Regular Expressions (re module)
- datetime module
- random module

## Author
Created during Coding Samurai AI Internship (2026)

## References
- Coding Samurai: https://www.codingsamurai.in
- YouTube Reference: How to Build a Simple Chatbot
- Python re module: https://docs.python.org/3/library/re.html

---
**Hashtags:** #CodingSamurai #AIInternship #Chatbot #Python #RegexPatternMatching #OOP
