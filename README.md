# 🎬 Movie Database Generator

This project creates a **fake movie database** as CSV files. You can use it for learning SQL, testing apps, or data analysis — without using real movie data.

---

## 📌 What does it do?

The scripts build six linked tables:

| Table | Rows | What it contains |
|-------|------|------------------|
| **directors** | 1,000 | Director names and birth years |
| **actors** | 5,000 | Actor names, birth years, and nationalities |
| **users** | 50,000 | Usernames, countries, and sign-up dates |
| **movies** | 10,000 | Titles, genres, release years, directors, and length |
| **roles** | 200,000 | Which actor played which character in which movie |
| **reviews** | 150,000 | User ratings (1-10) and review dates |

All files are saved in the `tables/` folder.

---

## 🚀 Quick start

### 1. Install Python packages

```bash
pip install pandas faker tqdm nltk numpy
```

### 2. Run the full pipeline

```bash
python generate.py
```

This runs all six scripts in order and shows progress and timing for each step.

> ⚠️ **Order matters.** `movies.py` needs `directors.csv`. `roles.py` needs `movies.csv` and `actors.csv`. `reviews.py` needs `movies.csv` and `users.csv`. Use `generate.py` to run everything in the right order.

---

## 📁 Project structure

```
Movie Database Generate/
├── generate.py      # Runs all scripts in order
├── directors.py     # Creates directors.csv
├── actors.py        # Creates actors.csv
├── users.py         # Creates users.csv
├── movies.py        # Creates movies.csv
├── roles.py         # Creates roles.csv
├── reviews.py       # Creates reviews.csv
├── test.ipynb       # Checks data quality and shows charts
└── tables/          # Output folder (created automatically)
    ├── directors.csv
    ├── actors.csv
    ├── users.csv
    ├── movies.csv
    ├── roles.csv
    └── reviews.csv
```

---

## 🔗 How the tables connect

```
directors --> movies <-- roles --> actors
                |
                v
              reviews <-- users
```

- Each **movie** has one **director**.
- Each **role** links one **actor** to one **movie** (with a character name).
- Each **review** links one **user** to one **movie** (with a rating and date).

---

## ✨ Smart details (why the data feels real)

The generator does more than random numbers:

- **Movie titles** — Built from common English words (nouns and adjectives from NLTK).
- **Release years** — More movies in recent years, fewer in old years (like real film history).
- **Director age rule** — A director must be at least 30 years old when their movie is released.
- **Actor age rule** — An actor must be at least 6 years old when the movie is released.
- **Every actor gets a role** — All 5,000 actors appear in at least one movie.
- **Review ratings** — Most movies score high (7-8 range), but some score low — like real review sites.
- **Review dates** — A user can only review after they sign up.
- **Unique IDs** — All IDs are 6-digit numbers with no duplicates inside each table.

---

## 📊 Table columns

### directors.csv

| Column | Type | Description |
|--------|------|-------------|
| directorID | int | Unique ID |
| directorName | string | Full name |
| birthYear | int | Year of birth |

### actors.csv

| Column | Type | Description |
|--------|------|-------------|
| actorID | int | Unique ID |
| actorName | string | Full name |
| birthYear | int | Year of birth |
| nationality | string | Country |

### users.csv

| Column | Type | Description |
|--------|------|-------------|
| userID | int | Unique ID |
| username | string | Login name |
| country | string | Country |
| registrationDate | date | When the user joined |

### movies.csv

| Column | Type | Description |
|--------|------|-------------|
| movieID | int | Unique ID |
| movieTitle | string | Movie name |
| releaseDate | int | Release year |
| genre | string | e.g. Drama, Comedy, Sci-Fi |
| directorID | int | Links to directors |
| duration | int | Length in minutes |

### roles.csv

| Column | Type | Description |
|--------|------|-------------|
| movieID | int | Links to movies |
| actorID | int | Links to actors |
| roleName | string | Character name |

### reviews.csv

| Column | Type | Description |
|--------|------|-------------|
| reviewID | int | Unique ID |
| movieID | int | Links to movies |
| userID | int | Links to users |
| rating | int | Score from 1 to 10 |
| reviewDate | datetime | When the review was written |

---

## 🧪 Testing the data

Open `test.ipynb` in Jupyter to:

- Load all six tables
- Check row counts and data rules
- View charts (release years, ratings, genres, and more)

---

## ⚙️ Change the size of the data

Each script has constants at the top you can edit:

| File | Constant | Default |
|------|----------|---------|
| `directors.py` | `DIRECTOR_COUNT` | 1,000 |
| `actors.py` | `ACTOR_COUNT` | 5,000 |
| `users.py` | `USER_COUNT` | 50,000 |
| `movies.py` | `MOVIE_COUNT` | 10,000 |
| `roles.py` | `ROW_COUNT` | 200,000 |
| `reviews.py` | `ROW_COUNT` | 150,000 |

After you change a value, run `generate.py` again to rebuild the tables.

---

## 📦 Requirements

- Python 3.8+
- pandas
- faker
- tqdm
- nltk
- numpy
