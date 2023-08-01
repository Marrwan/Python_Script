from script2 import scrape_reddit_users_info_without_auth
from script import scrape_reddit_users_info_with_auth

usernames = ["CoolAid876", "strange_dev", "strange__dev"]  # Add all 4000 usernames here
scrape_reddit_users_info_with_auth(usernames)
# scrape_reddit_users_info_without_auth(usernames)