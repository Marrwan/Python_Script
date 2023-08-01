import os
import requests
import time
import csv

RATE_LIMIT_INTERVAL = 2  # Seconds between API requests
REDDIT_API_BASE_URL = "https://www.reddit.com/user/{}/about.json"

def fetch_user_info(username):
    url = REDDIT_API_BASE_URL.format(username)
    headers = {
        "User-Agent": "PythonScrapingApp/1.0"
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            print(f"Error while fetching user info for username: {username}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error while making the request for username: {username}")
        print("Error Message:", str(e))
        return None

def fetch_and_save_user_info(usernames):
    # List to store fetched user information
    user_data_list = []

    # Fetch user information for each username
    for username in usernames:
        user_info = fetch_user_info(username)
        if user_info:
            user_data_list.append(user_info)

        # Introduce a delay to manage rate limiting
        time.sleep(RATE_LIMIT_INTERVAL)

    # Get all unique keys from the user_info dictionaries
    fieldnames = set()
    for user_info in user_data_list:
        fieldnames.update(user_info.keys())

    if not os.path.exists('csv'):
        os.makedirs('csv')

    # Save user information to a CSV file
    with open('csv/reddit_profiles_without_auth.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user_data_list)
        print('Scrapping successful, Check the csv/reddit_profiles_without_auth.csv file')

def scrape_reddit_users_info_without_auth(usernames):
    batch_size = 500

    for i in range(0, len(usernames), batch_size):
        batch_usernames = usernames[i:i + batch_size]
        fetch_and_save_user_info(batch_usernames)

