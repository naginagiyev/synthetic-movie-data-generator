import random
import pandas as pd
from tqdm import tqdm
from faker import Faker

# initialize faker for name generation
faker = Faker()

# total number of directors to generate
DIRECTOR_COUNT = 1000

# the generated ids' range
ID_MIN = 100000
ID_MAX = 999999

# birth year range for directors
BIRTH_YEAR_MIN = 1880
BIRTH_YEAR_MAX = 1990

# lists to store data
directorIds = []
directorNames = []
birthYears = []

# set to store used ids (to avoid duplicates)
usedDirectorIds = set()

# generate directors with tqdm progress bar
for _ in tqdm(range(DIRECTOR_COUNT), desc="Generating directors"):
    # generate unique director ID
    while True:
        directorId = random.randint(ID_MIN, ID_MAX)
        if directorId not in usedDirectorIds:
            usedDirectorIds.add(directorId)
            directorIds.append(directorId)
            break
    
    # generate director name
    directorName = faker.name()
    directorNames.append(directorName)
    
    # generate birth year
    birthYear = random.randint(BIRTH_YEAR_MIN, BIRTH_YEAR_MAX)
    birthYears.append(birthYear)

# convert the data into dataframe
df = pd.DataFrame({
    "directorID": directorIds,
    "directorName": directorNames,
    "birthYear": birthYears
})

# save the dataset as CSV
df.to_csv("./tables/directors.csv", index=False)