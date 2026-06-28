from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

PLATFORMS = ["Twitter", "Instagram", "Facebook", "YouTube", "LinkedIn", "Reddit"]

BRANDS = ["Samsung", "Apple", "Zomato", "Swiggy", "Flipkart", "Amazon"]

LOCATIONS = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad", "Salem", "Coimbatore"]

LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Kannada"]

DEVICES = ["Mobile", "Desktop", "Tablet"]

POSITIVE_TEMPLATES = [
    "Absolutely love {brand}! Best product ever.",
    "{brand} customer service is outstanding. Highly recommended!",
    "Just received my order from {brand}. Super fast delivery!",
    "{brand} never disappoints. 5 stars always.",
    "Switched to {brand} and never looking back. Amazing quality.",
    "Great experience with {brand} today. Keep it up!",
]

NEGATIVE_TEMPLATES = [
    "{brand} delivered a damaged product. Very disappointed.",
    "Worst experience with {brand} customer support ever.",
    "{brand} app keeps crashing. Please fix this!",
    "Waited 2 weeks for {brand} delivery. Unacceptable.",
    "Overcharged by {brand}. Still waiting for refund.",
    "{brand} quality has gone down badly. Not worth the price.",
]

NEUTRAL_TEMPLATES = [
    "Just bought something from {brand}. Let's see how it goes.",
    "Comparing {brand} with other options before deciding.",
    "{brand} has new offers this week. Checking it out.",
    "Anyone else use {brand}? What's your experience?",
    "Thinking of switching to {brand}. Any suggestions?",
]

def generate_sentiment_data(n=100000):
    records = []
    base_date = datetime(2024, 1, 1)

    for i in range(n):
        brand = random.choice(BRANDS)
        sentiment = random.choices(
            ["POSITIVE", "NEGATIVE", "NEUTRAL"],
            weights=[0.40, 0.30, 0.30]
        )[0]

        if sentiment == "POSITIVE":
            template = random.choice(POSITIVE_TEMPLATES)
            polarity = round(random.uniform(0.3, 1.0), 3)
        elif sentiment == "NEGATIVE":
            template = random.choice(NEGATIVE_TEMPLATES)
            polarity = round(random.uniform(-1.0, -0.3), 3)
        else:
            template = random.choice(NEUTRAL_TEMPLATES)
            polarity = round(random.uniform(-0.2, 0.2), 3)

        post_text = template.format(brand=brand)
        post_date = (base_date + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        likes = random.randint(0, 50000) if sentiment == "POSITIVE" else random.randint(0, 5000)

        records.append({
            "post_id": f"POST{str(i+1).zfill(7)}",
            "post_date": post_date,
            "platform": random.choice(PLATFORMS),
            "brand": brand,
            "post_text": post_text,
            "username": fake.user_name(),
            "location": random.choice(LOCATIONS),
            "language": random.choice(LANGUAGES),
            "device": random.choice(DEVICES),
            "likes": likes,
            "shares": random.randint(0, likes // 10 + 1),
            "comments": random.randint(0, likes // 5 + 1),
            "follower_count": random.randint(10, 1000000),
            "polarity_score": polarity,
            "sentiment_label": sentiment,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    print("Generating 100,000 social media records...")
    df = generate_sentiment_data(100000)
    df.to_csv("social_media_posts_100k.csv", index=False)
    print(f"Done! Generated {len(df)} records")
    print(f"Sentiment distribution:")
    print(df["sentiment_label"].value_counts().to_string())
    print(f"Top brands:")
    print(df["brand"].value_counts().to_string())
