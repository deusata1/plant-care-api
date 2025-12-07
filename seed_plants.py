from sqlmodel import Session
from main import Plant, engine

# List of sample plants to insert
PLANTS_TO_SEED = [
    {"name": "Front Hedge", "species": "Hibiscus", "location": "Front yard"},
    {"name": "Driveway Border", "species": "Ixora", "location": "Driveway"},
    {"name": "Back Fence Screen", "species": "Clusia", "location": "Back fence"},
    {"name": "Pool Accent", "species": "Areca palm", "location": "Pool deck"},
    {"name": "Corner Shade Tree", "species": "Live oak", "location": "Front corner"},
    {"name": "Butterfly Garden", "species": "Pentas", "location": "Side yard"},
    {"name": "Bird Garden", "species": "Firebush", "location": "Back corner"},
    {"name": "Color Pot 1", "species": "Croton", "location": "Front entry"},
    {"name": "Color Pot 2", "species": "Ti plant", "location": "Front entry"},
    {"name": "Mailbox Planting", "species": "Bougainvillea", "location": "Mailbox"},
    {"name": "Rock Bed Accent", "species": "Lantana", "location": "Rock bed"},
    {"name": "Palm Cluster", "species": "Sabal palm", "location": "Back corner"},
    {"name": "Shade Groundcover", "species": "Mondo grass", "location": "Under oak"},
    {"name": "Native Feature", "species": "Coontie", "location": "Native bed"},
    {"name": "Tropical Screen", "species": "Heliconia", "location": "Side fence"},
    {"name": "Feature Palm", "species": "Travelers palm", "location": "Back center"},
    {"name": "Patio Container", "species": "Bird of paradise", "location": "Patio"},
    {"name": "Accent Tree", "species": "Royal poinciana", "location": "Front yard"},
    {"name": "Driveway Palm", "species": "Areca palm", "location": "Driveway island"},
    {"name": "Entry Planting", "species": "Hibiscus", "location": "Front walk"},
]

def main():
    with Session(engine) as session:
        for p in PLANTS_TO_SEED:
            plant = Plant(**p)
            session.add(plant)
        session.commit()
        print(f"Seeded {len(PLANTS_TO_SEED)} plants.")

if __name__ == "__main__":
    main()
