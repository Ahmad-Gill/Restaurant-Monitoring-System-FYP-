# python_code/generate_random_value.py
import random
from main_Server.models import GeneratedValue  # Ensure this import works based on your app structure

def generate_random_value():
    value = random.uniform(1.0, 100.0)  # Generate a random float between 1.0 and 100.0
    generated_value = GeneratedValue.objects.create(value=value)  # Store it in the database
    return generated_value
