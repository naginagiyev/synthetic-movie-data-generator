import random
import pandas as pd
from tqdm import tqdm
from faker import Faker
from datetime import datetime, timedelta

# initialize faker for data generation
faker = Faker()

# total number of users to generate
USER_COUNT = 50000

# the generated ids' range
ID_MIN = 100000
ID_MAX = 999999

# registration date range
START_DATE = datetime(2005, 12, 15)
END_DATE = datetime(2026, 3, 15)

# lists to store data
userIds = []
usernames = []
countries = []
registrationDates = []

# set to store used ids (to avoid duplicates)
usedUserIds = set()

# generate users with tqdm progress bar
for _ in tqdm(range(USER_COUNT), desc="Generating users"):
    # generate unique user ID
    while True:
        userId = random.randint(ID_MIN, ID_MAX)
        if userId not in usedUserIds:
            usedUserIds.add(userId)
            userIds.append(userId)
            break
    
    # generate username
    username = faker.user_name()
    usernames.append(username)
    
    # generate country
    country = faker.country()
    countries.append(country)
    
    # generate random registration date between START_DATE and END_DATE
    days_between = (END_DATE - START_DATE).days
    random_days = random.randint(0, days_between)
    registrationDate = START_DATE + timedelta(days=random_days)
    registrationDates.append(registrationDate)

# convert the data into dataframe
df = pd.DataFrame({
    "userID": userIds,
    "username": usernames,
    "country": countries,
    "registrationDate": registrationDates
})

# save the dataset as CSV
df.to_csv("./tables/users.csv", index=False)