import nltk
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from faker import Faker
from collections import Counter
from nltk.corpus import wordnet, brown

# download corpuses
nltk.download('brown', quiet=True)
nltk.download('wordnet', quiet=True)

# initialize faker for name generation
faker = Faker()

# total data
MOVIE_COUNT = 10000

# the generated ids' range
ID_MIN = 100000
ID_MAX = 999999

# the range of years for movies release date
RELEASE_YEAR_MIN = 1920
RELEASE_YEAR_MAX = 2026

# the range of duration for movies
DURATION_MIN = 60
DURATION_MAX = 225

# the probabilities used in title generation
ARTICLE_PROBABILITY = 0.5
ADJECTIVE_PROBABILITY = 0.5

# load existing directors from CSV
directorsDf = pd.read_csv("./tables/directors.csv")

# lists to store data
movieIds = []
durations = []
movieTitles = []
releaseDates = []
movieDirectorIds = []
genres = []

# sets to store used ids (for not to use second time)
usedMovieIds = set()

# movie genres
movieGenres = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "History",
    "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi",
    "Short", "Sport", "Thriller", "War", "Western"
]

# get all nouns from the corpus
nouns = list(set(
    word.replace('_', ' ')
    for syn in wordnet.all_synsets('n')
    for word in syn.lemma_names()
    if '_' not in word and word.isalpha()
))

# get all adjectives from the corpus
adjectives = list(set(
    word.replace('_', ' ')
    for syn in wordnet.all_synsets('a')
    for word in syn.lemma_names()
    if '_' not in word and word.isalpha()
))

# count words (to select only most used words)
wordFreq = Counter(word.lower() for word in brown.words())

# select only most used 10,000 nouns and adjectives
nounsWithFreq = [(noun, wordFreq.get(noun, 0)) for noun in nouns]
adjectivesWithFreq = [(adj, wordFreq.get(adj, 0)) for adj in adjectives]
topNouns = [noun for noun, freq in sorted(nounsWithFreq, key=lambda x: x[1], reverse=True)[:MOVIE_COUNT]]
topAdjectives = [adj for adj, freq in sorted(adjectivesWithFreq, key=lambda x: x[1], reverse=True)[:MOVIE_COUNT]]

# precompute left-skewed year weights: quadratic growth so recent years get far more movies,
# reflecting how film production has grown with technology (few in 1920s, many by 2020s)
releaseYears = np.arange(RELEASE_YEAR_MIN, RELEASE_YEAR_MAX + 1)
yearWeights = (releaseYears - RELEASE_YEAR_MIN + 1.0) ** 2
yearWeights /= yearWeights.sum()

# the loop with tqdm
for _ in tqdm(range(MOVIE_COUNT), desc="Generating movies"):
    # generate ids for movies
    while True:
        movieId = random.randint(ID_MIN, ID_MAX)
        if movieId not in usedMovieIds:
            usedMovieIds.add(movieId)
            movieIds.append(movieId)
            break

    # generate title
    article = "The" if random.random() > ARTICLE_PROBABILITY else ""
    adjective = random.choice(topAdjectives) if random.random() > ADJECTIVE_PROBABILITY else ""
    adjective = adjective.capitalize().strip()
    noun = random.choice(topNouns).capitalize().strip()
    movieTitle = f"{article} {adjective} {noun}".replace("  ", " ").strip()
    movieTitles.append(movieTitle)

    # choose release date from the left-skewed distribution
    releaseYear = int(np.random.choice(releaseYears, p=yearWeights))
    releaseDates.append(releaseYear)

    # choose genre
    genres.append(random.choice(movieGenres))

    # choose duration
    durations.append(random.randint(DURATION_MIN, DURATION_MAX))

    # assign a director who was at least 30 years old when the movie was released
    eligibleDirectors = directorsDf[directorsDf["birthYear"] <= releaseYear - 30]
    if eligibleDirectors.empty:
        # fallback: pick the oldest available director if no one meets the age constraint
        eligibleDirectors = directorsDf.nsmallest(1, "birthYear")
    director = eligibleDirectors.sample(1).iloc[0]
    movieDirectorIds.append(director["directorID"])

# convert the data into dataframe
df = pd.DataFrame({
    "movieID": movieIds,
    "movieTitle": movieTitles,
    "releaseDate": releaseDates,
    "genre": genres,
    "directorID": movieDirectorIds,
    "duration": durations
})

# save the dataset
df.to_csv("./tables/movies.csv", index=False)