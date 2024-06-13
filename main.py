# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
import praw
import os
import datetime

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv();
    reddit_client_username = os.getenv('REDDIT_CLIENT_USERNAME')
    print('running as username:', reddit_client_username)
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID', ""),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        password=os.getenv("REDDIT_CLIENT_PASSWORD", ""),
        user_agent=os.getenv("REDDIT_CLIENT_USERAGENT", ""),
        username=os.getenv("REDDIT_CLIENT_USERNAME", ""),
        ratelimit_seconds=int(os.getenv("REDDIT_CLIENT_RATELIMIT_SECONDS", "600")),
    )
    comment_delete_days = int(os.getenv('COMMENT_DELETE_DAYS', "7"))
    expiry = datetime.datetime.now() - datetime.timedelta(days=comment_delete_days)
    readonly_mode = os.getenv("READONLY", "True").lower() == "true"


    for comment in reddit.user.me().comments.new():

        comment_datetime = datetime.datetime.fromtimestamp(comment.created_utc)
        is_expired = comment_datetime > expiry
        print('is_expired', is_expired)
        if not readonly_mode:
            print(comment_datetime)
            print('will delete')
            #comment.delete()

