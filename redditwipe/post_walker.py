
from praw.models import Comment, Subreddit
from datetime import datetime, timedelta

class PostWalker(object):
    _excluded_subreddits: list[str] = []
    _expiry_minutes: int = 86400

    _now: datetime = None
    def __init__(self, excluded_subreddits: list[str], expiry_minutes: int = 86400) -> None:
        self._excluded_subreddits = excluded_subreddits
        self._expiry_minutes = expiry_minutes
        pass

    def is_subreddit_excluded(self, subreddit_name: str) -> bool:
        return subreddit_name in self._excluded_subreddits

    def should_delete_comment(self, comment: Comment) -> bool:
        if comment.subreddit.display_name in self._excluded_subreddits:
            return False
        now: datetime = self._get_now()
        expiry_time: datetime = now - timedelta(minutes=self._expiry_minutes)
        comment_datetime: datetime = datetime.fromtimestamp(comment.created_utc)
        is_expired = comment_datetime < expiry_time
        return is_expired

    def _get_now(self) -> datetime:
        if self._now is None:
            return datetime.now()
        else:
            return self._now

    def inject_now(self, now: datetime) -> None:
        self._now = now


