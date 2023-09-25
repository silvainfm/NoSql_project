# Chatbot using Docker & Redis

This project implements a simple chatbot using Python and Redis. The chatbot provides an interface where users can interact with the bot, join channels, send messages, and receive messages. Additionally, users can request weather updates and fun facts, and they can identify themselves to the bot. 

## Features
- User Identification: Users can identify themselves with a username, and store their age, gender, and location in the Redis database.
- Channel Management: Users can join or leave channels. When a user sends a message to a channel, all users subscribed to that channel will receive the message.
- Messaging: Users can send direct messages to the chatbot and read messages from channels they've joined.
- Command Processing: The chatbot recognizes the following commands:
- !help: Provides a list of available commands.
- !weather <city>: Provides a mock weather update for the given city.
- !fact: Provides a random fun fact.
- !whoami: Provides information about the user based on their username.
- Weather and Fun Facts: The chatbot can provide mock weather updates and random fun facts from a predefined list stored in Redis.
