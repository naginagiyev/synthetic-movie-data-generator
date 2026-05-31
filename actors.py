import random
import pandas as pd
from tqdm import tqdm
from faker import Faker

# initialize faker for name generation
faker = Faker()

# total number of actors to generate
ACTOR_COUNT = 5000

# the generated ids' range
ID_MIN = 100000
ID_MAX = 999999

# birth year range
BIRTH_YEAR_MIN = 1900
BIRTH_YEAR_MAX = 2016

# nationalities list
NATIONALITIES = [
    "United States", "Canada", "Mexico", "United Kingdom", "France", 
    "Germany", "Italy", "Spain", "Portugal", "Netherlands", "Belgium", 
    "Switzerland", "Austria", "Sweden", "Norway", "Denmark", "Finland", 
    "Iceland", "Ireland", "Colombia", "Venezuela", "Ecuador", "Cuba"
]

# lists to store data
actorIds = []
actorNames = []
birthYears = []
nationalities = []

# set to store used ids (to avoid duplicates)
usedActorIds = set()

# generate actors with tqdm progress bar
for _ in tqdm(range(ACTOR_COUNT), desc="Generating actors"):
    # generate unique actor ID
    while True:
        actorId = random.randint(ID_MIN, ID_MAX)
        if actorId not in usedActorIds:
            usedActorIds.add(actorId)
            actorIds.append(actorId)
            break
    
    # generate actor name
    actorName = faker.name()
    actorNames.append(actorName)
    
    # generate birth year
    birthYear = random.randint(BIRTH_YEAR_MIN, BIRTH_YEAR_MAX)
    birthYears.append(birthYear)
    
    # generate nationality
    nationality = random.choice(NATIONALITIES)
    nationalities.append(nationality)

# convert the data into dataframe
df = pd.DataFrame({
    "actorID": actorIds,
    "actorName": actorNames,
    "birthYear": birthYears,
    "nationality": nationalities
})

# save the dataset as CSV
df.to_csv("./tables/actors.csv", index=False)