import os
import praw
import csv

# Constants
CSV_FILE_NAME = 'csv/reddit_profiles_with_auth.csv'
REDDIT_API_CREDENTIALS = {
    'client_id' : 'NOqM7Rrz-WcqMoNaMuy8ag',
    'client_secret' : 'atE1E5MnsgwnEVW9jUK8w9Je4lEyfQ',
    'user_agent' : 'MyRedditApp v1.0 by YourUsername'
}

def fetch_user_info(reddit, username):
    try:
        user = reddit.redditor(username)

        user_info = {
            'username': user.name,
            'user_id': user.id,
            'comment_karma': user.comment_karma,
            'link_karma': user.link_karma,
            'created_utc': user.created_utc,
        }
        return user_info
    except praw.exceptions.RedditAPIException as e:
        print(f"Error while fetching user info for username: {username}")
        print("Error Message:", str(e))
        return None

def fetch_and_save_user_info(reddit, usernames):
    # List to store fetched user information
    user_data_list = []

    # Fetch user information for each username
    for username in usernames:
        user_info = fetch_user_info(reddit, username)
        if user_info:
            user_data_list.append(user_info)
    if not os.path.exists('csv'):
        os.makedirs('csv')
    # Save user information to a CSV file
    with open(CSV_FILE_NAME, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username', 'user_id', 'comment_karma', 'link_karma', 'created_utc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user_data_list)
        print('Scrapping successful, Check the ' + CSV_FILE_NAME + ' file')

def scrape_reddit_users_info_with_auth(usernames):
    # Reddit API credentials
    reddit = praw.Reddit(
        client_id=REDDIT_API_CREDENTIALS['client_id'],
        client_secret=REDDIT_API_CREDENTIALS['client_secret'],
        user_agent=REDDIT_API_CREDENTIALS['user_agent']
    )

    # Process the usernames in batches (e.g., 500 at a time)
    batch_size = 500
    for i in range(0, len(usernames), batch_size):
        batch_usernames = usernames[i:i + batch_size]
        fetch_and_save_user_info(reddit, batch_usernames)


