import pandas as pd
import random
from faker import Faker

df = pd.read_csv("/Users/anne/PycharmProjects/ep_project/data/breast-cancer_train.csv")

# Anzahl der zufällig zu generierenden Einträge
num_entries = len(df)

# Faker-Instanz erstellen
fake = Faker()

# Liste zur Speicherung der generierten Namen und Altersangaben
names = []
ages = []

for _ in range(num_entries):
    # Zufälligen Namen generieren
    name = fake.name()
    # Zufälliges Alter zwischen 18 und 100 generieren
    age = random.randint(18, 100)
    # Name und Alter zu den Daten hinzufügen
    names.append(name)
    ages.append(age)


df["Name"] = names
df["Age"] = ages
print(df)

csv_file_path = "updated_breast_cancer_train.csv"
df.to_csv(csv_file_path, index=False)

