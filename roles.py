import random
import pandas as pd
import numpy as np
from tqdm import tqdm
from faker import Faker

faker = Faker()

ROW_COUNT = 200000

# load existing CSVs
moviesDf = pd.read_csv("./tables/movies.csv")
actorsDf = pd.read_csv("./tables/actors.csv")

# precompute eligible actors per unique release year
# an actor must be born at least 6 years before the movie's release year
uniqueReleaseYears = moviesDf["releaseDate"].unique()
yearToEligibleActors = {}
for year in tqdm(uniqueReleaseYears, desc="Precomputing eligible actors per year"):
    eligible = actorsDf[actorsDf["birthYear"] <= year - 6]["actorID"].tolist()
    if not eligible:
        # fallback: use the oldest available actor(s)
        eligible = actorsDf.nsmallest(1, "birthYear")["actorID"].tolist()
    yearToEligibleActors[year] = eligible

# map each movieID to its eligible actor list
movieIdList = moviesDf["movieID"].tolist()
movieReleaseYearMap = dict(zip(moviesDf["movieID"], moviesDf["releaseDate"]))
movieEligibleActors = {mid: yearToEligibleActors[movieReleaseYearMap[mid]] for mid in movieIdList}

# build reverse mapping: actorID → eligible movieIDs
# needed to seed exactly one role for every actor in phase 1
actorBirthYearMap = dict(zip(actorsDf["actorID"], actorsDf["birthYear"]))
actorEligibleMovies = {}
for aid, byear in tqdm(actorBirthYearMap.items(), desc="Precomputing eligible movies per actor"):
    eligible = moviesDf.loc[moviesDf["releaseDate"] >= byear + 6, "movieID"].tolist()
    if not eligible:
        eligible = moviesDf.nlargest(1, "releaseDate")["movieID"].tolist()
    actorEligibleMovies[aid] = eligible

allActorIds = actorsDf["actorID"].tolist()

def generateRoleName():
    return faker.first_name() if random.random() < 0.5 else faker.name()

roleNames = []
roleMovieIds = []
roleActorIds = []
usedPairs = set()

# phase 1: guarantee every actor appears in at least one role
with tqdm(total=len(allActorIds), desc="Phase 1 — seeding one role per actor") as pbar:
    for actorId in allActorIds:
        while True:
            movieId = random.choice(actorEligibleMovies[actorId])
            pair = (movieId, actorId)
            if pair not in usedPairs:
                usedPairs.add(pair)
                roleMovieIds.append(movieId)
                roleActorIds.append(actorId)
                roleNames.append(generateRoleName())
                pbar.update(1)
                break

# phase 2: fill the remaining rows with random roles
with tqdm(total=ROW_COUNT - len(allActorIds), desc="Phase 2 — filling remaining roles") as pbar:
    while len(roleMovieIds) < ROW_COUNT:
        movieId = random.choice(movieIdList)
        actorId = random.choice(movieEligibleActors[movieId])
        pair = (movieId, actorId)
        if pair in usedPairs:
            continue
        usedPairs.add(pair)
        roleMovieIds.append(movieId)
        roleActorIds.append(actorId)
        roleNames.append(generateRoleName())
        pbar.update(1)

# build and save the dataframe
df = pd.DataFrame({
    "movieID": roleMovieIds,
    "actorID": roleActorIds,
    "roleName": roleNames
})

df.to_csv("./tables/roles.csv", index=False)
print(f"roles.csv saved with {len(df):,} rows.")