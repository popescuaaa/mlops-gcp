import random
import datetime
import uuid
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UserPurchase:
    user_id: str
    name: str
    email: str
    location: str
    purchase_value: float
    purchase_date: datetime.datetime


class FakeUserDataGenerator:
    def __init__(self):
        self.first_names = [
            "Emma",
            "Liam",
            "Olivia",
            "Noah",
            "Sophia",
            "Jackson",
            "Ava",
            "Aiden",
            "Isabella",
            "Lucas",
            "Mia",
            "Caden",
            "Amelia",
            "Grayson",
            "Charlotte",
        ]

        self.last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
        ]

        self.european_cities = {
            "France": ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille"],
            "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
            "Italy": ["Rome", "Milan", "Naples", "Turin", "Florence"],
            "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
            "UK": ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool"],
            "Netherlands": [
                "Amsterdam",
                "Rotterdam",
                "Utrecht",
                "The Hague",
                "Eindhoven",
            ],
            "Poland": ["Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan"],
        }

        self.domains = [
            "gmail.com",
            "yahoo.com",
            "hotmail.com",
            "outlook.com",
            "protonmail.com",
        ]
        self.users = {}  # user_id -> (name, email)

    def _generate_user(self) -> Dict[str, Any]:
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        full_name = f"{first_name} {last_name}"

        email_prefix = f"{first_name.lower()}.{last_name.lower()}"
        if random.random() < 0.3:  # 30% chance to add a number
            email_prefix += str(random.randint(1, 99))
        email = f"{email_prefix}@{random.choice(self.domains)}"

        country = random.choice(list(self.european_cities.keys()))
        city = random.choice(self.european_cities[country])
        location = f"{city}, {country}"

        user_id = str(uuid.uuid4())
        self.users[user_id] = (full_name, email)

        return {
            "user_id": user_id,
            "name": full_name,
            "email": email,
            "location": location,
        }

    def _generate_purchase(self, user_id: str, name: str, email: str) -> UserPurchase:
        country = random.choice(list(self.european_cities.keys()))
        city = random.choice(self.european_cities[country])
        location = f"{city}, {country}"

        purchase_value = round(random.uniform(5.0, 500.0), 2)

        # Generate a random date within the last year
        days_ago = random.randint(0, 365)
        purchase_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

        return UserPurchase(
            user_id=user_id,
            name=name,
            email=email,
            location=location,
            purchase_value=purchase_value,
            purchase_date=purchase_date,
        )

    def generate_data(self, num_entries: int = 10000) -> List[UserPurchase]:
        """Generate fake user purchase data"""
        result = []

        # Decide how many unique users we want (between 20-50% of total entries)
        num_unique_users = random.randint(
            int(num_entries * 0.2), int(num_entries * 0.5)
        )

        # Generate unique users
        for _ in range(num_unique_users):
            user = self._generate_user()
            # Each user makes at least one purchase
            result.append(
                self._generate_purchase(user["user_id"], user["name"], user["email"])
            )

        # Generate remaining purchases from existing users
        remaining_entries = num_entries - num_unique_users
        for _ in range(remaining_entries):
            user_id = random.choice(list(self.users.keys()))
            name, email = self.users[user_id]
            result.append(self._generate_purchase(user_id, name, email))

        return result
