import redis 
import json

client = redis.StrictRedis(host='mp1', port=6379, db=0)

# Weather data by city
client.hset('weather:Memphis', mapping={
    'temperature': '26°C',
    'condition': 'Cloudy',
    'wind_speed': '30 km/h'
})

client.hset('weather:Nashville', mapping={
    'temperature': '28°C',
    'condition': 'AS ALWAYS HOT & HUMID',
    'wind_speed': '5 km/h'
})

client.hset('weather:Louisville', mapping={
    'temperature': '23°C',
    'condition': 'RAINY',
    'wind_speed': '10 km/h'
})

client.hset('weather:Cincinnati', mapping={
    'temperature': '21°C',
    'condition': 'INDIAN SUMMER',
    'wind_speed': '15 km/h'
})

client.hset('weather:Columbus', mapping={
    'temperature': '17°C',
    'condition': 'FALLY',
    'wind_speed': '20 km/h'
})

client.hset('weather:Jacksonville', mapping={
    'temperature': '30°C',
    'condition': 'HOT & STORMY',
    'wind_speed': '60 km/h'
})

# fun facts
client.rpush('funfacts', 'Monaco is its own country.')
client.rpush('funfacts', 'Male whales have a penis.')
client.rpush('funfacts', 'Friends premiered almost 30 years ago.')
client.rpush('funfacts', 'Monaco is the 2nd smallest country in the world.')
client.rpush('funfacts', 'Transformers are great.')
client.rpush('funfacts', 'We love redis.')

# Adding users
user_1 = {
    'username': 'Otis Doe',
    'age': '19',
    'gender': 'Male',
    'location': 'London'
}

user_2 = {
    'username': 'Maeve Doe',
    'age': '30',
    'gender': 'Female',
    'location': 'New York'
}

user3 = {
    'username': 'Eric Doe',
    'age': '30',
    'gender': 'Male',
    'location': 'Hogsmeade'
}

user3 = {
    'username': 'Jean Doe',
    'age': '45',
    'gender': 'Female',
    'location': 'The Shire'
}

client.set(user_1['username'], json.dumps(user_1))
client.set(user_2['username'], json.dumps(user_2))
