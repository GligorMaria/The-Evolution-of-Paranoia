import praw
import pandas as pd
import warnings

# Ignore PRAW async warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="praw")

# Demo credentials (lab style)
DEMO_CLIENT_ID = 'sIXZTihLNiKiHw'
DEMO_CLIENT_SECRET = 'EjfAsmz5z8mDbZohe4UPYTPIZsYmOQ'
DEMO_USER_AGENT = 'TestAgentPraw:v1 (by /u/TemporaryUser)'

try:
    reddit = praw.Reddit(
        client_id=DEMO_CLIENT_ID,
        client_secret=DEMO_CLIENT_SECRET,
        user_agent=DEMO_USER_AGENT,
        check_for_async=False
    )

    print("PRAW instance created successfully.")
    print("Read-only mode:", reddit.read_only)
    print("Reddit URL:", reddit.config.reddit_url)

    # Small test: fetch the top post from r/Python
    subreddit = reddit.subreddit("Python")
    post = next(subreddit.hot(limit=1))
    print("\nTest fetch successful!")
    print("Sample post title:", post.title)

except Exception as e:
    print("Error creating PRAW instance:")
    print(e)
