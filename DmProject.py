import praw
import pandas as pd
import warnings

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
