import random
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker("en_IN")
engine = create_engine("postgresql+psycopg://app:app@localhost:5433/propsearch")

LOCALITIES = ["Baner", "Wakad", "Hinjewadi", "Kharadi", "Viman Nagar",
              "Hadapsar", "Aundh", "Koregaon Park", "Pimple Saudagar", "Kothrud"]
AMENITIES = ["gym", "pool", "clubhouse", "garden", "security", "lift",
             "power backup", "play area", "metro nearby", "school nearby"]

rows = []
for _ in range(2000):
    bhk = random.choice([1, 2, 2, 3, 3, 4])
    loc = random.choice(LOCALITIES)
    area = bhk * random.randint(350, 550)
    price = area * random.randint(7000, 14000)
    status = random.choice([0, 0, 1])
    rows.append({
        "title": f"{bhk} BHK in {fake.company()} {random.choice(['Heights','Residency','Park','Greens'])}, {loc}",
        "description": fake.paragraph(nb_sentences=3),
        "locality": loc, "bhk": bhk, "price": price, "area_sqft": area,
        "parking": random.random() < 0.7, "possession_status": status,
        "amenities": str(random.sample(AMENITIES, k=random.randint(2, 6))).replace("'", '"'),
    })

with engine.begin() as conn:
    conn.execute(text("""
        INSERT INTO properties (title, description, locality, bhk, price, area_sqft,
                                parking, possession_status, amenities)
        VALUES (:title, :description, :locality, :bhk, :price, :area_sqft,
                :parking, :possession_status, CAST(:amenities AS jsonb))
    """), rows)
print("Seeded", len(rows))