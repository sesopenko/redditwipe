import unittest
from datetime import datetime, timedelta

import redditwipe.post_walker
from unittest.mock import MagicMock
from praw.models import Comment, Subreddit
from praw import Reddit

def reddit():
    """Return an instance of :class:`.Reddit` that doesn't make requests to Reddit."""
    reddit = Reddit(client_id="dummy", client_secret="dummy", user_agent="dummy")
    # Unit tests should never issue requests
    reddit._core.request = dummy_request
    yield reddit

def dummy_request(*args, **kwargs):
    pass

test_scenarios = [
    {
        'input': (),
        'expected': False,
    },
]

now: datetime = datetime.now()
five_minutes_ago = now - timedelta(minutes=5)
ten_minutes_ago = now - timedelta(minutes=10)
twenty_minutes_ago = now - timedelta(minutes=20)
day_ago = now - timedelta(days=1)

now_utc: float = now.timestamp()
class PostWalkerTestCase(unittest.TestCase):

    def test_is_subreddit_excluded(self):
        excluded: list[str] = ["something"]
        walker = redditwipe.post_walker.PostWalker(excluded)
        walker.inject_now(now)
        result = walker.is_subreddit_excluded("something")
        self.assertTrue(result)
    def test_should_not_delete_from_excluded_subreddit(self):
        excluded: list[str] = ["something"]
        walker = redditwipe.post_walker.PostWalker(excluded)
        walker.inject_now(now)
        mock_comment = MagicMock(spec=Comment)
        mock_comment.id = "1234"
        mock_comment.created_utc = day_ago.timestamp()
        mock_subreddit = MagicMock(spec=Subreddit)
        mock_subreddit.display_name = "something"
        mock_comment.subreddit = mock_subreddit
        result = walker.should_delete_comment(mock_comment)
        self.assertFalse(result)
    def test_should_not_delete_recent_comment(self):
        expiry_minutes: int = 60 * 24
        excluded: list[str] = []
        walker = redditwipe.post_walker.PostWalker(excluded, expiry_minutes)
        walker.inject_now(now)
        mock_comment = MagicMock(spec=Comment)
        mock_comment.id = "1234"
        mock_comment.created_utc = five_minutes_ago.timestamp()
        mock_subreddit = MagicMock(spec=Subreddit)
        mock_subreddit.display_name = "something"
        mock_comment.subreddit = mock_subreddit
        result = walker.should_delete_comment(mock_comment)
        self.assertFalse(result)

    def test_should_delete_expired_comment(self):
        expiry_minutes: int = 5
        excluded: list[str] = []
        walker = redditwipe.post_walker.PostWalker(excluded, expiry_minutes)
        walker.inject_now(now)
        mock_comment = MagicMock(spec=Comment)
        mock_comment.id = "1234"
        mock_comment.created_utc = ten_minutes_ago.timestamp()
        mock_subreddit = MagicMock(spec=Subreddit)
        mock_subreddit.display_name = "something"
        mock_comment.subreddit = mock_subreddit
        result = walker.should_delete_comment(mock_comment)
        self.assertTrue(result)
    def test_should_not_delete_expired_comment_from_excluded_subreddit(self):
        expiry_minutes: int = 5
        excluded: list[str] = ["excluded"]
        walker = redditwipe.post_walker.PostWalker(excluded, expiry_minutes)
        walker.inject_now(now)
        mock_comment = MagicMock(spec=Comment)
        mock_comment.id = "1234"
        mock_comment.created_utc = ten_minutes_ago.timestamp()
        mock_subreddit = MagicMock(spec=Subreddit)
        mock_subreddit.display_name = "excluded"
        mock_comment.subreddit = mock_subreddit
        result = walker.should_delete_comment(mock_comment)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
