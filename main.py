# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
import praw
import os
from datetime import datetime
from time import sleep

from redditwipe.post_walker import PostWalker

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv();
    # todo: validate config options
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID', ""),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
        password=os.getenv("REDDIT_CLIENT_PASSWORD", ""),
        user_agent=os.getenv("REDDIT_CLIENT_USERAGENT", ""),
        username=os.getenv("REDDIT_CLIENT_USERNAME", ""),
        ratelimit_seconds=int(os.getenv("REDDIT_CLIENT_RATELIMIT_SECONDS", "600")),
    )
    comment_delete_days = os.getenv('COMMENT_DELETE_DAYS', "")
    comment_delete_minutes = os.getenv('COMMENT_DELETE_MINUTES', "")
    if comment_delete_days != "":
        # do this maximum once per day, since we're tracking by days
        minimum_time_seconds: int = 86400
        comment_delete_minutes = int(comment_delete_days) * 60 * 24
    else:
        if comment_delete_minutes != "":
            # do this once per 10 minutes the typical rate limit sleep period
            minimum_time_seconds: int = 10 * 60
            comment_delete_minutes = int(comment_delete_minutes)
        else:
            raise Exception("Missing COMMENT_DELETE_DAYS or COMMENT_DELETE_MINUTES")
    readonly_mode = not (os.getenv("READONLY", "False").lower() == "false")
    excluded_subreddits = os.getenv("EXCLUDED_SUBREDDITS", "").split(",")

    post_walker: PostWalker = PostWalker(excluded_subreddits, comment_delete_minutes)

    while True:
        walk_start: datetime = datetime.now()
        for comment in reddit.user.me().comments.new():
            should_delete = post_walker.should_delete_comment(comment)
            if not readonly_mode and should_delete:
                print('will delete')
                comment.delete()
                print('deleted')
        finished: datetime = datetime.now()
        duration = finished - walk_start
        total_minutes = duration.total_seconds() / 60

        if total_minutes < minimum_time_seconds:
            sleep_time = minimum_time_seconds - total_minutes
            print(f'sleeping for {sleep_time} seconds')
            sleep(sleep_time)
