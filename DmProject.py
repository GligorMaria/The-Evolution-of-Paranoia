import praw
import pandas as pd
import warnings
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Ignore PRAW async warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="praw")


DEMO_CLIENT_ID = 'sIXZTihLNiKiHw'
DEMO_CLIENT_SECRET = 'EjfAsmz5z8mDbZohe4UPYTPIZsYmOQ'
DEMO_USER_AGENT = 'TestAgentPraw:v1 (by /u/TemporaryUser)'

# MJ Part1
try:
    reddit = praw.Reddit(
        client_id=DEMO_CLIENT_ID,
        client_secret=DEMO_CLIENT_SECRET,
        user_agent=DEMO_USER_AGENT,
        check_for_async=False
    )

except Exception as e:
    print("Error creating PRAW instance:", e)

subreddits = [
    "conspiracy",
    "MichaelJackson",
    "UnresolvedMysteries",
    "PopCulture",
    "TrueCrime"
]

posts_data = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    print(f"Scraping r/{sub}...")

    for post in subreddit.search("Michael Jackson", limit=200):
        posts_data.append({
            "subreddit": sub,
            "title": post.title,
            "text": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "created": post.created_utc,
            "id": post.id,
            "url": post.url
        })

df = pd.DataFrame(posts_data)
df.to_csv("mj_reddit_posts.csv", index=False)

print("Saved mj_reddit_posts.csv")

# MJ Part2

# Download NLTK resources (only first time)
nltk.download('stopwords')
nltk.download('wordnet')

# Load dataset
df = pd.read_csv("mj_reddit_posts.csv")

# Remove duplicates
df.drop_duplicates(subset=["title", "text"], inplace=True)

# Remove empty posts
df = df[df["text"].notna()]

# Lowercase
df["clean_text"] = df["text"].str.lower()

# Remove URLs
df["clean_text"] = df["clean_text"].apply(lambda x: re.sub(r"http\S+|www\S+", "", x))

# Remove punctuation
df["clean_text"] = df["clean_text"].apply(lambda x: re.sub(r"[^\w\s]", "", x))

# Remove numbers
df["clean_text"] = df["clean_text"].apply(lambda x: re.sub(r"\d+", "", x))

# Remove stopwords
stop_words = set(stopwords.words("english"))
df["clean_text"] = df["clean_text"].apply(
    lambda x: " ".join([word for word in x.split() if word not in stop_words])
)

# Lemmatization
lemmatizer = WordNetLemmatizer()
df["clean_text"] = df["clean_text"].apply(
    lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()])
)

# Save cleaned dataset
df.to_csv("mj_reddit_posts_clean.csv", index=False)

print("Saved mj_reddit_posts_clean.csv")