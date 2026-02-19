# Project 1: Rule-Based Support Chatbot with Regex Pattern Matching

**Coding Samurai AI Internship - Level 1 (Beginner)**

---

## 📋 About Coding Samurai

**Coding Samurai** is a pioneering EdTech startup founded in August 2022 with a mission to bridge the gap between academic knowledge and industry expectations. We offer a comprehensive ecosystem of IT services, technical training internships, and consultancy solutions designed to empower students, professionals, and businesses.

### Our Vision
At Coding Samurai, we envision a future where practical skills and innovation drive success. Our mission is to equip aspiring tech professionals with real-world expertise and help businesses harness the power of technology.

**Learn more:** https://www.codingsamurai.in

---

## 🎯 Project Overview

A **rule-based support chatbot** created using predefined rules and regex pattern matching. The chatbot demonstrates fundamental AI concepts and can greet users, answer basic questions, tell jokes, and provide help information.

### Project Level: **Level 1 (Beginner)**
- **Skills:** Conditional statements, string manipulation, regex pattern matching, OOP
- **Duration:** Part of Coding Samurai Technical Internship Program
- **Date Created:** February 2026

---

## 🏗️ Architecture & Features

### Architecture Highlights
✅ **Class-Based Design** (Object-Oriented Programming)  
✅ **Regex Pattern Matching** (using Python `re` module)  
✅ **Multiple Intent Handlers** (separate methods for each intent)  
✅ **Random Response Variation** (uses `random.choice()` for conversational variety)  
✅ **Clean & Modular Code Structure** (easy to extend and maintain)  

### Chatbot Capabilities
- 🎭 Greeting responses (hello, hi, hey, greetings, welcome)
- 🕐 Tell the current time
- 🤖 Introduce itself
- 😂 Tell random jokes
- ❓ Provide help information
- 👤 Personalized responses based on user name
- 🙏 Gratitude handling
- 👋 Graceful exit handling
- 🎲 Varied responses (multiple options for each response type)

---

## 🛠️ Technologies Used

- **Python 3.x** - Core language
- **re (Regular Expressions)** - Pattern matching for intent detection
- **datetime** - Time-related queries
- **random** - Response variation
- **No external dependencies** - Uses only Python standard library

---

## 📦 Project Structure

```
Project1-Chatbot/
├── chatbot.py          # Main SupportBot class with all logic
├── test_chatbot.py     # Automated test suite (13 test cases)
├── README.md           # Documentation
├── requirements.txt    # Dependencies (none required)
└── __pycache__/        # Python cache files
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed on your system
- No external packages required (standard library only)

### Interactive Chatbot
```bash
python chatbot.py
```
Start a live interactive chat session with the bot.

### Run Test Suite
```bash
python test_chatbot.py
```
Execute automated tests to see all chatbot features in action.

---

## 💬 Example Interactions

```
╔════════════════════════════════════════════════════════════════╗
║           INTERACTIVE CHATBOT CONVERSATION                     ║
╚════════════════════════════════════════════════════════════════╝

You: Hello
Bot: Hi there! Great to meet you. What can I assist with?

You: What's your name?
Bot: I'm a rule-based support chatbot created for the Coding Samurai internship!

You: What time is it?
Bot: Right now it's 21:57:14

You: Help
Bot: I can help you with:
    - Greetings (say hello, hi, etc.)
    - Tell you the current time
    - Answer questions about me
    - Tell you jokes
    - Remember your name
    - General chat
    Type 'goodbye' to exit

You: Tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: My name is Kiruthika
Bot: Nice to meet you, kiruthika! How can I assist you?

You: Thanks
Bot: My pleasure! Happy to help!

You: Goodbye
Bot: Thank you for reaching out. Have a great day!
```

---

## 📚 Code Structure Explanation

### Main Class: `SupportBot`

**Initialization**
```python
def __init__(self):
    # Exit command patterns
    self.exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "farewell")
    
    # Intent recognition patterns (Regex)
    self.support_responses = {
        'greeting': r'.*\b(hello|hi|hey|greetings|welcome)\b.*',
        'time_query': r'.*\b(time|clock|what\'s the time)\b.*',
        'about_bot': r'.*\b(who are you|your name|what are you|about you)\b.*',
        'jokes': r'.*\b(joke|funny|laugh|humor)\b.*',
        'personalization': r'.*\b(my name is|i\'m|call me)\b.*',
        # ... more patterns
    }
```

### Intent Handlers (Methods)
- `handle_greeting()` - Generates greeting responses
- `handle_time_query()` - Returns current time
- `handle_about_bot()` - Bot introduction
- `handle_help_request()` - Lists available features
- `handle_jokes()` - Tells random jokes
- `handle_personalization()` - Extracts and stores user name
- `handle_gratitude()` - Thank you responses
- `handle_no_match_intent()` - Fallback for unknown inputs

### Core Methods
- `match_reply(user_input)` - Matches user input to intent patterns
- `make_exit(user_input)` - Checks if user wants to exit
- `chat()` - Main interactive chat loop
- `greet()` - Initial greeting message

---

## 📊 Test Results

13 comprehensive test cases demonstrating all features:
```
✓ Greeting recognition
✓ Bot identity queries
✓ Time feature
✓ Help information
✓ Joke telling
✓ User personalization
✓ Gratitude handling
✓ Exit command recognition
✓ Varied responses
✓ Unknown input handling
✓ And more...
```

Run `python test_chatbot.py` to see full test output.

---

## 🔄 Intent Recognition Examples

### Regex Patterns Used
```python
'greeting': r'.*\b(hello|hi|hey|greetings|welcome)\b.*'
'time_query': r'.*\b(time|clock|what\'s the time)\b.*'
'about_bot': r'.*\b(who are you|your name|what are you|about you)\b.*'
'help_request': r'.*\b(help|what can you do|capabilities|features)\b.*'
'jokes': r'.*\b(joke|funny|laugh|humor)\b.*'
'personalization': r'.*\b(my name is|i\'m|call me)\b.*'
'gratitude': r'.*\b(thanks|thank you|appreciate)\b.*'
```

---

## 🎓 Skills Learned

Through this project, I have learned and applied:
- ✅ Object-Oriented Programming (Classes and Methods)
- ✅ Regular Expression (Regex) pattern matching using `re` module
- ✅ String manipulation and processing
- ✅ Conditional logic (if/elif/else)
- ✅ User input handling and validation
- ✅ Program flow control and loops
- ✅ Function organization and architecture
- ✅ Random selection for response variety
- ✅ Time handling with datetime module
- ✅ Code modularity and maintainability

---

## 🚀 Future Enhancement Ideas

- Integrate NLP libraries (NLTK, spaCy)
- Add sentiment analysis
- Implement conversation history/persistence
- Add context awareness for follow-up questions
- Integrate with external APIs
- Build a GUI interface (Tkinter/PyQt)
- Add machine learning for intent classification
- Implement conversation logging
- Add multi-language support
- Database integration for storing responses

---

## 📜 Submission Details

**Repository:** https://github.com/KiruthikaSelvaraj1/CODING-SAMURAI-INTERNSHIP-TASK

**Project Type:** Artificial Intelligence - Level 1 (Beginner)

**Completed By:** February 2026

**Internship Program:** Coding Samurai Technical Internship

---

## 🤝 Connect with Coding Samurai

- **Website:** https://www.codingsamurai.in
- **LinkedIn:** [Coding Samurai](https://www.linkedin.com/company/coding-samurai)
- **Email:** support@codingsamurai.in
- **Telegram:** Coding Samurai

---

## 📝 License & Attribution

Created as part of the **Coding Samurai AI Internship Program (Level 1 - Beginner)**

---

## 🏆 Hashtags

`#CodingSamurai` `#AIInternship` `#Chatbot` `#Python` `#RegexPatternMatching` `#OOP` `#RuleBasedAI` `#TechnicalInternship` `#EdTech`

---

**Status:** ✅ Project Completed and Published  
**Last Updated:** February 19, 2026
