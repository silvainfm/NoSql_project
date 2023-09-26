import redis
import json
import random

class Chatbot:
    def __init__(self, host='redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = None

    def introduce(self):
        # Provide an introduction and list of commands
        intro = """
        Your bot's introduction goes here
        Here are the commands this bot supports:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        and anything else you enabled your bot to do
        """
        print(intro)

    def identify(self, username, age, gender, location):
        # Store user details in Redis
        user_data = {
            'age': age,
            'gender': gender,
            'location': location,
        }
        self.client.set(username, json.dumps(user_data))
        self.username = username

    def join_channel(self, channel):
        # Join a channel
        self.pubsub.subscribe(channel)
        print(f"Joined channel {channel}")

    def leave_channel(self, channel):
        # Leave a channel
        self.pubsub.unsubscribe(channel)
        print(f"Left channel {channel}")

    def send_message(self, channel, message):
        # Send a message to a channel
        self.client.publish(channel, f"{self.username}: {message}")
        print(f"Sent message to {channel}")

    def read_message(self, channel):
        # Read messages from a channel
        for item in self.pubsub.listen():
            if item['type'] == 'message':
                print(f"Received in {item['channel'].decode()}: {item['data'].decode()}")

    def read_direct_messages(self):
        if not self.username:
            print('You must identify yourself before reading messages.')
            return

        messages = self.client.lrange(self.username, 0, -1)
        for message_json in messages:
            message_data = json.loads(message_json)
            print(f"{message_data['sender']}: {message_data['message']}")

        # Clear the message list after reading
        self.client.delete(self.username)

    def process_commands(self, message):
        # Handle special chatbot commands
        if message.startswith('!help'):
            self.introduce()

        elif message.startswith('!weather'):
            city = message.split(' ')[1]
            weather_data = self.get_weather(city)
            print(weather_data)

        elif message == '!fact':
            fact = self.get_fun_facts()
            print(fact)

        elif message == '!whoami':
            if not self.username:
                print("You have not identified yourself.")
            else:
                user_data = json.loads(self.client.get(self.username))
                print(f'Username: {self.username}')
                print(f"Age: {user_data['age']}")
                print(f"Gender: {user_data['gender']}")
                print(f"Location: {user_data['location']}")

    def get_weather(self, city):
        data = self.client.hgetall(f'weather:{city}')
        if data:
            response = f"Weather in {city}:\n"
            response += f"Temperature: {data[b'temperature'].decode()}\n"
            response += f"Condition: {data[b'condition'].decode()}\n"
            response += f"Wind Speed: {data[b'wind_speed'].decode()}"
            return response
        else:
            return f"No weather data available for {city}"

    def get_fun_facts(self):
        fact = self.client.lindex('funfacts', random.randint(0, self.client.llen('funfacts') - 1))
        return fact.decode() if fact else "No fun facts available."

    def direct_message(self, recipient, message):
        # Send a direct message to the chatbot
        if not self.username:
            print('You must identify yourself before sending messages.')
            return

        message_data = {
            'sender': self.username,
            'message': message
        }

        # Convert message data to a JSON string
        message_json = json.dumps(message_data)

        # Append the message JSON string to the recipient's list of messages
        self.client.rpush(recipient, message_json)
        print(f'Message sent to {recipient}')

if __name__ == "__main__":
    bot = Chatbot()
    bot.introduce()

    while True:
        print("""
        Menu:
        1. Send a message
        2. Join a channel
        3. Leave a channel
        4. Send a direct message
        5. Read direct messages
        6. Identify yourself
        7. Process commands
        8. Read channel messages
        9. Exit
        """)

        choice = input("Choose an option: ")

        if choice == '1':
            channel = input("Enter channel name: ")
            message = input("Enter message: ")
            bot.send_message(channel, message)
        elif choice == '2':
            channel = input("Enter channel name: ")
            bot.join_channel(channel)
        elif choice == '3':
            channel = input("Enter channel name: ")
            bot.leave_channel(channel)
        elif choice == '4':
            recipient = input("Enter recipient username: ")
            message = input("Enter message: ")
            bot.direct_message(recipient, message)
        elif choice == '5':
            bot.read_direct_messages()
        elif choice == '6':
            username = input("Enter username: ")
            age = input("Enter age: ")
            gender = input("Enter gender: ")
            location = input("Enter location: ")
            bot.identify(username, age, gender, location)
        elif choice == '7':
            message = input("Enter command: ")
            bot.process_commands(message)
        elif choice == '8':
            bot.read_message(input("Enter channel name: "))
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")