import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Reddit API credentials
client_id = 'private'
client_secret = 'private'  #you can get your own from https://www.reddit.com/wiki/api/
user_agent = 'test'

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


# Define subreddit and keyword
subreddit_name = 'wallstreetbets'
buyCount = 0;
sellCount = 0;
holdCount = 0;
keyword = input('What Stock do you want to analyze: ')

    
# Fetch posts containing the keyword from the last 24 hours
subreddit = reddit.subreddit(subreddit_name)
posts = subreddit.search(keyword, sort='new', syntax='cloudsearch', time_filter='week', limit=10)  # Fetching 10 latest posts

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Define function to analyze sentiment of a text
def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']  # Using compound score as overall sentiment

# Define function to make trading decision based on sentiment
def make_trading_decision(sentiment_score):
    if sentiment_score >= 0.1:
        
        return 'BUY'
    elif sentiment_score <= -0.1:
        return 'SELL'
    else:
        return 'HOLD'

# Initialize DataFrame to store results
results = []

# Iterate through fetched posts and analyze sentiment
for post in posts:
    title_sentiment = analyze_sentiment(post.title)
    body_sentiment = analyze_sentiment(post.selftext)
    total_sentiment = (title_sentiment + body_sentiment) / 2  # Average sentiment of title and body
    decision = make_trading_decision(total_sentiment)
    if(decision == 'BUY'):
        buyCount += 1
    elif(decision == 'SELL'):
        sellCount = sellCount + 1
    else:
        holdCount += 1
    results.append({
        'Title': post.title,
        'Sentiment': total_sentiment,
        'Decision': decision
    })

# Convert results to DataFrame for easier analysis
results_df = pd.DataFrame(results)

# Print results
print(results_df)
if(buyCount > sellCount):
    print('Overall Suggestion -- BUY')
elif(sellCount > buyCount):
    print('Overall Suggestion -- SELL')
else:
    print('Overall Suggestion -- HOLD')
