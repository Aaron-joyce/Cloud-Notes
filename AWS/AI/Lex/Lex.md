# Amazon Lex

Amazon Lex is a service for building conversational interfaces into any application using voice and text. It provides the advanced deep learning functionalities of automatic speech recognition (ASR) and natural language understanding (NLU).

## Conversational AI Engine

### Building Chatbots
Lex allows developers to build sophisticated, conversational AI chatbots. It is powered by the same technology engine that drives Amazon Alexa.

### Core Concepts
- **Intents**: An action that the user wants to perform (e.g., `BookFlight`, `OrderPizza`).
- **Utterances**: Spoken or typed phrases that trigger an intent (e.g., "I want to book a flight", "Can I order a pizza?").
- **Slots**: Data the user must provide to fulfill the intent (e.g., `DestinationCity`, `PizzaSize`).
- **Fulfillment**: The backend logic (usually an AWS Lambda function) that executes the action once all required slots are filled.

### Multi-Channel Integration
Bots built in Lex can be easily deployed across multiple platforms, including web applications, mobile apps, Slack, Facebook Messenger, and Amazon Connect (AWS's cloud contact center).
