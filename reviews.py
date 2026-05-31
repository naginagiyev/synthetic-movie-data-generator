import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()

ROW_COUNT = 150000

# the generated ids' range
ID_MIN = 100000
ID_MAX = 999999

# reviews can be written up to this date
REVIEW_END_DATE = datetime(2026, 3, 23)

# load existing CSVs
moviesDf = pd.read_csv("./tables/movies.csv")
usersDf = pd.read_csv("./tables/users.csv")

# parse registration dates
usersDf["registrationDate"] = pd.to_datetime(usersDf["registrationDate"])

movieIdList = moviesDf["movieID"].tolist()
userIdList = usersDf["userID"].tolist()
userRegDateMap = dict(zip(usersDf["userID"], usersDf["registrationDate"]))

# precompute per-movie rating weight distributions
# each movie gets a random gaussian center and spread so ratings cluster naturally
RATING_OPTIONS = np.arange(1, 11)

def generateMovieWeights():
    # Build a probability vector over ratings 1-10 for a single movie.
    # Uses a gaussian curve around a random center, plus small noise.
    # The center is drawn from a triangular distribution (mode=7.5) so the
    # global rating histogram is left-skewed: most movies rate high, few rate low.
    center = random.triangular(1.5, 9.5, 7.5)
    sigma = random.uniform(0.8, 2.5)
    weights = np.exp(-0.5 * ((RATING_OPTIONS - center) / sigma) ** 2)
    weights += np.random.uniform(0.005, 0.04, len(RATING_OPTIONS))  # subtle noise
    weights /= weights.sum()
    return weights

movieRatingWeights = {mid: generateMovieWeights() for mid in tqdm(movieIdList, desc="Precomputing rating weights per movie")}

# precompute movie selection weights: newer movies receive quadratically more reviews,
# reflecting that older films attract fewer online reviewers than recent releases
movieIdArr = np.array(movieIdList)
releaseYearMap = dict(zip(moviesDf["movieID"], moviesDf["releaseDate"]))
movieYears = np.array([releaseYearMap[mid] for mid in movieIdList], dtype=float)
movieSelectionWeights = (movieYears - movieYears.min() + 1.0) ** 2
movieSelectionWeights /= movieSelectionWeights.sum()

# pre-sample unique review IDs all at once (much faster than a while-loop)
reviewIds = random.sample(range(ID_MIN, ID_MAX + 1), ROW_COUNT)

# generate reviews
reviewMovieIds = []
reviewUserIds = []
reviewRatings = []
reviewDates = []

for _ in tqdm(range(ROW_COUNT), desc="Generating reviews"):
    movieId = int(np.random.choice(movieIdArr, p=movieSelectionWeights))
    userId = random.choice(userIdList)

    # sample rating from this movie's weighted distribution
    rating = int(np.random.choice(RATING_OPTIONS, p=movieRatingWeights[movieId]))

    # review date must be after the user's registration date and not exceed REVIEW_END_DATE.
    # daysAvailable is computed to the start of REVIEW_END_DATE (midnight), so adding
    # intra-day time components must use daysAvailable - 1 as the day ceiling to avoid
    # overshooting midnight; the final clamp is a safety net for edge cases.
    regDate = userRegDateMap[userId]
    daysAvailable = (REVIEW_END_DATE - regDate).days
    if daysAvailable <= 0:
        reviewDate = regDate
    else:
        reviewDate = regDate + timedelta(
            days=random.randint(0, max(0, daysAvailable - 1)),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        reviewDate = min(reviewDate, REVIEW_END_DATE)

    reviewMovieIds.append(movieId)
    reviewUserIds.append(userId)
    reviewRatings.append(rating)
    reviewDates.append(reviewDate)

# build and save the dataframe
df = pd.DataFrame({
    "reviewID": reviewIds,
    "movieID": reviewMovieIds,
    "userID": reviewUserIds,
    "rating": reviewRatings,
    "reviewDate": reviewDates
})

df.to_csv("./tables/reviews.csv", index=False)